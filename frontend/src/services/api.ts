import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for session cookies
});

export const authService = {
  register: async (data: { username: string; email: string; password: string }) => {
    const response = await api.post('/register', data);
    return response.data;
  },

  login: async (data: { email: string; password: string }) => {
    const response = await api.post('/login', data);
    return response.data;
  },

  logout: async () => {
    const response = await api.post('/logout');
    return response.data;
  },
};

export const profileService = {
  getProfile: async () => {
    const response = await api.get('/profile');
    return response.data;
  },

  updateProfile: async (data: any) => {
    const response = await api.post('/profile', data);
    return response.data;
  },
};

export const jobService = {
  apply: async (jobUrl: string) => {
    const response = await api.post('/apply', { job_url: jobUrl });
    return response.data;
  },
}; 