import { useState, useEffect } from 'react'
import Filter from './filter'
import PersonForm from './personform'
import Persons from './person'
import { getAll, create, remove, update } from './backend'

const App = () => {
  const [persons, setPersons] = useState([])
  
  
  useEffect(() => {
    console.log('effect')

    getAll()
      .then(response => {
        console.log(response)
        setPersons(response.data)
      })
      .catch(error => {
        console.error('Error fetching persons:', error)
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

    const nameofperson = persons.find(person => person.name === newName)

    if (nameofperson) {
      if (window.confirm(`it already exists do you want change ${newName}?`)) {
        const changednumperson = {
          ...nameofperson,
          phone: newNum,
        }

        update(nameofperson.id, changednumperson)
          .then(response => {
            setPersons(persons.map(person =>
              person.id === nameofperson.id ? response.data : person
            ))
            setNewNum('')
            setNewName('')
          })
          .catch(error => {
            console.error('Error updating person:', error)
          })
      }
      return
    }

    const personObject = {
      name: newName,
      phone: newNum,
      id: persons.length + 1
    }

    create(personObject)
      .then(response => {
        setPersons(persons.concat(response.data))
        setNewNum('')
        setNewName('')
      })
      .catch(error => {
        console.error('Error creating person:', error)
      })
  }

  const deletePerson = (id) => {
    const person = persons.find(i => i.id === id)
    if (window.confirm(`Delete ${person.name}?`)) {
      remove(id)
        .then(() => {
          console.log(`Deleted person with id ${id}`)
          setPersons(persons.filter(i => i.id !== id))
        })
        .catch(error => {
          console.error('Error deleting person:', error)
        })
    }
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
      <Persons persons={filteredPersons} deletePerson={deletePerson} />
    </div>
  )
}   
export default App
