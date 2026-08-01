import { useState } from 'react'
import Filter from './filter'
import PersonForm from './personform'
import Persons from './person'



const App = () => {
  
  const [persons, setPersons] = useState([
    { name: 'Arto Hellas', phone: '040-123456', id: 1 },
    { name: 'Ada Lovelace', phone: '39-44-5323523', id: 2 },
    { name: 'Dan Abramov', phone: '12-43-234345', id: 3 },
    { name: 'Mary Poppendieck', phone: '39-23-6423122', id: 4 }
  ])
  console.log('persons', persons)
  const [gh, setGh] = useState('')
  const [newName, setNewName] = useState('')
  const [newNum, setNewNum] = useState('')

  const handleNumChange = (event) => {
    setNewNum(event.target.value)
  }

  const handleNameChange = (event) => {
    setNewName(event.target.value)
  }
  const filteredPersons = persons.filter(person =>
    person.name.toLowerCase().includes(gh.toLowerCase())
  )

  const addPerson = (event) => {
    event.preventDefault()

    const exists = persons.some(person => person.name === newName)
    if (exists) {
      window.alert(`${newName} is already in the phonebook`)
      return
    }

    const personObject = {
      name: newName,
      phone: newNum,
      id: persons.length + 1
    }

    setPersons(persons.concat(personObject))
    setNewNum('')
    setNewName('')
  }
  console.log('render', persons.length, 'persons')

  

  return (
    <div>
      <h1>phonebook</h1>
      <Filter value={gh} onChange={(event) => setGh(event.target.value)} />

      <h2>add a new</h2>
      <PersonForm
        onSubmit={addPerson}
        nameValue={newName}
        nameOnChange={handleNameChange}
        numValue={newNum}
        numOnChange={handleNumChange}
      />

      <h2>Numbers</h2>
      <Persons persons={filteredPersons} />
      
    </div>
  )
}

export default App
