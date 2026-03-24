import { useState } from 'react'
import { toast } from 'react-hot-toast'
import { testAPI } from '../api/test'
import { CheckCircle, XCircle, Trophy } from 'lucide-react'
import { useSearchParams } from 'react-router-dom'

const PERFORMANCE_COLOR = { Excellent: 'text-green-400', Good: 'text-blue-400', Average: 'text-yellow-400', 'Needs Improvement': 'text-red-400' }

export default function PracticeTest() {
  const [searchParams] = useSearchParams()
  const initialTopic = searchParams.get('topic') || ''
  const [config, setConfig] = useState({ topic: initialTopic, numQuestions: 10 })
  const [phase, setPhase] = useState('setup')   // setup | answering | results
  const [testId, setTestId] = useState(null)
  const [questions, setQuestions] = useState([])
  const [selected, setSelected] = useState({})  // { [idx]: 'A' | 'B' | 'C' | 'D' }
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const generateTest = async () => {
    if (!config.topic.trim()) { toast.error('Enter a topic'); return }
    setLoading(true)
    try {
      const res = await testAPI.generate({ topic: config.topic, num_questions: config.numQuestions })
      setTestId(res.data.test_id)
      setQuestions(res.data.questions)
      setSelected({})
      setPhase('answering')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to generate test')
    } finally {
      setLoading(false)
    }
  }

  const submitTest = async () => {
    if (Object.keys(selected).length < questions.length) {
      toast.error('Answer all questions before submitting')
      return
    }
    setLoading(true)
    try {
      const answers = questions.map((_, i) => selected[i] ?? 0)
      const res = await testAPI.submit({ test_id: testId, answers })
      setResults(res.data)
      setPhase('results')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to submit test')
    } finally {
      setLoading(false)
    }
  }

  const reset = () => {
    setPhase('setup')
    setTestId(null)
    setQuestions([])
    setSelected({})
    setResults(null)
  }

  // ── Setup ─────────────────────────────────────────────────────────
  if (phase === 'setup') {
    return (
      <div className="p-8 max-w-xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-100 mb-2">Practice Test</h1>
        <p className="text-gray-400 mb-8">AI generates topic-specific MCQs and evaluates your performance.</p>
        <div className="card space-y-5">
          <div>
            <label className="label">Topic</label>
            <input 
              className={`input ${initialTopic ? 'opacity-70 cursor-not-allowed bg-gray-800 border-gray-700 text-gray-400' : ''}`} 
              placeholder="e.g. Binary Trees, REST APIs, Sorting Algorithms" 
              value={config.topic} 
              onChange={(e) => setConfig({ ...config, topic: e.target.value })} 
              disabled={!!initialTopic}
            />
          </div>
          <div>
            <label className="label">Number of Questions: {config.numQuestions}</label>
            <input type="range" min="5" max="20" value={config.numQuestions} onChange={(e) => setConfig({ ...config, numQuestions: +e.target.value })} className="w-full accent-indigo-500" />
          </div>
          <button className="btn-primary w-full" onClick={generateTest} disabled={loading}>
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full" />
                Generating…
              </span>
            ) : 'Generate Test'}
          </button>
        </div>
      </div>
    )
  }

  // ── Answering ─────────────────────────────────────────────────────
  if (phase === 'answering') {
    const answered = Object.keys(selected).length
    return (
      <div className="p-8 max-w-3xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-xl font-bold text-gray-100">{config.topic} — Practice Test</h1>
          <span className="text-sm text-gray-400">{answered}/{questions.length} answered</span>
        </div>
        <div className="space-y-6">
          {questions.map((q, idx) => (
            <div key={idx} className="card">
              <p className="text-gray-200 mb-4 font-medium">Q{idx + 1}. {q.question}</p>
              <div className="space-y-2">
                {(q.options || []).map((text, optIdx) => (
                  <label key={optIdx} className={`flex items-start gap-3 p-3 rounded-lg cursor-pointer border transition-colors ${selected[idx] === optIdx ? 'border-indigo-500 bg-indigo-950/40' : 'border-gray-700 hover:border-gray-600'}`}>
                    <input type="radio" name={`q${idx}`} value={optIdx} checked={selected[idx] === optIdx} onChange={() => setSelected({ ...selected, [idx]: optIdx })} className="mt-0.5 accent-indigo-500" />
                    <span className="text-sm text-gray-300"><span className="font-medium text-indigo-400">{String.fromCharCode(65 + optIdx)}.</span> {text}</span>
                  </label>
                ))}
              </div>
            </div>
          ))}
        </div>
        <div className="mt-8 flex gap-4">
          <button className="btn-primary" onClick={submitTest} disabled={loading}>
            {loading ? 'Submitting…' : 'Submit Test'}
          </button>
          <button className="btn-secondary" onClick={reset}>Cancel</button>
        </div>
      </div>
    )
  }

  // ── Results ───────────────────────────────────────────────────────
  if (phase === 'results' && results) {
    const pColor = PERFORMANCE_COLOR[results.performance_level] ?? 'text-gray-300'
    return (
      <div className="p-8 max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-100 mb-6">Test Results</h1>
        <div className="card flex items-center gap-8 mb-8">
          <Trophy size={40} className="text-yellow-400 shrink-0" />
          <div>
            <p className="text-5xl font-bold text-gray-100">{results.score}<span className="text-xl text-gray-500">%</span></p>
            <p className={`text-lg font-semibold ${pColor}`}>{results.performance_level}</p>
            <p className="text-sm text-gray-500 mt-1">{results.correct} of {results.total_questions} correct</p>
          </div>
        </div>
        <div className="space-y-5">
          {results.results?.map((r, idx) => (
            <div key={idx} className={`card border ${r.is_correct ? 'border-green-800/60' : 'border-red-800/60'}`}>
              <div className="flex items-start gap-3">
                {r.is_correct ? <CheckCircle size={18} className="text-green-400 shrink-0 mt-0.5" /> : <XCircle size={18} className="text-red-400 shrink-0 mt-0.5" />}
                <div className="flex-1 min-w-0">
                  <p className="text-gray-200 mb-2 text-sm font-medium">Q{idx + 1}. {r.question}</p>
                  <div className="flex flex-wrap gap-4 text-xs mb-2">
                    <span className="text-gray-400">Your answer: <span className="font-semibold text-gray-200">{r.options?.[r.user_answer] ?? r.user_answer}</span></span>
                    {!r.is_correct && <span className="text-gray-400">Correct: <span className="font-semibold text-green-400">{r.options?.[r.correct_answer] ?? r.correct_answer}</span></span>}
                  </div>
                  {r.explanation && <p className="text-xs text-gray-500 leading-relaxed">{r.explanation}</p>}
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className="mt-8 flex gap-4">
          <button className="btn-primary" onClick={reset}>Take Another Test</button>
        </div>
      </div>
    )
  }

  return null
}
