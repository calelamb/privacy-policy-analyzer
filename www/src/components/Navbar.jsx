import { useState, useRef, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X, Shield, ChevronDown } from 'lucide-react'

const mainLinks = [
  { path: '/', label: 'Home' },
  { path: '/research', label: 'Research' },
  { path: '/results', label: 'Results' },
]

const toolLinks = [
  { path: '/analyze', label: 'Analyze a Policy' },
  { path: '/explorer', label: 'App Explorer' },
  { path: '/compare', label: 'Compare Apps' },
]

const referenceLinks = [
  { path: '/resources', label: 'Resources' },
  { path: '/legislation', label: 'Legislation' },
]

function Dropdown({ label, links, location }) {
  const [open, setOpen] = useState(false)
  const ref = useRef(null)
  const isActive = links.some((l) => l.path === location.pathname)

  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false)
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen(!open)}
        className={`inline-flex items-center gap-1 px-3.5 py-1.5 rounded text-sm transition-colors ${
          isActive
            ? 'bg-white/15 text-white font-medium'
            : 'text-white/70 hover:text-white hover:bg-white/10'
        }`}
      >
        {label}
        <ChevronDown className={`w-3.5 h-3.5 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>
      {open && (
        <div className="absolute top-full left-0 mt-1 w-48 bg-navy-light border border-white/10 rounded-lg shadow-xl overflow-hidden z-50">
          {links.map(({ path, label: linkLabel }) => (
            <Link
              key={path}
              to={path}
              onClick={() => setOpen(false)}
              className={`block px-4 py-2.5 text-sm transition-colors ${
                location.pathname === path
                  ? 'bg-white/15 text-white font-medium'
                  : 'text-white/70 hover:text-white hover:bg-white/10'
              }`}
            >
              {linkLabel}
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

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
            {mainLinks.map(({ path, label }) => (
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
            <Dropdown label="Tools" links={toolLinks} location={location} />
            <Dropdown label="Reference" links={referenceLinks} location={location} />
            <Link
              to="/team"
              className={`px-3.5 py-1.5 rounded text-sm transition-colors ${
                location.pathname === '/team'
                  ? 'bg-white/15 text-white font-medium'
                  : 'text-white/70 hover:text-white hover:bg-white/10'
              }`}
            >
              Team
            </Link>
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
            {mainLinks.map(({ path, label }) => (
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
            <p className="px-3.5 pt-3 pb-1 text-[10px] font-semibold uppercase tracking-wider text-white/40">
              Tools
            </p>
            {toolLinks.map(({ path, label }) => (
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
            <p className="px-3.5 pt-3 pb-1 text-[10px] font-semibold uppercase tracking-wider text-white/40">
              Reference
            </p>
            {referenceLinks.map(({ path, label }) => (
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
            <Link
              to="/team"
              onClick={() => setOpen(false)}
              className={`block px-3.5 py-2 rounded text-sm ${
                location.pathname === '/team'
                  ? 'bg-white/15 text-white font-medium'
                  : 'text-white/70 hover:text-white hover:bg-white/10'
              }`}
            >
              Team
            </Link>
          </div>
        </div>
      )}
    </nav>
  )
}
