import { useState, useEffect, useRef } from 'react'
import { toast } from 'react-hot-toast'
import { authAPI } from '../api/auth'
import { resumeAPI } from '../api/resume'
import useAuthStore from '../stores/authStore'
import { UploadCloud, Plus, X, Save } from 'lucide-react'

const BRANCHES = ['CS', 'IT', 'ECE', 'EEE', 'Mechanical', 'Civil', 'Chemical', 'Other']
const PROFICIENCY = ['beginner', 'intermediate', 'advanced']

export default function Profile() {
  const { user, updateUser } = useAuthStore()
  const [profile, setProfile] = useState({ name: '', cgpa: '', branch: '', graduation_year: '', experience_years: '', target_company: '', target_role: '' })
  const [skills, setSkills] = useState([])   // [{name, proficiency}]
  const [newSkill, setNewSkill] = useState({ name: '', proficiency: 'beginner' })
  const [saving, setSaving] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [resumeSkills, setResumeSkills] = useState([])
  const fileRef = useRef(null)

  useEffect(() => {
    if (!user) return
    setProfile({
      name: user?.name || '',
      cgpa: user?.cgpa || '',
      branch: user?.branch || '',
      graduation_year: user?.graduation_year || '',
      experience_years: user?.experience_years || '',
      target_company: user?.target_company || '',
      target_role: user?.target_role || '',
    })
    setSkills(user?.skills || [])
  }, [user])

  const saveProfile = async () => {
    setSaving(true)
    try {
      const res = await authAPI.updateProfile(profile)
      updateUser(res.data)
      toast.success('Profile saved!')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save profile')
    } finally {
      setSaving(false)
    }
  }

  const saveSkills = async () => {
    setSaving(true)
    try {
      const res = await authAPI.updateSkills(skills)
      updateUser(res.data)
      toast.success('Skills updated!')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to update skills')
    } finally {
      setSaving(false)
    }
  }

  const addSkill = () => {
    if (!newSkill.name.trim()) return
    if (skills.find((s) => s.skill_name.toLowerCase() === newSkill.name.toLowerCase())) {
      toast.error('Skill already added')
      return
    }
    setSkills([...skills, { skill_name: newSkill.name.trim(), proficiency: newSkill.proficiency }])
    setNewSkill({ name: '', proficiency: 'beginner' })
  }

  const removeSkill = (name) => setSkills(skills.filter((s) => s.skill_name !== name))

  const handleResume = async (file) => {
    if (!file) return
    setUploading(true)
    try {
      const uploadRes = await resumeAPI.upload(file)
      const analyzeRes = await resumeAPI.analyze(uploadRes.data.resume_id)
      setResumeSkills(analyzeRes.data.skills ?? [])
      toast.success('Resume analyzed!')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Resume analysis failed')
    } finally {
      setUploading(false)
    }
  }

  const addFromResume = (skillName) => {
    if (skills.find((s) => s.skill_name.toLowerCase() === skillName.toLowerCase())) return
    setSkills([...skills, { skill_name: skillName, proficiency: 'beginner' }])
  }

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-8">
      <h1 className="text-2xl font-bold text-gray-100">My Profile</h1>

      {/* Profile details */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-200 mb-5">Personal Details</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            { key: 'name', label: 'Full Name', type: 'text', placeholder: 'Your name' },
            { key: 'cgpa', label: 'CGPA', type: 'number', placeholder: '8.5' },
            { key: 'graduation_year', label: 'Graduation Year', type: 'number', placeholder: '2025' },
            { key: 'experience_years', label: 'Experience (years)', type: 'number', placeholder: '0' },
            { key: 'target_company', label: 'Target Company', type: 'text', placeholder: 'Google' },
            { key: 'target_role', label: 'Target Role', type: 'text', placeholder: 'Software Engineer' },
          ].map(({ key, label, type, placeholder }) => (
            <div key={key}>
              <label className="label">{label}</label>
              <input className="input" type={type} placeholder={placeholder} value={profile[key]} onChange={(e) => setProfile({ ...profile, [key]: e.target.value })} />
            </div>
          ))}
          <div>
            <label className="label">Branch</label>
            <select className="input" value={profile.branch} onChange={(e) => setProfile({ ...profile, branch: e.target.value })}>
              <option value="">Select branch</option>
              {BRANCHES.map((b) => <option key={b} value={b}>{b}</option>)}
            </select>
          </div>
        </div>
        <button className="btn-primary mt-5 flex items-center gap-2" onClick={saveProfile} disabled={saving}>
          <Save size={16} />
          {saving ? 'Saving…' : 'Save Profile'}
        </button>
      </div>

      {/* Skills */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-200 mb-5">Skills</h2>
        <div className="flex flex-wrap gap-2 mb-4 min-h-[2rem]">
          {skills.map((s) => (
            <span key={s.skill_name} className="flex items-center gap-1.5 px-3 py-1 rounded-full text-sm bg-indigo-950/50 border border-indigo-800/50 text-indigo-300">
              {s.skill_name}
              <span className="text-xs text-indigo-500">{s.proficiency}</span>
              <button onClick={() => removeSkill(s.skill_name)} className="text-indigo-400 hover:text-red-400 transition-colors ml-1"><X size={12} /></button>
            </span>
          ))}
          {!skills.length && <p className="text-sm text-gray-500">No skills added yet</p>}
        </div>
        <div className="flex gap-3 mb-4">
          <input className="input flex-1" placeholder="Add skill (e.g. Python)" value={newSkill.name} onChange={(e) => setNewSkill({ ...newSkill, name: e.target.value })} onKeyDown={(e) => e.key === 'Enter' && addSkill()} />
          <select className="input w-44" value={newSkill.proficiency} onChange={(e) => setNewSkill({ ...newSkill, proficiency: e.target.value })}>
            {PROFICIENCY.map((p) => <option key={p} value={p}>{p}</option>)}
          </select>
          <button className="btn-secondary flex items-center gap-1" onClick={addSkill}><Plus size={16} /> Add</button>
        </div>
        <button className="btn-primary flex items-center gap-2" onClick={saveSkills} disabled={saving}>
          <Save size={16} />
          {saving ? 'Saving…' : 'Save Skills'}
        </button>
      </div>

      {/* Resume upload */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-200 mb-5">Resume</h2>
        <input ref={fileRef} type="file" accept=".pdf,.docx" className="hidden" onChange={(e) => handleResume(e.target.files[0])} />
        <button
          className="w-full border-2 border-dashed border-gray-700 rounded-xl p-8 flex flex-col items-center gap-3 hover:border-gray-600 transition-colors cursor-pointer bg-transparent"
          onClick={() => fileRef.current?.click()}
        >
          {uploading ? (
            <span className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full" />
          ) : (
            <>
              <UploadCloud size={36} className="text-gray-500" />
              <p className="text-gray-300">Click to upload PDF or DOCX</p>
              <p className="text-sm text-gray-500">Skills will be extracted automatically</p>
            </>
          )}
        </button>
        {resumeSkills.length > 0 && (
          <div className="mt-4">
            <p className="text-sm text-gray-400 mb-2">Extracted skills — click to add to your profile:</p>
            <div className="flex flex-wrap gap-2">
              {resumeSkills.map((s) => {
                const added = skills.some((sk) => sk.skill_name.toLowerCase() === s.toLowerCase())
                return (
                  <button key={s} onClick={() => !added && addFromResume(s)} disabled={added}
                    className={`text-xs px-3 py-1 rounded-full border transition-colors ${added ? 'border-green-800/40 bg-green-950/30 text-green-500 cursor-default' : 'border-gray-700 text-gray-300 hover:border-indigo-600 hover:text-indigo-300'}`}>
                    {added ? `✓ ${s}` : `+ ${s}`}
                  </button>
                )
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
