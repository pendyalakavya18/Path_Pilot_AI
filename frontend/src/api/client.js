/**
 * client.js — ★ FRONTEND API CONNECTION POINT ★
 *
 * All API calls go through this Axios instance.
 * Set VITE_API_BASE_URL in frontend/.env to point to your backend:
 *
 *   Local dev:   VITE_API_BASE_URL=http://localhost:8000
 *   Production:  VITE_API_BASE_URL=https://your-api.render.com
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || (import.meta.env.PROD ? '/api' : 'http://localhost:8000')

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
})

// ── Request interceptor: attach JWT access token ──────────────────
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ── Response interceptor: auto-refresh on 401 ─────────────────────
client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const res = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          })
          const { access_token, refresh_token } = res.data
          localStorage.setItem('access_token', access_token)
          localStorage.setItem('refresh_token', refresh_token)
          original.headers.Authorization = `Bearer ${access_token}`
          return client(original)
        } catch {
          // Refresh failed — clear tokens and redirect to login
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      } else {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default client
