
const assert = require('node:assert')
const mongoose = require('mongoose')
const supertest = require('supertest')
const app = require('../app')
const { test, after,describe, beforeEach } = require('node:test')

const helper = require('./test_helper')
const Blogs = require('../models/model')

const bcrypt = require('bcrypt')
const User = require('../models/user')
beforeEach(async () => {
  await User.deleteMany({})
  
  const passwordHash = await bcrypt.hash('sekret', 10)
  const user = new User({ username: 'root', passwordHash })
  await user.save()
})
const api = supertest(app)

const initialBlogs = [
  {
    title: 'React patterns',
    author: 'Michael',
    url: 'https://reactpatterns.com/',
    likes: 7,
  },
  {
    title: 'Go To Statement Considered Harmful',
    author: 'Edsger W. Dijkstra',
    url: 'http://www.u.arizona.edu/~rubinson/copyright_violations/Go_To_Considered_Harmful.html',
    likes: 5,
  },
]
beforeEach(async () => {
  await Blogs.deleteMany({})
  const user = await User.findOne({ username: 'root' })
  let blogObject = new Blogs({ 
    ...initialBlogs[0], 
    user: user._id 
  })
  await blogObject.save()
  
  blogObject = new Blogs({ 
    ...initialBlogs[1], 
    user: user._id 
  })
  await blogObject.save()
  
  
  
  
  
})
beforeEach(async () => {
  const loginResponse = await api
    .post('/api/login')
    .send({ username: 'root', password: 'sekret' })
    
  token = loginResponse.body.token
})
test('Blog List Tests', async () => {
  const response = await api
    .get('/api/blogs')
    .expect(200) 
    .expect('Content-Type', /application\/json/)
  console.log("here t")


  assert.strictEqual(response.body.length, initialBlogs.length)
})

test('a specific blog is within the returned notes', async () => {
  const response = await api.get('/api/blogs')

  
  const contents = response.body.map(e => e.title)
  const bloh=  {
    title: 'Go To Statement Considered Harmful',
    author: 'Edsger W. Dijkstra',
    url: 'http://www.u.arizona.edu/~rubinson/copyright_violations/Go_To_Considered_Harmful.html',
    likes: 5,
  }
  assert.strictEqual(contents.includes(bloh.title), true)
})
test('a valid blog can be added ', async () => {
  console.log("valid")
  const newblog = {
    title: 'React patterns4 ',
    author: 'john',
    url: 'https://reactpatterns4.com/',
    user:"6a86b5b02af48fd49b80297e",
    likes: 10,
  }

  await api
    .post('/api/blogs')
    .set('Authorization', `Bearer ${token}`)
    .send(newblog)
    .expect(201)
    .expect('Content-Type', /application\/json/)

  const response = await api.get('/api/blogs')
  console.log(token)
  console.log("hijhsahjsjxhjsx")

  const contents = response.body.map(r => r.title)

  assert.strictEqual(response.body.length, initialBlogs.length + 1)

  assert(contents.includes('React patterns4 '))
})
test('a blog with no likes ', async () => {
  const newblog = {
    title: 'React patterns4 ',
    author: 'john',
    user:"6a86b5b02af48fd49b80297e",
    url: 'https://reactpatterns4.com/',
    
  }

  await api
    .post('/api/blogs')
    .set('Authorization', `Bearer ${token}`)
    .send(newblog)
    .expect(201)
    .expect('Content-Type', /application\/json/)

  const response = await api.get('/api/blogs')

  const contents = response.body.map(r => r.likes)
  console.log(response,'jy')
  const last = response.body[response.body.length - 1]

 

  assert.strictEqual(last.likes, 0)
})
test('unique identifier property of the blog posts is named id', async () => {
  const response = await api.get('/api/blogs')
  const blog = response.body[0]
  assert(blog.id)
  assert(!blog._id)
})

test('blog without author is not added', async () => {
  const newblog = {
    title: 'React pattrns4 ',
    
    url: 'https://reactpatterns4.com/',
    likes: 10,
  }
  })
