const Persons = ({ persons, deletePerson }) => {
  return (
    <ul>
      {persons.map(person => {
        const personId = person.id ?? person._id

        return (
          <li key={personId}>
            {person.name} {person.number}
            <button onClick={() => deletePerson(personId)}>delete</button>
          </li>
        )
      })}
    </ul>
  )
}

export default Persons