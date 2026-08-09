
const express = require('express')
const Phonebook = require('../model.js')
const persons = 'yuus'

const app = express()

app.use(express.json())

app.post('/api/persons', (req, res) => {
  console.log('POST /api/persons body:', req.body)

  const { name, number } = req.body

  if (!name || !number) {
    return res.status(400).json({ error: 'Name or number is missing' })
  }

  const existingPerson = persons.find(p => p.name === name)

  if (existingPerson) {
    return res.status(400).json({ error: 'Name must be unique' })
  }

  const newPerson = {
    id: Math.floor(Math.random() * 10000).toString(),
    name,
    number
  }

  persons.push(newPerson)
  res.status(201).json(newPerson)

  console.log('Created person:', JSON.stringify(newPerson))
})

app.get('/info', (req, res) => {
  const date = new Date()

  res.send(
    `<p>Phonebook has info for ${persons.length} people</p><p>${date}</p>`
  )
})

app.get('/api/persons/:id', (req, res) => {
  const id = req.params.id

  console.log(`Fetching person with id: ${id}`)

  const person = persons.find(p => p.id === id)

  if (person) {
    res.json(person)
  } else {
    res.status(404).end()
  }
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