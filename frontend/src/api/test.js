import client from './client'

export const testAPI = {
  generate: (data) => client.post('/tests/generate', data),
  submit: (data) => client.post('/tests/submit', data),
  list: () => client.get('/tests'),
}

export const resumeAPI = {
  upload: (file) => {
    const form = new FormData()
    form.append('file', file)
    return client.post('/resume/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  analyze: () => client.post('/resume/analyze'),
  get: () => client.get('/resume'),
}
