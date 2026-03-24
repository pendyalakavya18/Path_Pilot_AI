import client from './client'

export const resumeAPI = {
  upload: (file) => {
    const form = new FormData()
    form.append('file', file)
    return client.post('/resume/upload', form, { headers: { 'Content-Type': 'multipart/form-data' } })
  },
  analyze: (resumeId) => client.post('/resume/analyze', { resume_id: resumeId }),
  get: () => client.get('/resume'),
}
