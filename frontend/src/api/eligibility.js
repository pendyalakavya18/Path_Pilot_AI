import client from './client'

export const eligibilityAPI = {
  check: (params) => client.post('/eligibility/check', params),
  getSuggestions: () => client.get('/eligibility/suggestions'),
}
