import client from './client'

export const companiesAPI = {
  list: () => client.get('/companies'),
  getRoles: (company) => client.get(`/companies/${encodeURIComponent(company)}/roles`),
  getRoleSkills: (company, role) => client.get(`/companies/${encodeURIComponent(company)}/roles/${encodeURIComponent(role)}/skills`),
}
