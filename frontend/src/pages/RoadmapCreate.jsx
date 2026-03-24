import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { toast } from 'react-hot-toast'
import { roadmapAPI, companiesAPI } from '../api/roadmap'
import useAuthStore from '../stores/authStore'

export default function RoadmapCreate() {
  const user = useAuthStore((s) => s.user)
  const navigate = useNavigate()

  const [companies, setCompanies] = useState([])
  const [roles, setRoles] = useState([])
  const [form, setForm] = useState({
    company: user?.target_company || '',
    role: user?.target_role || '',
    weeks: 12,
    skills: '',
  })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    companiesAPI.list().then((res) => setCompanies(res.data))
  }, [])

  useEffect(() => {
    if (form.company && form.company.length > 1) {
      companiesAPI.getRoles(form.company).then((res) => setRoles(res.data.roles || [])).catch(() => setRoles([]))
    } else {
      setRoles([])
    }
  }, [form.company])

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const skillsArray = form.skills
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean)

      const res = await roadmapAPI.generate({
        company: form.company,
        role: form.role,
        weeks: parseInt(form.weeks),
        current_skills: skillsArray,
      })
      toast.success('Roadmap generated!')
      navigate(`/roadmap/${res.data.id}`)
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to generate roadmap')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-100 mb-2">Generate Your Roadmap</h1>
      <p className="text-gray-400 mb-8">AI will create a personalized week-by-week preparation plan.</p>

      <div className="card">
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="label">Target Company</label>
            <input
              name="company"
              className="input"
              list="companies-list"
              placeholder="e.g. Google, Amazon, Infosys…"
              value={form.company}
              onChange={handleChange}
              required
              autoComplete="off"
            />
            <datalist id="companies-list">
              {companies.map((c) => <option key={c.name} value={c.name} />)}
            </datalist>
          </div>

          <div>
            <label className="label">Target Role</label>
            <input
              name="role"
              className="input"
              list="roles-list"
              placeholder="e.g. Software Engineer, Data Scientist…"
              value={form.role}
              onChange={handleChange}
              required
              autoComplete="off"
            />
            <datalist id="roles-list">
              {roles.map((r) => <option key={r} value={r} />)}
            </datalist>
          </div>

          <div>
            <label className="label">Preparation Time (weeks)</label>
            <input
              type="range"
              name="weeks"
              min="4"
              max="24"
              value={form.weeks}
              onChange={handleChange}
              className="w-full accent-indigo-500"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>4 weeks</span>
              <span className="font-semibold text-indigo-400">{form.weeks} weeks selected</span>
              <span>24 weeks</span>
            </div>
          </div>

          <div>
            <label className="label">
              Current Skills <span className="text-gray-600 font-normal">(comma-separated)</span>
            </label>
            <input
              name="skills"
              className="input"
              placeholder="Python, SQL, React"
              value={form.skills}
              onChange={handleChange}
            />
            <p className="text-xs text-gray-600 mt-1">Leave blank to use skills from your profile</p>
          </div>

          <button type="submit" className="btn-primary w-full" disabled={loading}>
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full" />
                Generating roadmap with AI…
              </span>
            ) : (
              'Generate Roadmap'
            )}
          </button>
        </form>
      </div>
    </div>
  )
}
