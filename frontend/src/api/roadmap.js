import client from './client'

export const roadmapAPI = {
  generate: (data) => client.post('/roadmaps/generate', data),
  list: () => client.get('/roadmaps'),
  get: (id) => client.get(`/roadmaps/${id}`),
  updateProgress: (id, data) => client.put(`/roadmaps/${id}/progress`, data),
  adapt: (id) => client.post(`/roadmaps/${id}/adapt`),
  analyzeSkillGap: (data) => client.post('/roadmaps/skill-gap', data),
}

export const companiesAPI = {
  list: () => client.get('/companies'),
  getRoles: (company) => client.get(`/companies/${company}/roles`),
  getSkills: (company, role) => client.get(`/companies/${company}/roles/${role}/skills`),
}

export const progressAPI = {
  getDashboard: () => client.get('/progress'),
}

export const eligibilityAPI = {
  check: (data) => client.post('/eligibility/check', data),
  getSuggestions: () => client.get('/eligibility/suggestions'),
}
