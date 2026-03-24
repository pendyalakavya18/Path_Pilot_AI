import { useState, useEffect, useRef } from 'react'
import { toast } from 'react-hot-toast'
import { roadmapAPI } from '../api/roadmap'
import { eligibilityAPI } from '../api/eligibility'
import { resumeAPI } from '../api/resume'
import { companiesAPI } from '../api/companies'
import { UploadCloud, CheckCircle, XCircle, Globe } from 'lucide-react'

export default function SkillGap() {
  const [companies, setCompanies] = useState([])
  const [roles, setRoles] = useState([])
  const [form, setForm] = useState({ company: '', role: '', userSkills: '' })
  const [loading, setLoading] = useState(false)
  const [analysis, setAnalysis] = useState(null)
  const [eligibility, setEligibility] = useState(null)
  const [dragOver, setDragOver] = useState(false)
  const [uploading, setUploading] = useState(false)
  const fileRef = useRef(null)

  useEffect(() => {
    companiesAPI.list().then((r) => setCompanies(r.data)).catch(() => {})
  }, [])

  useEffect(() => {
    if (!form.company) { setRoles([]); setForm((p) => ({ ...p, role: '' })); return }
    companiesAPI.getRoles(form.company).then((r) => setRoles(r.data.roles || [])).catch(() => {})
  }, [form.company])

  const handleFile = async (file) => {
    if (!file) return
    setUploading(true)
    try {
      const uploadRes = await resumeAPI.upload(file)
      const analyzeRes = await resumeAPI.analyze(uploadRes.data.resume_id)
      const skills = analyzeRes.data.skills?.join(', ') ?? ''
      setForm((p) => ({ ...p, userSkills: skills }))
      toast.success('Resume analyzed — skills extracted!')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Resume analysis failed')
    } finally {
      setUploading(false)
    }
  }

  const analyze = async () => {
    if (!form.company || !form.role) { toast.error('Select company and role'); return }
    setLoading(true)
    setAnalysis(null)
    setEligibility(null)
    try {
      const skillList = form.userSkills.split(',').map((s) => s.trim()).filter(Boolean)
      const [gapRes, eligRes] = await Promise.all([
        roadmapAPI.analyzeSkillGap({ company: form.company, role: form.role, user_skills: skillList }),
        eligibilityAPI.check({ company: form.company }),
      ])
      setAnalysis(gapRes.data)
      setEligibility(eligRes.data)
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Analysis failed')
    } finally {
      setLoading(false)
    }
  }

  const onDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    const file = e.dataTransfer.files[0]
    if (file) handleFile(file)
  }

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-100 mb-2">Skill Gap Analysis</h1>
      <p className="text-gray-400 mb-8">Discover what skills you need for your target company and role.</p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Form */}
        <div className="card space-y-4">
          <div>
            <label className="label">Target Company</label>
            <input
              className="input" list="sg-companies-list"
              placeholder="e.g. Google, TCS, Infosys…"
              value={form.company}
              onChange={(e) => setForm({ ...form, company: e.target.value })}
              autoComplete="off"
            />
            <datalist id="sg-companies-list">
              {companies.map((c) => <option key={c.name} value={c.name} />)}
            </datalist>
          </div>
          <div>
            <label className="label">Target Role</label>
            <input
              className="input" list="sg-roles-list"
              placeholder="e.g. Software Engineer, Data Scientist…"
              value={form.role}
              onChange={(e) => setForm({ ...form, role: e.target.value })}
              autoComplete="off"
            />
            <datalist id="sg-roles-list">
              {roles.map((r) => <option key={r} value={r} />)}
            </datalist>
          </div>
          <div>
            <label className="label">Your Current Skills <span className="text-gray-500 text-xs">(comma-separated or upload resume)</span></label>
            <textarea className="input resize-none h-24" placeholder="Python, SQL, Machine Learning, …" value={form.userSkills} onChange={(e) => setForm({ ...form, userSkills: e.target.value })} />
          </div>
          <button className="btn-primary w-full" onClick={analyze} disabled={loading}>
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full" />
                Analyzing…
              </span>
            ) : 'Analyze Gap'}
          </button>
        </div>

        {/* Resume upload */}
        <div
          className={`card flex flex-col items-center justify-center cursor-pointer border-2 border-dashed transition-colors ${dragOver ? 'border-indigo-500 bg-indigo-950/20' : 'border-gray-700 hover:border-gray-600'}`}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
          onDragLeave={() => setDragOver(false)}
          onDrop={onDrop}
          onClick={() => fileRef.current?.click()}
        >
          <input ref={fileRef} type="file" accept=".pdf,.docx" className="hidden" onChange={(e) => handleFile(e.target.files[0])} />
          {uploading ? (
            <span className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full" />
          ) : (
            <>
              <UploadCloud size={40} className="text-gray-500 mb-3" />
              <p className="text-gray-300 font-medium">Upload Resume</p>
              <p className="text-sm text-gray-500 mt-1">PDF or DOCX — auto-extracts skills</p>
            </>
          )}
        </div>
      </div>

      {/* Results */}
      {analysis && (
        <div className="space-y-6">
          {/* Match score */}
          <div className="card flex items-center gap-6 relative overflow-hidden">
            <div className="absolute top-0 right-0 bg-indigo-500/10 border-b border-l border-indigo-500/20 px-3 py-1.5 rounded-bl-xl flex items-center gap-1.5">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
              </span>
              <Globe size={12} className="text-indigo-400" />
              <span className="text-[10px] text-indigo-300 font-bold uppercase tracking-wider">Live Web Insights</span>
            </div>
            
            <div className="text-center shrink-0">
              <p className={`text-5xl font-bold ${analysis.match_score >= 70 ? 'text-green-400' : analysis.match_score >= 40 ? 'text-yellow-400' : 'text-red-400'}`}>
                {analysis.match_score}%
              </p>
              <p className="text-sm text-gray-400 mt-1">Match Score</p>
            </div>
            <div className="flex-1 min-w-0">
              <div className="w-full bg-gray-800 rounded-full h-3">
                <div className={`h-3 rounded-full transition-all ${analysis.match_score >= 70 ? 'bg-green-500' : analysis.match_score >= 40 ? 'bg-yellow-500' : 'bg-red-500'}`} style={{ width: `${analysis.match_score}%` }} />
              </div>
              <p className="text-sm text-gray-400 mt-2">{form.company} — {form.role}</p>
            </div>
          </div>

          {/* Eligibility */}
          {eligibility && (
            <div className={`card border ${eligibility.eligible ? 'border-green-800/60' : 'border-red-800/60'}`}>
              <div className="flex items-center gap-3 mb-2">
                {eligibility.eligible ? <CheckCircle size={20} className="text-green-400" /> : <XCircle size={20} className="text-red-400" />}
                <h3 className="font-semibold text-gray-200">Company Eligibility</h3>
              </div>
              <p className="text-sm text-gray-400">{eligibility.message}</p>
              {eligibility.gaps?.length > 0 && (
                <ul className="mt-2 space-y-1">{eligibility.gaps.map((g, i) => <li key={i} className="text-xs text-red-400">• {g}</li>)}</ul>
              )}
            </div>
          )}

          {/* Skill gap */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <h3 className="font-semibold text-gray-200 mb-3">Missing Skills</h3>
              <div className="space-y-2">
                {analysis.missing_skills?.map((s, idx) => {
                  const skillName = s.skill || s.name || 'Unknown Skill';
                  return (
                    <div key={idx} className="flex items-center justify-between">
                      <span className="text-sm text-gray-300">{skillName}</span>
                      <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${s.priority === 'HIGH' ? 'badge-high' : s.priority === 'MEDIUM' ? 'badge-medium' : 'badge-low'}`}>
                        {s.priority || 'LOW'}
                      </span>
                    </div>
                  )
                })}
                {!analysis.missing_skills?.length && <p className="text-sm text-gray-500">No missing skills 🎉</p>}
              </div>
            </div>
            <div className="card">
              <h3 className="font-semibold text-gray-200 mb-3">Skills You Have</h3>
              <div className="flex flex-wrap gap-2">
                {analysis.existing_skills?.map((s) => (
                  <span key={s} className="text-xs px-2 py-1 bg-green-950/40 border border-green-800/40 text-green-300 rounded-full">{s}</span>
                ))}
                {!analysis.existing_skills?.length && <p className="text-sm text-gray-500">None matched yet</p>}
              </div>
            </div>
          </div>

          {/* Recommendations */}
          {analysis.recommendations?.length > 0 && (
            <div className="card">
              <h3 className="font-semibold text-gray-200 mb-3">Recommendations</h3>
              <ul className="space-y-2">
                {analysis.recommendations.map((r, i) => (
                  <li key={i} className="text-sm text-gray-400 flex gap-2">
                    <span className="text-indigo-400 shrink-0">→</span>{r}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
