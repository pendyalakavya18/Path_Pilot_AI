import client from './client'

export const authAPI = {
  register: (data) => client.post('/auth/register', data),
  login: (data) => client.post('/auth/login', data),
  refresh: (refreshToken) => client.post('/auth/refresh', { refresh_token: refreshToken }),

  getMe: () => client.get('/users/me'),
  updateProfile: (data) => client.put('/users/me', data),
  updateSkills: (skills) => client.put('/users/me/skills', { skills }),
}
