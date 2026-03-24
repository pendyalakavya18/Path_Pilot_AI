import client from './client'

export const interviewAPI = {
  start: (data) => client.post('/interviews/start', data),
  answer: (id, answer) => client.post(`/interviews/${id}/answer`, { answer }),
  getSummary: (id) => client.get(`/interviews/${id}/summary`),
  list: () => client.get('/interviews'),
}
