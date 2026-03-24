import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoute'
import Navbar from './components/Navbar'

import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import RoadmapCreate from './pages/RoadmapCreate'
import RoadmapView from './pages/RoadmapView'
import MockInterview from './pages/MockInterview'
import PracticeTest from './pages/PracticeTest'
import SkillGap from './pages/SkillGap'
import Profile from './pages/Profile'

import Landing from './pages/Landing'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected routes — require JWT */}
        <Route element={<ProtectedRoute />}>
          <Route element={<Navbar />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/roadmap/create" element={<RoadmapCreate />} />
            <Route path="/roadmap/:id" element={<RoadmapView />} />
            <Route path="/interview" element={<MockInterview />} />
            <Route path="/test" element={<PracticeTest />} />
            <Route path="/skill-gap" element={<SkillGap />} />
            <Route path="/profile" element={<Profile />} />
          </Route>
        </Route>

        {/* Default redirect */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
