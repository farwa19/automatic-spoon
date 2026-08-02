import axios from 'axios'

const baseUrl = 'https://special-space-journey-pj7jq7qxjwrqc9w4v-3001.app.github.dev/persons'

export const getAll = () => {
  return axios.get(baseUrl)
}

export const create = newObject => {
  return axios.post(baseUrl, newObject)
}

export const remove = id => {
  return axios.delete(`${baseUrl}/${id}`)
}
export const update = (id, newObject) => {
  return axios.put(`${baseUrl}/${id}`, newObject)
}