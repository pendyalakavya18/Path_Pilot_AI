import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { RadialBarChart, RadialBar, ResponsiveContainer, Tooltip, LineChart, Line, XAxis, YAxis, CartesianGrid } from 'recharts'
import { progressAPI, roadmapAPI } from '../api/roadmap'
import useAuthStore from '../stores/authStore'
import { MapPin, Brain, FileText, Zap, TrendingUp, Award } from 'lucide-react'

export default function Dashboard() {
  const user = useAuthStore((s) => s.user)
  const [progress, setProgress] = useState(null)
  const [roadmaps, setRoadmaps] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([progressAPI.getDashboard(), roadmapAPI.list()])
      .then(([pRes, rRes]) => {
        setProgress(pRes.data)
        setRoadmaps(rRes.data.slice(0, 3))
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center h-full">
        <div className="text-gray-400 animate-pulse">Loading dashboard…</div>
      </div>
    )
  }

  const readinessColor = {
    'Highly Ready': 'text-green-400',
    Ready: 'text-emerald-400',
    'Moderately Ready': 'text-yellow-400',
    'Not Ready': 'text-red-400',
  }

  return (
    <div className="p-8 max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-100">
          Welcome back, {user?.name?.split(' ')[0]} 👋
        </h1>
        <p className="text-gray-400 mt-1">
          {user?.target_company
            ? `Preparing for ${user.target_company} — ${user.target_role}`
            : 'Set your target company and role in your profile'}
        </p>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard
          label="Roadmap Progress"
          value={`${progress?.roadmap_progress_percent ?? 0}%`}
          icon={MapPin}
          color="text-indigo-400"
        />
        <StatCard
          label="Avg Test Score"
          value={`${progress?.avg_test_score ?? 0}%`}
          icon={FileText}
          color="text-blue-400"
        />
        <StatCard
          label="Avg Interview"
          value={`${progress?.avg_interview_score ?? 0}/10`}
          icon={Brain}
          color="text-purple-400"
        />
        <div className="card flex flex-col items-center justify-center">
          <span className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Readiness</span>
          <span className={`text-xl font-bold ${readinessColor[progress?.readiness_label] ?? 'text-gray-300'}`}>
            {progress?.readiness_label ?? 'Not Ready'}
          </span>
          <span className="text-2xl font-bold text-gray-100 mt-1">
            {progress?.overall_readiness_score ?? 0}
            <span className="text-sm text-gray-500">/10</span>
          </span>
        </div>
      </div>

      {/* Progress Graphs */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-8">
        <div className="card flex flex-col">
          <h3 className="text-sm font-semibold text-gray-200 mb-4 uppercase tracking-wider">Test Score History</h3>
          <div className="h-64 mt-auto">
            {progress?.test_history?.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={progress.test_history}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                  <XAxis dataKey="date" stroke="#9ca3af" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#9ca3af" fontSize={12} tickLine={false} axisLine={false} domain={[0, 100]} />
                  <Tooltip contentStyle={{ backgroundColor: '#1f2937', borderColor: '#374151', color: '#f3f4f6' }} />
                  <Line type="monotone" dataKey="score" stroke="#60a5fa" strokeWidth={3} dot={{ r: 4, fill: '#60a5fa' }} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-sm text-gray-500">No practice tests taken yet.</div>
            )}
          </div>
        </div>

        <div className="card flex flex-col">
          <h3 className="text-sm font-semibold text-gray-200 mb-4 uppercase tracking-wider">Interview Score History</h3>
          <div className="h-64 mt-auto">
            {progress?.interview_history?.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={progress.interview_history}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                  <XAxis dataKey="date" stroke="#9ca3af" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#9ca3af" fontSize={12} tickLine={false} axisLine={false} domain={[0, 10]} />
                  <Tooltip contentStyle={{ backgroundColor: '#1f2937', borderColor: '#374151', color: '#f3f4f6' }} />
                  <Line type="monotone" dataKey="score" stroke="#c084fc" strokeWidth={3} dot={{ r: 4, fill: '#c084fc' }} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-sm text-gray-500">No interviews completed yet.</div>
            )}
          </div>
        </div>
      </div>

      {/* Quick actions */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <QuickAction to="/roadmap/create" icon={MapPin} label="New Roadmap" desc="Generate AI roadmap" color="bg-indigo-600/20 border-indigo-600/30" />
        <QuickAction to="/skill-gap" icon={Zap} label="Skill Gap" desc="Analyze your gaps" color="bg-blue-600/20 border-blue-600/30" />
        <QuickAction to="/test" icon={FileText} label="Practice Test" desc="Topic-specific MCQs" color="bg-purple-600/20 border-purple-600/30" />
        <QuickAction to="/interview" icon={Brain} label="Mock Interview" desc="AI interview agent" color="bg-green-600/20 border-green-600/30" />
      </div>

      {/* Active roadmaps */}
      {roadmaps.length > 0 && (
        <div>
          <h2 className="text-lg font-semibold text-gray-200 mb-4">Your Roadmaps</h2>
          <div className="space-y-3">
            {roadmaps.map((r) => (
              <Link
                key={r.id}
                to={`/roadmap/${r.id}`}
                className="card flex items-center justify-between hover:border-indigo-700 transition-colors"
              >
                <div>
                  <p className="font-medium text-gray-100">{r.company} — {r.role}</p>
                  <p className="text-sm text-gray-400">{r.total_weeks} weeks · Week {r.current_week} of {r.total_weeks}</p>
                </div>
                <div className="text-right">
                  <span className={`text-xs px-2 py-1 rounded-full ${r.status === 'active' ? 'bg-green-900 text-green-300' : 'bg-gray-800 text-gray-400'}`}>
                    {r.status}
                  </span>
                  <div className="w-24 bg-gray-800 rounded-full h-1.5 mt-2">
                    <div
                      className="bg-indigo-500 h-1.5 rounded-full"
                      style={{ width: `${(r.current_week / r.total_weeks) * 100}%` }}
                    />
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function StatCard({ label, value, icon: Icon, color }) {
  return (
    <div className="card">
      <div className="flex items-center gap-3 mb-2">
        <Icon size={18} className={color} />
        <span className="text-xs text-gray-500 uppercase tracking-wider">{label}</span>
      </div>
      <p className={`text-2xl font-bold ${color}`}>{value}</p>
    </div>
  )
}

function QuickAction({ to, icon: Icon, label, desc, color }) {
  return (
    <Link to={to} className={`card border ${color} hover:opacity-90 transition-opacity`}>
      <Icon size={22} className="text-gray-300 mb-3" />
      <p className="font-semibold text-gray-100 text-sm">{label}</p>
      <p className="text-xs text-gray-500 mt-0.5">{desc}</p>
    </Link>
  )
}
