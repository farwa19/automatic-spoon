
const express = require('express')
const morgan = require('morgan')


const app = express()
morgan.token('body', (req) => {
  return JSON.stringify(req.body)
})



app.use(morgan('tiny'))
app.use(express.json())
app.use(morgan(':method :url :status :body'))
const persons = [
  
    { 
      "id": "1",
      "name": "Arto Hellas", 
      "number": "040-123456"
    },
    { 
      "id": "2",
      "name": "Ada Lovelace", 
      "number": "39-44-5323523"
    },
    { 
      "id": "3",
      "name": "Dan Abramov", 
      "number": "12-43-234345"
    },
    { 
      "id": "4",
      "name": "Mary Poppendieck", 
      "number": "39-23-6423122"
    }
]

app.get('/', (req, res) => { res.send('Phonebok backend is running!') }) 
console.log('Server running on port 3001') 



app.get('/api/persons', (req, res) => { res.json(persons) })
app.get('/info', (req, res) => {
  const date = new Date()
  res.send(`<p>Phonebook has info for ${persons.length} people</p><p>${date}</p>`)
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
app.delete('/api/persons/:id', (req, res) => {
  const id = req.params.id
  console.log(`Deleting person with id: ${id}`)
  const index = persons.findIndex(p => p.id === id)
  if (index !== -1) {
    persons.splice(index, 1)
    res.status(204).end()
  } else {
    res.status(404).end()
  }
})
app.post('/api/persons', (req, res) => {
  const { name, number } = req.body
  if (!name || !number) {
    return res.status(400).json({ error: 'Name or number is missing' })
  }
  const existingPerson = persons.find(p => p.name === name)
  if (existingPerson) {
    return res.status(400).json({ error: 'Name must be unique' })
  }
  const newPerson = {
    id: (Math.floor(Math.random() * 10000)).toString(),
    name,
    number
  }
  persons.push(newPerson)
  res.status(201).json(newPerson)
  console.log(
  JSON.stringify([newPerson]),
);
})

const PORT = 3001 
app.listen(PORT, () => { console.log(`Server running on port ${PORT}`) })