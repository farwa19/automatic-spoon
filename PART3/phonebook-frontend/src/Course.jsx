

const Header = (props) => {
  
  return <h1>{props.course.name}</h1>
}

const Part = (props) => {
    console.log(props)
  return (
    <p>
      {props.part} {props.exercises}
    </p>
  )
}

const Content = (props) => {
    console.log(props)
    console.log(":")
  
  return (
    
    <div>

      {props.course.parts.map(part => (
        
        <Part key={part.id} part={part.name} exercises={part.exercises} />
      ))}   
       
    
    </div>
  )
}



const Total = (props) => {
  const total = props.course.parts.reduce((s, p) => {
    return s + p.exercises
  }, 0)
  return (
    <p>Number of exercises {total}</p>
  )
}



const Course = (probs) => {
  return (
    <div>
      
      <Header course={probs.course} />
      <Content course={probs.course} />
      <Total course={probs.course} />
      </div>
  )}  
  

export default Course;