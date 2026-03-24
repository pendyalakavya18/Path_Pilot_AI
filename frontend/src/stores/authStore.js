import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { authAPI } from '../api/auth'

const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,

      login: async (email, password) => {
        const res = await authAPI.login({ email, password })
        const { access_token, refresh_token } = res.data
        localStorage.setItem('access_token', access_token)
        localStorage.setItem('refresh_token', refresh_token)
        // Fetch user profile
        const meRes = await authAPI.getMe()
        set({ user: meRes.data, isAuthenticated: true })
        return meRes.data
      },

      register: async (name, email, password) => {
        const res = await authAPI.register({ name, email, password })
        const { access_token, refresh_token } = res.data
        localStorage.setItem('access_token', access_token)
        localStorage.setItem('refresh_token', refresh_token)
        const meRes = await authAPI.getMe()
        set({ user: meRes.data, isAuthenticated: true })
        return meRes.data
      },

      logout: () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        set({ user: null, isAuthenticated: false })
      },

      refreshUser: async () => {
        try {
          const res = await authAPI.getMe()
          set({ user: res.data, isAuthenticated: true })
        } catch {
          get().logout()
        }
      },

      updateUser: (data) => set((state) => ({ user: { ...state.user, ...data } })),
    }),
    {
      name: 'pathpilot-auth',
      partialize: (state) => ({ user: state.user, isAuthenticated: state.isAuthenticated }),
    }
  )
)

export default useAuthStore
