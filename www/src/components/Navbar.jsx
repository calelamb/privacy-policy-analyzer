import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X, Shield } from 'lucide-react'

const navLinks = [
  { path: '/', label: 'Home' },
  { path: '/research', label: 'Research' },
  { path: '/results', label: 'Results' },
  { path: '/team', label: 'Team' },
]

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const location = useLocation()

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-navy border-b border-navy-light">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14">
          <Link to="/" className="flex items-center gap-2.5">
            <Shield className="w-5 h-5 text-white/80" />
            <span className="font-semibold text-sm text-white tracking-wide">
              BYU EdTech Privacy Lab
            </span>
          </Link>

          <div className="hidden md:flex items-center gap-0.5">
            {navLinks.map(({ path, label }) => (
              <Link
                key={path}
                to={path}
                className={`px-3.5 py-1.5 rounded text-sm transition-colors ${
                  location.pathname === path
                    ? 'bg-white/15 text-white font-medium'
                    : 'text-white/70 hover:text-white hover:bg-white/10'
                }`}
              >
                {label}
              </Link>
            ))}
          </div>

          <button
            onClick={() => setOpen(!open)}
            className="md:hidden p-2 rounded text-white/70 hover:text-white hover:bg-white/10"
          >
            {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {open && (
        <div className="md:hidden bg-navy border-t border-white/10">
          <div className="px-4 py-2 space-y-0.5">
            {navLinks.map(({ path, label }) => (
              <Link
                key={path}
                to={path}
                onClick={() => setOpen(false)}
                className={`block px-3.5 py-2 rounded text-sm ${
                  location.pathname === path
                    ? 'bg-white/15 text-white font-medium'
                    : 'text-white/70 hover:text-white hover:bg-white/10'
                }`}
              >
                {label}
              </Link>
            ))}
          </div>
        </div>
      )}
    </nav>
  )
}
