require('dotenv').config()


const express = require('express')
const morgan = require('morgan')
const cors = require('cors')
const mongoose = require('mongoose')
console.log('Backend started')

const url = process.env.MONGODB_URI
const app = express()
morgan.token('body', (req) => {
  return JSON.stringify(req.body)
})
app.use(express.static('dist'))
app.use(cors())

app.use(express.json())
app.use(morgan(':method :url :status :body'))
mongoose.connect(url, { family: 4 })
  .then(() => {
    console.log('connected to MongoDB')


  })
  .catch(error => {
    console.log('error connecting to MongoDB:', error.message)
  })
const Phonebook = require('../model.js')





app.post('/api/persons', (req, res, next) => {
  const body = req.body
  if (!body.name || !body.number) {
    return res.status(400).json({
      error: 'Name or number is missing'
    })
  }
  const person = new Phonebook({
    name: body.name,
    number: body.number,
  })
  Phonebook.findOne({ name: body.name })
    .then(existingPerson => {
      if (existingPerson) {
        return res.status(400).json({
          error: 'name must be unique'
        })
      }

      return person.save()
    })
    .then(savedPerson => {
      res.json(savedPerson)
      console.log('Created person:', JSON.stringify(savedPerson))
    })
    .catch(error => {

      console.log('CATCH BLCK RUNNING')

      console.error(error)
      next(error)
      console.log('CATCH BLOCK RUNNING')
      console.error(error)
    })
})
app.get('/api/persons', (req, res) => {
  console.log('Fetching all persons from backend')
  Phonebook.find({}).then(persons => {
    res.json(persons)
  })
})

app.put('/api/persons/:id', (request, response) => {
  console.log('test')
  console.log(`Updating person with id: ${request.params.id}`)
  const body = request.body

  if (!body.name || !body.number) {
    return response.status(400).json({ error: 'Name or number is missing' })
  }

  const person = {
    name: body.name,
    number: body.number,
  }

  Phonebook.findByIdAndUpdate(request.params.id, person, { new: true })
    .then(updatedPerson => {
      if (updatedPerson) {
        response.json(updatedPerson)
      } else {
        response.status(404).end()
      }
    })
    .catch(error => {
      console.log(error)
      response.status(400).send({ error: 'malormatted id' })
    })
})

app.get('/api/persons/:id', (req, res) => {
  console.log('6a74868be9e57e2328cc8ad'.length)
  console.log(`Fetching person with id: ${req.params.id}`)

  Phonebook.findById(req.params.id)
    .then(Phonebook => {
      if (Phonebook) {
        res.json(Phonebook)

      } else {
        res.status(404).end()
      }
    })
    .catch(error => {
      console.log(error)
      res.status(400).send({ error: 'malormatted id' })
    })
})
app.delete('/api/persons/:id', (request, response, next) => {
  console.log(request.params)
  console.log(`Deleting person with id: ${request.params.id}`)
  Phonebook.findByIdAndDelete(request.params.id)
    .then(() => {
      response.status(204).end()
    })
    .catch(error => next(error))
})
const unknownEndpoint = (request, response) => {
  response.status(404).send({ error: 'unknown endpoint' })
}
app.use(unknownEndpoint)

const errorHandler = (error, request, response, next) => {
  console.error(error.message)


  if (error.name === 'ValidationError') {
    return response.status(400).json({
      error: error.message
    })
  }

  next(error)
}
app.use(errorHandler)
// handler of requests that result in errors
app.use(errorHandler)
const PORT = 3001
app.listen(PORT, () => { console.log(`Server running on port ${PORT}`) })
