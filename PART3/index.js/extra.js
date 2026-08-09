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
    id: (Math.floor(Math.random() * 10000)).toString(),
    name,
    number
  }
  persons.push(newPerson)
  res.status(201).json(newPerson)
  console.log('Created person:', JSON.stringify(newPerson))
})
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