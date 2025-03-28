import axios from 'axios'

// Create a configured axios instance
const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add request interceptor
api.interceptors.request.use(
  config => {
    // You can add authentication tokens or other request modifications here
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Add response interceptor
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error)
    if (error.response) {
      // Error with server response
      console.error('Status:', error.response.status)
      console.error('Data:', error.response.data)
    } else if (error.request) {
      // Error with no response
      console.error('Request failed, no response received')
    } else {
      // Error setting up request
      console.error('Error setting up request:', error.message)
    }
    return Promise.reject(error)
  }
)

export default api
