import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import AdminLayout from './layouts/AdminLayout'
import GuestLayout from './layouts/GuestLayout'
import LoginPage from './pages/admin/LoginPage'
import AdminDashboard from './pages/admin/Dashboard'
import GuestsPage from './pages/admin/GuestsPage'
import TasksPage from './pages/admin/TasksPage'
import CostsPage from './pages/admin/CostsPage'
import ContentPage from './pages/admin/ContentPage'
import AnalyticsPage from './pages/admin/AnalyticsPage'
import GuestRegistration from './pages/guest/Registration'
import GuestInfo from './pages/guest/Info'

function AppRoutes() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  return (
    <Routes>
      {/* Guest Routes (Public) */}
      <Route path="/" element={<GuestLayout />}>
        <Route index element={<GuestRegistration />} />
        <Route path="info" element={<GuestInfo />} />
      </Route>

      {/* Admin Routes (Protected) */}
      <Route
        path="/admin"
        element={user ? <AdminLayout /> : <Navigate to="/admin/login" replace />}
      >
        <Route index element={<Navigate to="/admin/dashboard" replace />} />
        <Route path="dashboard" element={<AdminDashboard />} />
        <Route path="guests" element={<GuestsPage />} />
        <Route path="tasks" element={<TasksPage />} />
        <Route path="costs" element={<CostsPage />} />
        <Route path="content" element={<ContentPage />} />
        <Route path="analytics" element={<AnalyticsPage />} />
      </Route>

      <Route
        path="/admin/login"
        element={user ? <Navigate to="/admin/dashboard" replace /> : <LoginPage />}
      />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  )
}

export default App

