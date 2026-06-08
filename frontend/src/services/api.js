import axios from 'axios';

const api = axios.create({
  baseURL: '', // Dev proxy routes to Flask port 5000, production uses relative path
  withCredentials: true, // Crucial for session cookies
});

// Response interceptor to handle unauthenticated/unauthorized responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      // Clear cookie or just redirect back to Flask login page
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
