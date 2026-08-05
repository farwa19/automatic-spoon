import axios from 'axios'

const baseUrl = '/api/persons'

export const getAll = () => {
  console.log('Fetching all persons from backend')
  return axios.get(baseUrl)
}

export const create = newObject => {
  console.log('Creating new person:', newObject)
  return axios.post(baseUrl, newObject)
}

export const remove = id => {
  return axios.delete(`${baseUrl}/${id}`)
}
export const update = (id, newObject) => {
  return axios.put(`${baseUrl}/${id}`, newObject)
}