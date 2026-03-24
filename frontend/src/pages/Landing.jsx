import React from 'react';
import { Link } from 'react-router-dom';
import { Bot, Map, Target, Award, ArrowRight, Zap, BookOpen } from 'lucide-react';

export default function Landing() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 overflow-hidden font-sans selection:bg-indigo-500/30">
      
      {/* Background Orbs */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-600/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-600/20 rounded-full blur-[120px] pointer-events-none" />

      {/* Navigation */}
      <nav className="relative z-10 flex items-center justify-between px-8 py-6 max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
            <Target className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold tracking-tight text-white">PathPilot <span className="text-indigo-400">AI</span></span>
        </div>
        <div className="flex items-center gap-4">
          <Link to="/login" className="text-sm font-medium text-gray-300 hover:text-white transition-colors">Sign In</Link>
          <Link to="/register" className="text-sm font-medium bg-white text-gray-950 px-4 py-2 rounded-full hover:bg-gray-200 transition-colors">Get Started</Link>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="relative z-10 flex flex-col items-center justify-center text-center px-4 pt-24 pb-32 max-w-5xl mx-auto">

        
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8 leading-[1.1]">
          Your AI Co-Pilot for <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">
            Dream Tech Roles
          </span>
        </h1>
        
        <p className="text-lg md:text-xl text-gray-400 max-w-2xl mb-10 leading-relaxed">
          Upload your resume, select your target company, and let our AI agents generate a personalized learning roadmap, gap analysis, and conduct real-time mock interviews.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center gap-4">
          <Link to="/register" className="group flex items-center gap-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-4 rounded-full text-lg font-semibold hover:opacity-90 transition-opacity">
            Start Your Journey
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
          <Link to="/login" className="px-8 py-4 rounded-full text-lg font-semibold text-gray-300 border border-gray-700 hover:bg-gray-800 transition-colors">
            Resume Existing Plan
          </Link>
        </div>
      </main>

      {/* Features Grid */}
      <section className="relative z-10 max-w-7xl mx-auto px-4 pb-32">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Feature 1 */}
          <div className="bg-gray-900/50 border border-gray-800 backdrop-blur-sm p-8 rounded-3xl hover:border-indigo-500/50 transition-colors group">
            <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Map className="w-6 h-6 text-indigo-400" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">AI Study Roadmaps</h3>
            <p className="text-gray-400 leading-relaxed">
              We analyze your resume against your dream role's requirements and generate a day-by-day preparation timeline tailored to your skill gaps.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="bg-gray-900/50 border border-gray-800 backdrop-blur-sm p-8 rounded-3xl hover:border-purple-500/50 transition-colors group">
            <div className="w-12 h-12 rounded-2xl bg-purple-500/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Bot className="w-6 h-6 text-purple-400" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Interactive Mock Interviews</h3>
            <p className="text-gray-400 leading-relaxed">
              Experience real-time AI interviews with dynamic follow-up questions, behavioral assessments, and instant actionable feedback.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="bg-gray-900/50 border border-gray-800 backdrop-blur-sm p-8 rounded-3xl hover:border-pink-500/50 transition-colors group">
            <div className="w-12 h-12 rounded-2xl bg-pink-500/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Award className="w-6 h-6 text-pink-400" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Smart Practice Tests</h3>
            <p className="text-gray-400 leading-relaxed">
              Take RAG-powered conceptual MCQs and coding tests that adapt to your progress and target the areas where you need the most improvement.
            </p>
          </div>

        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-800/50 py-8 text-center text-gray-500 text-sm">
        <p>© {new Date().getFullYear()} PathPilot AI. All rights reserved.</p>
        <p className="mt-1">Built with React, FastAPI, and Qdrant.</p>
      </footer>
    </div>
  );
}
