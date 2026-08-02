const Persons = ({ persons, deletePerson }) => {
  return (
    <ul>
      {persons.map(person => (
        <li key={person.id}>
          {person.name} {person.phone}
          <button onClick={() => deletePerson(person.id)}>delete</button>
        </li>
      ))}
    </ul>
  )
}

export default Persons