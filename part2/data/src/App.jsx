import { useState, useEffect } from 'react'
const apiKey = import.meta.env.VITE_WEATHER_API_KEY
import axios from 'axios'
import getAll from './countries'

const App = () => {
  const [countries, setCountries] = useState([])
  const [search, setSearch] = useState('')
  const [weather, setWeather] = useState(null)

  useEffect(() => {
    getAll().then(data => {
      setCountries(data)
      console.log('effect')
    })
  }, [])

  const handleSearchChange = (event) => {
    setSearch(event.target.value)
  }

  const moreinfo = (name) => {
    const country = countries.find(country => country.name.common === name)
    console.log('moreinfo country:', country)
    if (country) {
      setSearch(country.name.common)
    }
  }

  const filteredCountries = countries.filter(country =>
    country.name.common.toLowerCase().includes(search.toLowerCase())
  )

  useEffect(() => {
    if (filteredCountries.length === 1) {
      const country = filteredCountries[0]

      if (country.capitalInfo?.latlng) {
        const [lat, lon] = country.capitalInfo.latlng

        axios
          .get(
            `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=metric`
          )
          .then(response => {
            setWeather({
              temperature: response.data.main.temp,
              windSpeed: response.data.wind.speed,
              icon: `https://openweathermap.org/img/wn/${response.data.weather[0].icon}@2x.png`
            })
            console.log('Weather data:', response.data)
          })
      }
    }
  }, [filteredCountries])

  console.log('check', search.length)

  if (search.length === 0) {
    return (
      <div>
        <h1>Countries</h1>
        input field for searching countries
        <input value={search} onChange={handleSearchChange} />
      </div>
    )
  }

  if (filteredCountries.length === 0) {
    return (
      <div>
        <h1>Countries</h1>
        input field for searching countries
        <input value={search} onChange={handleSearchChange} />
        <p>No matches found</p>
      </div>
    )
  }

  if (filteredCountries.length > 10) {
    console.log('here')
    return (
      <div>
        <h1>Countries</h1>
        input field for searching countries
        <input value={search} onChange={handleSearchChange} />
        <p>Too many matches, specify another filter</p>
      </div>
    )
  }

  if (filteredCountries.length === 1) {
    const country = filteredCountries[0]
    console.log('country:', country)

    return (
      <div>
        <h1>Countries</h1>
        input field for searching countries
        <input value={search} onChange={handleSearchChange} />
        <h2>{country.name.common}</h2>
        <p>Capital: {country.capital}</p>
        <p>area: {country.area}</p>
        <img src={country.flags.png} alt={`Flag of ${country.name.common}`} />
        <h1> Languages</h1>
        <ul>
          {Object.values(country.languages).map(language => (
            <li key={language}>{language}</li>
          ))}
        </ul>
        <h1>Weather in {country.capital}</h1>
        <p>Temperature: {weather?.temperature} °C</p>
        <p>Wind: {weather?.windSpeed} m/s</p>
        <img src={weather?.icon} alt={`Weather icon for ${country.capital}`} />
      </div>
    )
  }

  console.log('filteredCountries', filteredCountries.map(country => country.name.common))
  console.log('search', search)

  return (
    <div>
      <h1>Countries</h1>
      input field for searching countries
      <input value={search} onChange={handleSearchChange} />
      <ul>
        {filteredCountries.map(country => (
          <li key={country.name.common}>
            {country.name.common}
            <button onClick={() => moreinfo(country.name.common)}>show details</button>
          </li>
        ))}
      </ul>
    </div>
  )
}
   
  


export default App



