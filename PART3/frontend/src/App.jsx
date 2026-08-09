import { useState, useEffect } from 'react'
import Filter from './filter'
import PersonForm from './personform'
import Persons from './person'
import { Notification } from './notification'
import { ErrorNotification } from './notification'
import { getAll, create, remove, update } from './backend'
import './App.css'

const App = () => {
  const [persons, setPersons] = useState([])
  const [notificationMessage, setNotificationMessage] = useState(null)
  const [errorNotificationMessage, setErrorNotificationMessage] = useState(null)

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
    console.log('addPerson called')
    event.preventDefault()
    const trimmedName = newName.trim()
    if (!trimmedName || !newNum.trim()) {
      console.log('Name or number is empty')
      setErrorNotificationMessage('Name or number cannot be empty')
      setTimeout(() => {
        setErrorNotificationMessage(null)
      }, 5000)
      return
    }

    const existingPerson = persons.find(person => person.name.toLowerCase() === trimmedName.toLowerCase())
    if (existingPerson) {
      if (window.confirm(`${trimmedName} is already added to phonebook, replace the old number with a new one?`)) {
        const updatedPerson = { ...existingPerson, number: newNum }
        update(existingPerson.id ?? existingPerson._id, updatedPerson)
          .then(response => {
            setPersons(persons.map(person => (person.id ?? person._id) === (existingPerson.id ?? existingPerson._id) ? response.data : person))
            setNotificationMessage(`Updated ${trimmedName}'s number`)
            setTimeout(() => {
              setNotificationMessage(null)
            }, 5000)
            setNewNum('')
            setNewName('')
          })
          .catch(error => {
            console.error('Error updating person:', error)
            setErrorNotificationMessage(`Failed to update ${trimmedName}'s number`)
            setTimeout(() => {
              setErrorNotificationMessage(null)
            }, 5000)
          })
      }
      return
    }

  

    const personObject = {
      name: trimmedName,
      number: newNum,
    }

    create(personObject)
      .then(response => {
        setPersons(persons.concat(response.data))
        setNotificationMessage(`Added ${newName}`)
        setTimeout(() => {
          setNotificationMessage(null)
        }, 5000)
        setNewNum('')
        setNewName('')
      })
      .catch(error => {
        console.error('Error creating person:', error)
        const message =
  error.response?.data?.error || 'Failed to d person'

  setErrorNotificationMessage(message)
        setTimeout(() => {
          setErrorNotificationMessage(null)
        }, 5000)
      })
  }

const deletePerson = (id) => {
  const person = persons.find(i => (i.id ?? i._id) === id)
  console.log(`Attempting to delete person with id: ${id}`)

  if (person && window.confirm(`Delete ${person.name}?`)) {
    remove(id)
      .then(() => {
        console.log(`Deleted person with id ${id}`)
        setPersons(persons.filter(i => (i.id ?? i._id) !== id))
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
      <Notification message={notificationMessage} />

<ErrorNotification message={errorNotificationMessage} />
     
     
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
