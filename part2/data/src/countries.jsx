const baseUrl = 'https://studies.cs.helsinki.fi/restcountries/api/all'

const getAll = () => {
    console.log('Fetching countries from API:', baseUrl)
    const countries = fetch(baseUrl)
        .then(response => response.json())
        .then(data => {
            console.log('Fetched countries data:', data)
            return data
        })
        .catch(error => {
            console.error('Error fetching countries:', error)
            throw error
        })
    return countries
}
export default getAll



