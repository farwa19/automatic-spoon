 

const config = require('./utils/config')
const { info, error } = require('./utils/logger')
const express = require('express')
const mongoose = require('mongoose')
const app = express()
const loginRouter = require('./controllers/log')
const usersRouter = require('./users')


const Blog = require('./models/model')
const reverse = require('./utils/for_testing').reverse

app.use(express.json())
app.use('/api/users', usersRouter) 
app.use('/api/login', loginRouter)


const jwt = require('jsonwebtoken')
const User = require('./models/user')
const tokenExtractor = (request, response, next) => {
  const authorization = request.get('authorization')
  
  if (authorization && authorization.startsWith('Bearer ')) {
    request.token = authorization.replace('Bearer ', '')
  } else {
    request.token = null 
  }
  
  next()
}
const userExtractor = async (request, response, next) => {
   if (request.token) {
    const decodedToken = jwt.verify(request.token, process.env.SECRET)
    
    if (decodedToken.id) {
      request.user = await User.findById(decodedToken.id)
    }
  }
  next()
}
app.use(tokenExtractor)
app.use(userExtractor)


const mongoUrl = config.MONGODB_URI
mongoose.connect(mongoUrl, { family: 4 })

app.use(express.json())
app.get('/api/blogs/:id', async (request, response) => {
  const note = await Blog.findById(request.params.id)
  
  if (note) {
    response.json(note)
  } else {
    response.status(404).end()
  }
})
app.delete('/api/blogs/:id', userExtractor, async (request, response) => {

  const blog = await Blog.findById(request.params.id)
  console.log(blog)
  if (!blog) {
    return response.status(404).json({ error: 'blog not found' })
  }
  const user = request.user
  console.log(user)

  if (!user) {
    return response.status(400).json({ error: 'user missing or not valid' })
  }
  if (blog.user && blog.user.toString() === user._id.toString())
     {
    
    await Blog.findByIdAndDelete(request.params.id)
    return response.status(204).end()
    
  }
  
  else{return response.status(401).json({ error: 'only the creator can delete a blog' })}
})

app.put('/api/blogs/:id', async (request, response) => {
  await Blog.findById(request.params.id)
  
  const blog = {
    title: request.body.title,
    author: request.body.author,
    url: request.body.url,
    likes: request.body.likes
  }
  const updatedBlog = await Blog.findByIdAndUpdate(request.params.id, blog, { new: true })
  
  if (updatedBlog) {
    response.json(updatedBlog)
  } else {
    response.status(404).end()
  }
})

const errorHandler = (error, request, response, next) => {
  if (error.name === 'CastError') {
    return response.status(400).send({ error: 'malformatted id' })
  } else if (error.name === 'ValidationError') {
    return response.status(400).json({ error: error.message })
  } else if (error.name === 'MongoServerError' && error.message.includes('E11000 duplicate key error')) {
    return response.status(400).json({ error: 'expected `username` to be unique' })

  } else if (error.name ===  'JsonWebTokenError') {
    return response.status(401).json({ error: 'token invalid' })
  
   } else if (error.name === 'TokenExpiredError') {
    return response.status(401).json({
      error: 'token expired'
    })
  }

  next(error)
}
app.get('/api/blogs', (request, response) => {
  Blog.find({}).then((blogs) => {
    response.json(blogs)
  })
})

app.post('/api/blogs', userExtractor, async (request, response) => {
  const body = request.body
  if (!body.author) { 
    return response.status(400).json({ error: 'author is missing' })
  }
  if (!body.url) { 
    return response.status(400).json({ error: 'url is missing' })
  }
  if (!body.title) { 
    return response.status(400).json({ error: 'title is missing' })
  }
  
  
   
  
 const user = request.user

  if (!user) {
    return response.status(401).json({ error: 'userId missing or not valid' })
  }
  

  const blog = new Blog({
    title: body.title,
    author: body.author,
    url: body.url,
    user: user._id,
    likes: body.likes || 0
    
  })
  const result = await blog.save()
  
  
  user.blog = user.blog.concat(result._id) 
  await user.save()

  

  response.status(201).json(result)
})
app.get('/api/blogs/:id', async (request, response) => {
  const note = await Blog.findById(request.params.id)
  if (note) {
    response.json(note)
  } else {
    response.status(404).end()
  }
})
app.get('/', (request, response) => {
  response.send('<h1>Blog API is running</h1>')
})

module.exports = app