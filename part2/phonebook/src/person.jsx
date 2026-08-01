const Persons = ({ persons }) => {
  
  return (
    <ul>
      {persons.map(person => (
        <li key={person.id}>
          {person.name} {person.phone}
        </li>
      ))}
    </ul>
  )
}


export default Persons