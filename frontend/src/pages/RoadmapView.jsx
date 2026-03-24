import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { toast } from 'react-hot-toast'
import { roadmapAPI } from '../api/roadmap'
import { CheckCircle2, Circle, ChevronDown, ChevronUp, Zap, ExternalLink, PlaySquare, Video, Lock, Globe } from 'lucide-react'

export default function RoadmapView() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [roadmap, setRoadmap] = useState(null)
  const [loading, setLoading] = useState(true)
  const [expanded, setExpanded] = useState({})
  const [adapting, setAdapting] = useState(false)

  useEffect(() => {
    roadmapAPI.get(id).then((res) => {
      setRoadmap(res.data)
      if (res.data.weekly_plan?.length > 0) {
        setExpanded({ [res.data.weekly_plan[0].week]: true })
      }
    }).finally(() => setLoading(false))
  }, [id])

  const getAllDays = () => {
    if (!roadmap?.weekly_plan) return []
    const allDays = []
    roadmap.weekly_plan.forEach(w => {
      const days = w.days || []
      days.forEach(d => {
        allDays.push({ weekNum: w.week, ...d })
      })
    })
    return allDays
  }

  const toggleTopic = async (weekNum, topic, currentState) => {
    try {
      await roadmapAPI.updateProgress(id, {
        week_number: weekNum,
        topic,
        completed: !currentState,
      })
      setRoadmap((prev) => ({
        ...prev,
        weekly_plan: prev.weekly_plan.map((w) =>
          w.week === weekNum
            ? {
                ...w,
                days: w.days?.map((d) =>
                  d.topic === topic ? { ...d, _completed: !currentState } : d
                ),
              }
            : w
        ),
      }))
    } catch {
      toast.error('Failed to update progress')
    }
  }

  const handleAdapt = async () => {
    setAdapting(true)
    try {
      await roadmapAPI.adapt(id)
      const res = await roadmapAPI.get(id)
      setRoadmap(res.data)
      toast.success('Roadmap adapted to your current progress!')
    } catch {
      toast.error('Adaptation failed')
    } finally {
      setAdapting(false)
    }
  }

  if (loading) return <div className="p-8 text-gray-400 animate-pulse flex items-center justify-center min-h-[50vh]">Loading roadmap…</div>
  if (!roadmap) return <div className="p-8 text-red-400 flex items-center justify-center min-h-[50vh]">Roadmap not found</div>

  const plan = roadmap.weekly_plan || []
  const gap = roadmap.skill_gap || {}
  const allDays = getAllDays()

  return (
    <div className="p-8 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-start justify-between mb-8 bg-gray-800/50 p-6 rounded-2xl border border-gray-700/50 shadow-lg">
        <div>
          <div className="flex items-center gap-3 flex-wrap">
            <h1 className="text-3xl font-extrabold bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent">
              {roadmap.company} — {roadmap.role}
            </h1>
            <div className="flex items-center gap-1.5 bg-cyan-950/40 border border-cyan-800/50 px-3 py-1 rounded-full shadow-inner mt-1 md:mt-0">
               <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
               </span>
               <Globe size={12} className="text-cyan-400" />
               <span className="text-[10px] uppercase tracking-widest text-cyan-300 font-bold">Live AI Context</span>
            </div>
          </div>
          <p className="text-gray-400 mt-2 font-medium">{roadmap.total_weeks}-week preparation plan</p>
        </div>
        <button
          onClick={handleAdapt}
          disabled={adapting}
          className="btn-secondary flex items-center gap-2 text-sm px-4 py-2 hover:bg-indigo-600/20"
        >
          <Zap size={16} className={adapting ? 'animate-pulse' : ''} />
          {adapting ? 'Adapting…' : 'Smart Adapt'}
        </button>
      </div>

      {/* Skill gap summary */}
      {gap.missing_skills?.length > 0 && (
        <div className="card mb-8 border border-yellow-800/50 bg-yellow-900/10 shadow-lg shadow-yellow-900/5">
          <h3 className="font-semibold text-yellow-500 mb-4 flex items-center gap-2">
            <Zap size={18} /> Skill Gap Analysis
          </h3>
          <div className="flex flex-wrap gap-2">
            {gap.missing_skills.map((s, idx) => (
              <span
                key={idx}
                className={s.priority === 'HIGH' ? 'badge-high shadow-sm shadow-red-900/20' : 'badge-medium shadow-sm shadow-yellow-900/20'}
              >
                {s.skill || s} · {s.priority || 'MEDIUM'}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Weekly plan */}
      <div className="space-y-6">
        {plan.map((week) => {
          const isExpanded = expanded[week.week]
          const days = week.days || []

          return (
            <div key={week.week} className="card bg-gray-800/40 border border-gray-700/50 hover:border-gray-600/50 transition-colors shadow-lg">
              <button
                className="w-full flex items-center justify-between group"
                onClick={() => setExpanded((p) => ({ ...p, [week.week]: !p[week.week] }))}
              >
                <div className="flex items-center gap-4">
                  <span className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 text-white text-lg font-bold flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:shadow-indigo-500/40 transition-shadow">
                    {week.week}
                  </span>
                  <div className="text-left">
                    <p className="font-bold text-lg text-gray-100 group-hover:text-white transition-colors">{week.theme}</p>
                    <p className="text-sm text-gray-400 mt-0.5 font-medium flex items-center gap-2">
                      <span>{days.length} days</span>
                      <span className="w-1 h-1 rounded-full bg-gray-600"></span>
                      <span>{week.hours_per_day || 2}h/day</span>
                      {week.adapted && <span className="text-yellow-400 bg-yellow-400/10 px-2 py-0.5 rounded text-xs ml-2">· Adapted</span>}
                    </p>
                  </div>
                </div>
                {isExpanded ? 
                  <ChevronUp size={20} className="text-gray-400 group-hover:text-indigo-400 transition-colors" /> : 
                  <ChevronDown size={20} className="text-gray-400 group-hover:text-indigo-400 transition-colors" />
                }
              </button>

              {isExpanded && (
                <div className="mt-6 space-y-4">
                  {days.map((dayItem) => {
                    const name = dayItem.topic || 'Unknown Topic'
                    const resources = dayItem.resources || []
                    const done = dayItem._completed || false
                    
                    const currentIndex = allDays.findIndex(d => d.topic === name && d.weekNum === week.week)
                    const prevDay = currentIndex > 0 ? allDays[currentIndex - 1] : null
                    const isLocked = prevDay && !prevDay._completed

                    return (
                      <div 
                        key={name} 
                        className={`bg-gray-800/80 rounded-2xl p-5 border ${isLocked ? 'border-gray-700/50 opacity-60 filter grayscale-[50%]' : 'border-gray-600/50 shadow-xl shadow-black/20 hover:border-gray-500 transition-all duration-300'}`}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex items-start gap-4">
                            <button 
                              onClick={() => !isLocked && toggleTopic(week.week, name, done)}
                              disabled={isLocked}
                              className={`mt-1 flex-shrink-0 ${isLocked ? 'cursor-not-allowed opacity-50' : 'hover:scale-110 transition-transform active:scale-95'}`}
                              title={isLocked ? "Complete previous topics first" : "Mark complete"}
                            >
                              {done ? (
                                <CheckCircle2 size={28} className="text-emerald-400 drop-shadow-[0_0_12px_rgba(52,211,153,0.5)]" />
                              ) : (
                                <Circle size={28} className="text-gray-500 hover:text-indigo-400 transition-colors" />
                              )}
                            </button>
                            <div>
                              <div className="flex items-center gap-3">
                                <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider bg-indigo-500/10 px-2.5 py-1 rounded-md">Day {dayItem.day}</span>
                                {isLocked && <span className="flex items-center gap-1 text-[10px] font-bold bg-red-950/80 text-red-400 px-2 py-1 rounded-md uppercase tracking-wide border border-red-900/50"><Lock size={10} /> Locked</span>}
                              </div>
                              <h4 className={`text-xl font-bold mt-2 ${done ? 'line-through text-gray-500 decoration-gray-600' : 'text-gray-100'} ${isLocked ? 'text-gray-400' : ''}`}>
                                {name}
                              </h4>
                            </div>
                          </div>
                        </div>

                        {!isLocked && resources.length > 0 && (
                          <div className="pl-[52px] mt-4 space-y-2.5">
                            <p className="text-[11px] font-bold text-gray-500 uppercase tracking-widest mb-1">Learning Materials</p>
                            {resources.map((res, i) => {
                              // Safely extract metadata properties, handling case where metadata is missing or a string
                              let title = 'Resource';
                              let url = '#';
                              if (res.metadata && typeof res.metadata === 'object') {
                                title = res.metadata.title || res.metadata.url || title;
                                url = res.metadata.url || url;
                              }
                              
                              return (
                                <a
                                  key={i}
                                  href={url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="flex items-center gap-2.5 text-sm text-indigo-300 hover:text-indigo-200 hover:underline bg-gray-900/60 p-2.5 rounded-xl border border-gray-700/50 transition-colors hover:border-indigo-500/30 group/link"
                                >
                                  <ExternalLink size={14} className="text-indigo-500/70 group-hover/link:text-indigo-400" />
                                  <span className="truncate font-medium">{title}</span>
                                </a>
                              );
                            })}
                          </div>
                        )}
                        
                        {!isLocked && (
                          <div className="pl-[52px] flex flex-wrap gap-3 mt-6 pt-5 border-t border-gray-700/50">
                            <button
                              onClick={() => navigate(`/test?topic=${encodeURIComponent(name)}`)}
                              className="bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm flex items-center gap-2 py-2.5 px-5 rounded-xl shadow-[0_0_20px_rgba(79,70,229,0.25)] hover:shadow-[0_0_25px_rgba(79,70,229,0.4)] transition-all transform hover:-translate-y-0.5 active:translate-y-0 border border-indigo-500"
                            >
                              <PlaySquare size={16} /> Take Practice Test
                            </button>
                            <button
                              onClick={() => navigate(`/interview?topic=${encodeURIComponent(name)}`)}
                              className="bg-gray-800 hover:bg-gray-700 text-gray-200 font-medium text-sm flex items-center gap-2 py-2.5 px-5 rounded-xl border border-gray-600 hover:border-indigo-500/50 transition-all shadow-sm"
                            >
                              <Video size={16} className="text-indigo-400" /> Start Mock Interview
                            </button>
                          </div>
                        )}
                      </div>
                    )
                  })}
                  {week.note && (
                    <p className="text-sm font-medium text-yellow-300 bg-yellow-900/30 border border-yellow-700/40 rounded-xl px-5 py-4 shadow-inner">{week.note}</p>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