test('blog without title is not added', async () => {
  const newblog = {
    author: 'hshgq',
    
    url: 'https://reactpatterns4.com/',
    likes: 10,
  }
  await api
    .post('/api/blogs')
    .send(newblog)
    .expect(400)

  const response = await api.get('/api/blogs')

  assert.strictEqual(response.body.length, initialBlogs.length)
})
test('blog without url is not added', async () => {
  const newblog = {
    author: 'hshgq',
    title: 'React pattrns4 ',
    
    likes: 10,
  }
  await api
    .post('/api/blogs')
    .send(newblog)
    .expect(400)

  const response = await api.get('/api/blogs')

  assert.strictEqual(response.body.length, initialBlogs.length)
})
test('a specific note can be viewed', async () => {
  const blogsAtStart = await helper.notesInDb()
  const blogToView = blogsAtStart[0]
  console.log(blogToView,"hereS")


  const resultBlog = await api
    .get(`/api/blogs/${blogToView.id}`) 

    .expect(200)
    .expect('Content-Type', /application\/json/)

  console.log('STATUS CODE:', resultBlog.status)
  console.log('RESPONSE TEXT:', resultBlog.text)
  assert.deepStrictEqual(resultBlog.body, JSON.parse(JSON.stringify(blogToView)))
})
test.only('a blog can be deleted', async () => {
  const blogsAtStart = await helper.notesInDb()
  const blogToDelete = blogsAtStart[0]
  console.log(blogToDelete,'fgyttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt')

  const response = await api
    .delete(`/api/blogs/${blogToDelete.id}`) 
    .set('Authorization', `Bearer ${token}`)
    //.expect(204)

  const blogsAtEnd = await helper.notesInDb()
  console.log('respokjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjnse')
  console.log(response.status)

  const ids = blogsAtEnd.map(n => n.id)
  assert(!ids.includes(blogToDelete.id))

  assert.strictEqual(blogsAtEnd.length, helper.initialBlogs.length - 1)
})
test('a valid blog can be updated ', async () => {
  const blogsAtStart = await helper.notesInDb()
  const blogToUpdate = blogsAtStart[0]
  
  const changed = {
    id: blogToUpdate.id,
    title: blogToUpdate.title,
    author: blogToUpdate.author,
    url: blogToUpdate.url,
    likes: 10 
  }
  console.log(changed,"change")
  

  const response = await api
    .put(`/api/blogs/${changed.id}`) 
    .send(changed)
    
    .expect(200) 
    .expect('Content-Type', /application\/json/)

  
  console.log(response.body)
  assert.strictEqual(response.body.likes, 10)
})

after(async () => {
  await mongoose.connection.close()
})

describe('when there is initially one user in db', () => {
  beforeEach(async () => {
    await User.deleteMany({})
    

    const passwordHash = await bcrypt.hash('sekret', 10)
    const user = new User({ username: 'root', passwordHash })

    await user.save()
  })

  test('creation succeeds with a fresh username', async () => {
    const usersAtStart = await helper.usersInDb()

    const newUser = {
      username: 'mluukkai',
      name: 'Matti Luukkainen',
      password: 'salainen',
    }
    console.log("here i am")

    response = await api
      .post('/api/users')
      .send(newUser)
      .expect(201)
      .expect('Content-Type', /application\/json/)

    console.log('HTTP Status:', response.status) 


      const usersAtEnd = await helper.usersInDb()

      console.log('Users in DB:', usersAtEnd)

    assert.strictEqual(usersAtEnd.length, usersAtStart.length + 1)

    const usernames = usersAtEnd.map(u => u.username)
    assert(usernames.includes(newUser.username))
  })
   test('creation fails when username when username with less then 3 chracters entered', async () => {
    const usersAtStart = await helper.usersInDb()

    const newUser = {
      username: 'mu',
      name: 'Matti Luukkainen',
      password: 'salainen',
    }
    console.log("here i am")

    response = await api
      .post('/api/users')
      .send(newUser)
      .expect(400)
      .expect('Content-Type', /application\/json/)

    console.log('HTTP Status:', response.status) 
    const usersAtEnd = await helper.usersInDb()


      

    assert.strictEqual(usersAtEnd.length, usersAtStart.length)

    
  })
  test('creation fails when username when password with less then 3 chracters entered', async () => {
    const usersAtStart = await helper.usersInDb()

    const newUser = {
      username: 'mukjk',
      name: 'Matti Luukkainen',
      password: 'sn',
    }
    console.log("here i am")

    response = await api
      .post('/api/users')
      .send(newUser)
      .expect(400)
      .expect('Content-Type', /application\/json/)

    console.log('HTTP Status:', response.status) 
    const usersAtEnd = await helper.usersInDb()


      

    assert.strictEqual(usersAtEnd.length, usersAtStart.length)

    
  })

})
test('adding a blog fails with status code 401 if token is not provided', async () => {
  const newBlog = {
    title: 'hi ',
    author: 'check',
    url: 'http://check.com',
    likes: 0
  }

  await api
    .post('/api/blogs')
    .send(newBlog) 
    .expect(401)
    .expect('Content-Type', /application\/json/)
})