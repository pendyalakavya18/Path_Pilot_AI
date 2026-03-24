import { useState, useRef, useEffect } from 'react'
import { toast } from 'react-hot-toast'
import { interviewAPI } from '../api/interview'
import { Send, Mic, MicOff, Video, VideoOff, Award, TrendingUp } from 'lucide-react'
import { useSearchParams } from 'react-router-dom'

const TOPICS = ['Data Structures', 'Algorithms', 'System Design', 'Python', 'Machine Learning', 'Databases', 'Behavioral']

export default function MockInterview() {
  const [searchParams] = useSearchParams()
  const initialTopic = searchParams.get('topic') || ''
  const [config, setConfig] = useState({ topic: initialTopic, difficulty: 'medium', numQuestions: 5 })
  const [session, setSession] = useState(null)   // { interviewId, question, questionIndex, totalQuestions }
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [lastEval, setLastEval] = useState(null)
  const [summary, setSummary] = useState(null)
  const chatRef = useRef(null)
  const videoRef = useRef(null)
  const [cameraEnabled, setCameraEnabled] = useState(false)
  const [micEnabled, setMicEnabled] = useState(false)
  const [stream, setStream] = useState(null)
  const [recognition, setRecognition] = useState(null)
  const [isSpeaking, setIsSpeaking] = useState(false)

  const transcriptRef = useRef('');
  const answerRef = useRef('');
  const micEnabledRef = useRef(false);

  useEffect(() => {
    micEnabledRef.current = micEnabled;
  }, [micEnabled]);

  // Initialize Speech Recognition
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recog = new SpeechRecognition();
      recog.continuous = true;
      recog.interimResults = true;
      recog.onresult = (event) => {
        let currentIterim = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript + ' ';
          } else {
            currentIterim += transcript;
          }
        }
        
        if (finalTranscript) {
           transcriptRef.current += (transcriptRef.current ? ' ' : '') + finalTranscript.trim();
        }
        
        const newAnswer = (transcriptRef.current + ' ' + currentIterim).trim();
        answerRef.current = newAnswer;
        setAnswer(newAnswer);
      };
      
      recog.onerror = (e) => {
        console.error("Speech recognition error", e.error);
        if (e.error === 'not-allowed') {
          setMicEnabled(false);
          toast.error("Microphone access denied.");
        }
      }

      recog.onend = () => {
        transcriptRef.current = answerRef.current;
        if (micEnabledRef.current) {
          try { recog.start() } catch (e) {
              console.log("Restarting recog failed", e);
          }
        }
      };
      setRecognition(recog);
    } else {
      toast.error('Speech recognition not supported in this browser. Please use Chrome.');
    }
  }, []);

  // Handle camera toggling
  const toggleCamera = async () => {
    if (cameraEnabled && stream) {
      const tracks = stream.getVideoTracks();
      tracks.forEach(t => t.stop());
      setCameraEnabled(false);
      if (!micEnabled) {
        setStream(null);
      }
    } else {
      try {
        const newStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: micEnabled });
        setStream(newStream);
        if (videoRef.current) videoRef.current.srcObject = newStream;
        setCameraEnabled(true);
      } catch (err) {
        toast.error('Failed to access camera');
      }
    }
  }

  // Handle mic toggling
  const toggleMic = async () => {
    if (micEnabled) {
      if (recognition) recognition.stop();
      if (stream) {
        stream.getAudioTracks().forEach(t => t.stop());
        if (!cameraEnabled) setStream(null);
      }
      setMicEnabled(false);
    } else {
      try {
        if (!stream) {
          const newStream = await navigator.mediaDevices.getUserMedia({ video: cameraEnabled, audio: true });
          setStream(newStream);
          if (videoRef.current && cameraEnabled) videoRef.current.srcObject = newStream;
        } else {
            // we already have stream, but might not have audio
            const audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            audioStream.getAudioTracks().forEach(track => stream.addTrack(track));
        }
        if (recognition) {
            setAnswer('');
            recognition.start();
        }
        setMicEnabled(true);
      } catch (err) {
        toast.error('Failed to access microphone');
      }
    }
  }

  // Speak AI question
  const speakText = (text) => {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    window.speechSynthesis.speak(utterance);
  }

  useEffect(() => { chatRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [lastEval, session])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (stream) {
          stream.getTracks().forEach(t => t.stop());
      }
      if (recognition) {
          recognition.stop();
      }
      if (window.speechSynthesis) {
          window.speechSynthesis.cancel();
      }
    }
  }, [stream, recognition]);

  const startInterview = async () => {
    if (!config.topic) { toast.error('Select a topic'); return }
    setLoading(true)
    try {
      const res = await interviewAPI.start({
        topic: config.topic,
        difficulty: config.difficulty,
        num_questions: config.numQuestions,
      })
      setSession({ interviewId: res.data.interview_id, question: res.data.question, questionIndex: 0, totalQuestions: res.data.total_questions })
      speakText(res.data.question);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to start interview')
    } finally {
      setLoading(false)
    }
  }

  const submitAnswer = async () => {
    if (!answer.trim()) return
    setLoading(true)

    // Automatically stop mic upon submission
    if (micEnabled) {
      toggleMic();
    }

    try {
      const res = await interviewAPI.answer(session.interviewId, answer)
      const data = res.data
      setLastEval(data.evaluation)
      setAnswer('')
      transcriptRef.current = '';
      answerRef.current = '';
      
      if (recognition && micEnabled) {
          recognition.stop() // Will restart automatically via onend and clear memory
      }

      if (data.is_complete) {
        const sumRes = await interviewAPI.getSummary(session.interviewId)
        setSummary(sumRes.data)
        setSession(null)
      } else {
        setSession((prev) => ({
          ...prev,
          question: data.next_question,
          questionIndex: data.question_index,
        }))
        speakText(data.next_question);
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to submit answer')
    } finally {
      setLoading(false)
    }
  }

  // ── Summary view ──────────────────────────────────────────────────
  if (summary) {
    return (
      <div className="p-8 max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-100 mb-6">Interview Complete 🎉</h1>
        <div className="grid grid-cols-2 gap-4 mb-6">
          {[
            { label: 'Overall', value: summary.overall_score },
            { label: 'Technical', value: summary.technical_score },
            { label: 'Communication', value: summary.communication_score },
            { label: 'Confidence', value: summary.confidence_score },
          ].map((s) => (
            <div key={s.label} className="card text-center">
              <p className="text-gray-400 text-sm mb-1">{s.label}</p>
              <p className={`text-3xl font-bold ${s.value >= 7 ? 'text-green-400' : s.value >= 5 ? 'text-yellow-400' : 'text-red-400'}`}>
                {(s.value ?? 0).toFixed(1)}
              </p>
              <p className="text-xs text-gray-600">/10</p>
            </div>
          ))}
        </div>
        <div className="card mb-4">
          <h3 className="font-semibold text-gray-200 mb-2">Overall Feedback</h3>
          <p className="text-gray-400 text-sm leading-relaxed">{summary.feedback}</p>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="card">
            <h3 className="font-semibold text-green-400 mb-2 flex items-center gap-2"><Award size={16} /> Strengths</h3>
            <ul className="space-y-1">{summary.strengths?.map((s, i) => <li key={i} className="text-sm text-gray-400">• {s}</li>)}</ul>
          </div>
          <div className="card">
            <h3 className="font-semibold text-yellow-400 mb-2 flex items-center gap-2"><TrendingUp size={16} /> Improvements</h3>
            <ul className="space-y-1">{summary.improvements?.map((s, i) => <li key={i} className="text-sm text-gray-400">• {s}</li>)}</ul>
          </div>
        </div>
        <button onClick={() => { setSummary(null); setLastEval(null) }} className="btn-primary mt-6">
          Start New Interview
        </button>
      </div>
    )
  }

  // ── Config view ───────────────────────────────────────────────────
  if (!session) {
    return (
      <div className="p-8 max-w-xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-100 mb-2">Mock Interview</h1>
        <p className="text-gray-400 mb-8">AI will interview you and evaluate your answers in real-time.</p>
        <div className="card space-y-5">
          <div>
            <label className="label">Topic</label>
            {initialTopic ? (
              <input className="input opacity-70 cursor-not-allowed bg-gray-800 border-gray-700 text-gray-400" value={config.topic} disabled />
            ) : (
              <select className="input" value={config.topic} onChange={(e) => setConfig({ ...config, topic: e.target.value })}>
                <option value="">Select topic</option>
                {TOPICS.map((t) => <option key={t} value={t}>{t}</option>)}
              </select>
            )}
          </div>
          <div>
            <label className="label">Difficulty</label>
            <div className="flex gap-3">
              {['easy', 'medium', 'hard'].map((d) => (
                <button
                  key={d}
                  type="button"
                  onClick={() => setConfig({ ...config, difficulty: d })}
                  className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors capitalize ${config.difficulty === d ? 'bg-indigo-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
                >
                  {d}
                </button>
              ))}
            </div>
          </div>
          <div>
            <label className="label">Number of Questions: {config.numQuestions}</label>
            <input type="range" min="3" max="10" value={config.numQuestions} onChange={(e) => setConfig({ ...config, numQuestions: +e.target.value })} className="w-full accent-indigo-500" />
          </div>
          <button className="btn-primary w-full" onClick={startInterview} disabled={loading}>
            {loading ? 'Starting…' : 'Start Interview'}
          </button>
        </div>
      </div>
    )
  }

  // ── Active interview ──────────────────────────────────────────────
  return (
    <div className="h-full min-h-[calc(100vh-4rem)] flex flex-col bg-gray-950 text-gray-100 p-6 md:p-10 relative overflow-hidden">
      
      {/* Dynamic Background Glow Based on AI Speaking state */}
      <div className={`absolute inset-0 pointer-events-none transition-opacity duration-1000 ${isSpeaking ? 'opacity-30' : 'opacity-0'}`}>
        <div className="absolute top-[-20%] left-1/4 w-[50vw] h-[50vh] bg-indigo-600/40 blur-[120px] rounded-full animate-pulse-slow"></div>
        <div className="absolute bottom-1/4 right-1/4 w-[40vw] h-[40vh] bg-cyan-600/30 blur-[120px] rounded-full animate-blob animation-delay-2000"></div>
      </div>

      <div className="max-w-6xl mx-auto w-full flex flex-col h-full relative z-10 flex-1">
        <header className="flex items-center justify-between border-b border-gray-800/50 pb-5 mb-8">
          <div>
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-300">Mock Interview</h1>
            <p className="text-gray-400 text-sm mt-1">{config.topic} • {config.difficulty}</p>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs font-semibold text-indigo-300 bg-indigo-950/50 px-3 py-1.5 rounded-full border border-indigo-500/30">
              Q {session.questionIndex + 1} of {session.totalQuestions}
            </span>
          </div>
        </header>

        <main className="flex-1 flex flex-col lg:flex-row gap-8 min-h-0">
          
          {/* Left Column: AI & Feedback */}
          <div className="flex-1 flex flex-col min-h-0 overflow-y-auto pr-2 scrollbar-hide space-y-6">
            
            {/* AI Interviwer Card */}
            <div className={`relative overflow-hidden rounded-2xl border transition-all duration-500 ${isSpeaking ? 'border-indigo-500/60 shadow-[0_0_30px_rgba(99,102,241,0.25)] bg-gray-900/80' : 'border-gray-800 bg-gray-900/40 backdrop-blur-md'}`}>
              <div className="p-8">
                <div className="flex items-center gap-3 mb-6">
                  <div className={`w-3 h-3 rounded-full ${isSpeaking ? 'bg-indigo-400 animate-pulse shadow-[0_0_10px_theme(colors.indigo.400)]' : 'bg-gray-600'}`}></div>
                  <h2 className="text-sm tracking-widest text-indigo-300 font-semibold uppercase">AI Interviewer</h2>
                  {isSpeaking && <span className="ml-2 text-xs text-indigo-400 animate-pulse">Speaking...</span>}
                </div>
                <p className="text-xl md:text-2xl font-medium leading-relaxed text-gray-100">
                  {session.question}
                </p>
              </div>
              
              {/* Subtle bottom gradient line */}
              <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500/0 via-indigo-500/40 to-indigo-500/0"></div>
            </div>

            {/* Last Evaluation Card */}
            {lastEval && (
              <div className="rounded-2xl border border-gray-800 bg-gray-900/30 backdrop-blur-sm p-6 animate-fade-in-up">
                <div className="flex items-center gap-2 mb-4">
                  <Award size={18} className="text-yellow-500" />
                  <h3 className="text-sm font-semibold text-gray-300 tracking-wide uppercase">Previous Answer Feedback</h3>
                </div>
                
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-5">
                  {[
                    { key: 'technical', label: 'Technical Accuracy' },
                    { key: 'communication', label: 'Communication' },
                    { key: 'problem_solving', label: 'Problem Solving' },
                    { key: 'cultural_fit', label: 'Cultural Fit' }
                  ].map((metric) => (
                    <div key={metric.key} className="bg-gray-950/50 rounded-xl p-3 border border-gray-800/60 flex flex-col items-center justify-center">
                      <p className={`text-2xl font-bold mb-1 ${lastEval[metric.key] >= 8 ? 'text-green-400 drop-shadow-[0_0_8px_rgba(74,222,128,0.3)]' : lastEval[metric.key] >= 5 ? 'text-yellow-400' : 'text-red-400'}`}>
                        {lastEval[metric.key] ?? '-'}
                      </p>
                      <p className="text-[10px] text-gray-500 uppercase font-medium text-center leading-tight">{metric.label}</p>
                    </div>
                  ))}
                </div>
                
                <div className="bg-gray-800/30 rounded-lg p-4 border border-gray-700/30">
                  <p className="text-sm text-gray-300 leading-relaxed">
                    <span className="text-gray-500 mr-2">Feedback:</span>
                    {lastEval.feedback}
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Right Column: User Input & Camera */}
          <div className="lg:w-[420px] flex flex-col gap-6 shrink-0 h-full">
            
            {/* Camera Viewport */}
            <div className={`relative rounded-2xl overflow-hidden aspect-[4/3] bg-gray-900 border-2 transition-colors duration-300 flex flex-col items-center justify-center shadow-2xl ${micEnabled && !isSpeaking ? 'border-cyan-500/50 shadow-[0_0_20px_rgba(6,182,212,0.15)]' : 'border-gray-800'}`}>
              
              <video 
                ref={videoRef} 
                autoPlay 
                playsInline 
                muted 
                className={`absolute inset-0 w-full h-full object-cover transition-opacity duration-300 ${!cameraEnabled ? 'opacity-0' : 'opacity-100'}`} 
              />
              
              {!cameraEnabled && (
                <div className="flex flex-col items-center justify-center text-gray-600 z-10">
                  <VideoOff size={40} className="mb-3 opacity-50" />
                  <span className="font-medium tracking-wide">Camera Disabled</span>
                </div>
              )}

              {/* Status overlays */}
              {micEnabled && !isSpeaking && (
                <div className="absolute top-4 right-4 bg-cyan-950/80 backdrop-blur-md px-3 py-1.5 rounded-full border border-cyan-500/30 flex items-center gap-2 z-20">
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
                  </span>
                  <span className="text-xs font-semibold text-cyan-300">Listening...</span>
                </div>
              )}

              {/* Controls Overlay */}
              <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-gray-950/90 via-gray-900/50 to-transparent z-20 pt-12">
                <div className="flex justify-center gap-4">
                  <button 
                    onClick={toggleMic} 
                    className={`flex items-center justify-center w-12 h-12 rounded-full backdrop-blur-md transition-all duration-200 border shadow-lg ${micEnabled ? 'bg-cyan-600/90 border-cyan-500/50 text-white hover:bg-cyan-500' : 'bg-gray-800/80 border-gray-700 text-red-400 hover:bg-gray-700 hover:text-red-300'}`}
                    title={micEnabled ? 'Mute Microphone' : 'Unmute Microphone'}
                  >
                    {micEnabled ? <Mic size={20} /> : <MicOff size={20} />}
                  </button>
                  <button 
                    onClick={toggleCamera} 
                    className={`flex items-center justify-center w-12 h-12 rounded-full backdrop-blur-md transition-all duration-200 border shadow-lg ${cameraEnabled ? 'bg-indigo-600/90 border-indigo-500/50 text-white hover:bg-indigo-500' : 'bg-gray-800/80 border-gray-700 text-gray-400 hover:bg-gray-700 hover:text-white'}`}
                    title={cameraEnabled ? 'Turn off camera' : 'Turn on camera'}
                  >
                    {cameraEnabled ? <Video size={20} /> : <VideoOff size={20} />}
                  </button>
                </div>
              </div>
            </div>

            {/* Answer Input Area */}
            <div ref={chatRef} className="flex-1 flex flex-col bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-2xl p-5 shadow-inner">
              <div className="flex justify-between items-end mb-3">
                <label className="text-xs font-semibold tracking-wider text-gray-500 uppercase">Your Answer</label>
                {micEnabled && answer && (
                  <span className="text-[10px] text-cyan-500 font-medium animate-pulse">Transcribing Voice...</span>
                )}
              </div>
              
              <textarea
                className="w-full flex-1 min-h-[140px] bg-gray-950/50 border border-gray-700/50 rounded-xl leading-relaxed text-gray-200 p-4 focus:ring-2 focus:ring-indigo-500/40 focus:border-indigo-500/50 transition-all resize-none placeholder-gray-600 font-medium"
                placeholder={micEnabled ? "Speak naturally to answer..." : "Type your answer here..."}
                value={answer}
                onChange={(e) => {
                  setAnswer(e.target.value);
                  answerRef.current = e.target.value;
                  transcriptRef.current = e.target.value;
                }}
                onKeyDown={(e) => { if (e.key === 'Enter' && e.ctrlKey) submitAnswer() }}
              />
              
              <div className="flex items-center justify-between mt-4">
                <p className="text-xs text-gray-600 font-medium tracking-wide">Press <kbd className="font-mono bg-gray-800 px-1 py-0.5 rounded text-gray-400">Ctrl</kbd> + <kbd className="font-mono bg-gray-800 px-1 py-0.5 rounded text-gray-400">Enter</kbd> to submit</p>
                <div className="flex gap-3">
                  {micEnabled && (
                    <button 
                      className="flex items-center gap-2 px-6 py-2.5 rounded-xl font-semibold transition-all shadow-lg bg-red-600 hover:bg-red-500 text-white shadow-red-500/20"
                      onClick={toggleMic}
                      disabled={loading}
                    >
                      <MicOff size={18} />
                      Stop Recording
                    </button>
                  )}
                  <button 
                    className={`flex items-center gap-2 px-6 py-2.5 rounded-xl font-semibold transition-all shadow-lg ${answer.trim() && !loading ? 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-500/20 shadow-[0_4px_14px_0_rgba(79,70,229,0.39)]' : 'bg-gray-800 text-gray-500 cursor-not-allowed border border-gray-700'}`} 
                    onClick={submitAnswer} 
                    disabled={loading || !answer.trim()}
                  >
                    {loading ? (
                      <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                    ) : (
                      <Send size={18} className={answer.trim() ? "translate-x-0.5 transition-transform" : ""} />
                    )}
                    <span>{loading ? 'Submitting...' : 'Submit'}</span>
                  </button>
                </div>
              </div>
            </div>

          </div>
        </main>
      </div>
    </div>
  )
}
