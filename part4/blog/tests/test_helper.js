const Blog = require('../models/model')
const User = require('../models/user')
const initialBlogs = [
  {
    title: 'React patterns3',
    author: 'Michael',
    url: 'https://reactpatterns.com/',
    likes: 7,
  },
  {
    title: ' Statement Considered Harmful',
    author: 'Edsger W. Dijkstra',
    url: 'http://www.u.arizona.edu/~rubinson/copyright_violations/Go_To_Considered_Harmful.html',
    likes: 5,
  },
]
const nonExistingId = async () => {
  const blog = new Blog({
    title: ' Statement Considered Harmful',
    author: 'Edsger  Dijkstra',
    url: 'http://www.u.arizona.edu/~rubinson/copyright_violations/Go_To_Considered_Harmful.html',
    likes: 5,
  })
  await blog.save()
  await blog.deleteOne()

  return blog._id.toString()
}

const notesInDb = async () => {
  const notes = await Blog.find({})
  return notes.map(blog => blog.toJSON())
}
const usersInDb = async () => {
  const users = await User.find({})
  return users.map(u => u.toJSON())
}


module.exports = {
  initialBlogs, nonExistingId, notesInDb, usersInDb,
}