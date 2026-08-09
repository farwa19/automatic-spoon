const PersonForm = ({ onSubmit, nameValue, nameOnChange, numValue, numOnChange }) => {
  return (
    <form onSubmit={onSubmit}>
      <div>
        name:
        <input value={nameValue} onChange={nameOnChange} />
      </div>
      <div>
        number:
        <input value={numValue} onChange={numOnChange} />
      </div>
      <div>
        <button type="submit">save</button>
      </div>
    </form>
  )
} 

export default PersonForm