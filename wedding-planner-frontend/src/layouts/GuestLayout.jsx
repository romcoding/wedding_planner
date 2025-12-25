import { Outlet } from 'react-router-dom'

export default function GuestLayout() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8">
        <Outlet />
      </div>
    </div>
  )
}

