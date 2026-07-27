import { useState } from 'react' // Make sure you have this import at the top of your file!

const History = (props) => {
  if (props.allClicks.length === 0) {
    const percentage_of_good = (props.good / (props.good + props.neutral + props.bad)) * 100
    return (
      <div>
        <p>No feedback given</p>

          
      </div>
    )
  }

  
}
const StatisticLine = (props) => {
  return (
    console.log(props.text),
    <div>
      <p>{props.value}</p>
    </div>
  )
}

const Button = ({ onClick, text }) => <button onClick={onClick}>{text}</button>
const Statistics = (props) => {
  const total = props.good + props.neutral + props.bad;
  return (
    <div name="statistics">
      <h1>statistics</h1>
      <table>
  <tbody>
    <tr>
      <td>good</td>
      <td><StatisticLine text="good" value={props.good} /></td>
    </tr>
    <tr>
      <td>neutral</td>
      <td><StatisticLine text="neutral" value={props.neutral} /></td>
    </tr>
    <tr>
      <td>bad</td>
      <td><StatisticLine text="bad" value={props.bad} />  </td>
    </tr>
    <tr>
      <td>all</td>
      <td><StatisticLine text="all" value={total} /></td>
    </tr>
    <tr>
      <td>average</td>
      <td><StatisticLine text="average" value={((props.good - props.bad) / total).toFixed(2)} /></td>
    </tr>
    <tr>
      <td>Positive</td>
      <td><StatisticLine text="Positive" value={((props.good / total) * 100).toFixed(2) + '%'} /></td>
    </tr>
  </tbody>
</table>
      
     
      
      
    </div>
  )
}
const App = () => {
  const name = 'Give feedback'
  const [good, setGood] = useState(0)
  const [neutral, setNeutral] = useState(0)
  const [bad, setBad] = useState(0)

  const [allClicks, setAll] = useState([])
  console.log(allClicks);

  const handleLeftClick = () => {
    setAll(allClicks.concat('L'))
    setGood(good + 1)
  }

  const handleRightClick = () => {
    setAll(allClicks.concat('R'))
    setNeutral(neutral + 1)
  }

  const handleBadClick = () => {
    setAll(allClicks.concat('B'))
    setBad(bad + 1)
  }
  if (good + neutral + bad === 0) {
    return (
      <div style={{ right: '10px', margin: '10px' }}>
        <h1>{name}</h1>
        <h1>statistics</h1>
        <Button onClick={handleLeftClick} text='good' />
        <Button onClick={handleRightClick} text='neutral' />
        <Button onClick={handleBadClick} text='bad' />
        <p>No feedback given</p>
      </div>
    )
  }

  return (
    <div style={{ right: '10px', margin: '10px' }}>
      <h1>{name}</h1>
      <Button onClick={handleLeftClick} text='good' />
      <Button onClick={handleRightClick} text='neutral' />
      <Button onClick={handleBadClick} text='bad' />
      
      <Statistics good={good} neutral={neutral} bad={bad} />
      

      
     
    </div>
  )
}
export default App