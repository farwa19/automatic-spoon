import { useState } from 'react'
import Filter from './filter'
import PersonForm from './personform'
import Persons from './person'
import axios from 'axios'
import { useEffect } from 'react'


const App = () => {
  const [persons, setPersons] = useState([])
  
  
  useEffect(() => {
    console.log('effect')
    
    axios
      .get('https://special-space-journey-pj7jq7qxjwrqc9w4v-3001.app.github.dev/persons')
      .then(response => {
        console.log(response)
        setPersons(response.data)

      })
  }, [])
  console.log('render', persons.length, 'persons')
  

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
