import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { MapPin, BarChart2, Brain, FileText, User, LogOut, Zap } from 'lucide-react'
import useAuthStore from '../stores/authStore'
import clsx from 'clsx'

const navItems = [
  { to: '/dashboard',   label: 'Dashboard',   icon: BarChart2 },
  { to: '/roadmap/create', label: 'Roadmap',  icon: MapPin },
  { to: '/skill-gap',   label: 'Skill Gap',   icon: Zap },
  { to: '/test',        label: 'Practice',    icon: FileText },
  { to: '/interview',   label: 'Interview',   icon: Brain },
  { to: '/profile',     label: 'Profile',     icon: User },
]

export default function Navbar() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside className="w-60 flex-shrink-0 bg-gray-900 border-r border-gray-800 flex flex-col">
        {/* Brand */}
        <div className="px-6 py-5 border-b border-gray-800">
          <span className="text-xl font-bold text-indigo-400">PathPilot AI</span>
          <p className="text-xs text-gray-500 mt-0.5">Career Preparation</p>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
          {navItems.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                clsx(
                  'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-indigo-600 text-white'
                    : 'text-gray-400 hover:bg-gray-800 hover:text-gray-100'
                )
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* User + Logout */}
        <div className="px-4 py-4 border-t border-gray-800">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-8 h-8 rounded-full bg-indigo-700 flex items-center justify-center text-sm font-bold">
              {user?.name?.[0]?.toUpperCase() || 'U'}
            </div>
            <div className="min-w-0">
              <p className="text-sm font-medium text-gray-200 truncate">{user?.name || 'User'}</p>
              <p className="text-xs text-gray-500 truncate">{user?.email || ''}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 text-sm text-gray-500 hover:text-red-400 transition-colors w-full"
          >
            <LogOut size={15} />
            Sign out
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto bg-gray-950">
        <Outlet />
      </main>
    </div>
  )
}
