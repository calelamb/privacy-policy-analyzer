import { useState, useEffect, useMemo, useRef } from 'react'
import {
  Search,
  X,
  Plus,
  CheckCircle,
  XCircle,
  Shield,
  ShieldAlert,
  ShieldCheck,
  ArrowRight,
} from 'lucide-react'
import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
} from 'recharts'

const INDICATOR_LABELS = [
  'Data Collection',
  'Data Use Purpose',
  'Third-Party Sharing',
  'Parental Consent',
  'COPPA/FERPA',
  'Data Retention',
  'User Data Rights',
  'Data Security',
  'Tracking Tech',
]

const RADAR_LABELS = [
  'Collection',
  'Purpose',
  '3rd Party',
  'Consent',
  'COPPA/FERPA',
  'Retention',
  'Rights',
  'Security',
  'Tracking',
]

const CHART_COLORS = ['#002E5D', '#0047BA', '#00966C']
const RISK_COLORS = { Low: '#00966C', Medium: '#A39382', High: '#D14124' }

function AppSearch({ apps, onSelect, exclude }) {
  const [query, setQuery] = useState('')
  const [open, setOpen] = useState(false)
  const ref = useRef(null)

  const results = useMemo(() => {
    if (!query.trim()) return []
    const q = query.toLowerCase()
    return apps
      .filter((a) => a.name.toLowerCase().includes(q) && !exclude.includes(a.id))
      .slice(0, 8)
  }, [query, apps, exclude])

  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false)
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  return (
    <div ref={ref} className="relative">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
        <input
          type="text"
          placeholder="Search for an app..."
          className="w-full pl-9 pr-4 py-2.5 border border-border rounded-lg text-sm bg-surface text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-royal/40"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value)
            setOpen(true)
          }}
          onFocus={() => query && setOpen(true)}
        />
      </div>
      {open && results.length > 0 && (
        <div className="absolute z-20 w-full mt-1 bg-surface border border-border rounded-lg shadow-lg max-h-60 overflow-y-auto">
          {results.map((app) => (
            <button
              key={app.id}
              onClick={() => {
                onSelect(app)
                setQuery('')
                setOpen(false)
              }}
              className="w-full text-left px-4 py-2.5 text-sm hover:bg-page transition-colors flex items-center justify-between"
            >
              <span className="text-text-primary">{app.name}</span>
              <span className="text-xs text-text-muted">{app.score}/9</span>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

function ScoreRing({ score, color }) {
  const pct = (score / 9) * 100
  const radius = 36
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (pct / 100) * circumference
  return (
    <div className="relative w-24 h-24 mx-auto">
      <svg className="w-24 h-24 -rotate-90" viewBox="0 0 80 80">
        <circle cx="40" cy="40" r={radius} fill="none" stroke="#E5E7EB" strokeWidth="6" />
        <circle
          cx="40"
          cy="40"
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth="6"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className="transition-all duration-700"
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-lg font-bold text-text-primary">{score}/9</span>
      </div>
    </div>
  )
}

export default function Compare() {
  const [apps, setApps] = useState([])
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState([])

  useEffect(() => {
    fetch('/apps.json')
      .then((r) => r.json())
      .then((data) => {
        setApps(data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  const addApp = (app) => {
    if (selected.length < 3) setSelected([...selected, app])
  }

  const removeApp = (id) => {
    setSelected(selected.filter((a) => a.id !== id))
  }

  const radarData = RADAR_LABELS.map((label, i) => {
    const point = { indicator: label }
    selected.forEach((app, j) => {
      point[`app${j}`] = app.ind[i] ? 100 : 0
    })
    return point
  })

  const riskIcon = (risk) => {
    if (risk === 'Low') return <ShieldCheck className="w-4 h-4 text-emerald-600" />
    if (risk === 'High') return <ShieldAlert className="w-4 h-4 text-red-500" />
    return <Shield className="w-4 h-4 text-amber-600" />
  }

  return (
    <main className="pt-14">
      {/* Header */}
      <div className="bg-navy text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <p className="text-xs font-semibold uppercase tracking-[0.15em] text-byu-lightblue mb-2">
            Side-by-Side
          </p>
          <h1
            className="text-3xl sm:text-4xl font-bold mb-3"
            style={{ fontFamily: "'Merriweather', serif" }}
          >
            Compare Apps
          </h1>
          <p className="text-white/70 max-w-2xl leading-relaxed">
            Select up to 3 educational apps to compare their privacy compliance profiles
            side-by-side. Ideal for school districts evaluating competing tools.
          </p>
        </div>
      </div>

      {/* App selector */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-surface border border-border rounded-lg p-6">
          <h3 className="text-sm font-semibold text-text-primary mb-3">
            Select Apps to Compare ({selected.length}/3)
          </h3>

          {/* Selected chips */}
          {selected.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {selected.map((app, i) => (
                <span
                  key={app.id}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium text-white"
                  style={{ backgroundColor: CHART_COLORS[i] }}
                >
                  {app.name}
                  <button onClick={() => removeApp(app.id)} className="hover:bg-white/20 rounded-full p-0.5">
                    <X className="w-3.5 h-3.5" />
                  </button>
                </span>
              ))}
            </div>
          )}

          {selected.length < 3 && !loading && (
            <AppSearch apps={apps} onSelect={addApp} exclude={selected.map((a) => a.id)} />
          )}

          {loading && <p className="text-sm text-text-muted">Loading app database...</p>}
        </div>
      </section>

      {/* Comparison content */}
      {selected.length >= 2 && (
        <>
          {/* Score rings */}
          <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-8">
            <div className={`grid gap-4 ${selected.length === 3 ? 'grid-cols-3' : 'grid-cols-2'}`}>
              {selected.map((app, i) => (
                <div key={app.id} className="bg-surface border border-border rounded-lg p-6 text-center">
                  <div
                    className="w-3 h-3 rounded-full mx-auto mb-3"
                    style={{ backgroundColor: CHART_COLORS[i] }}
                  />
                  <h4 className="text-sm font-semibold text-text-primary mb-3 truncate">{app.name}</h4>
                  <ScoreRing score={app.score} color={RISK_COLORS[app.risk]} />
                  <div className="mt-3 flex items-center justify-center gap-1.5">
                    {riskIcon(app.risk)}
                    <span className="text-sm font-medium text-text-primary">{app.risk} Risk</span>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Overlay radar */}
          <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-8">
            <div className="bg-surface border border-border rounded-lg p-6">
              <h3 className="text-lg font-semibold text-text-primary mb-1">Compliance Overlay</h3>
              <p className="text-sm text-text-muted mb-4">Radar comparison of all selected apps</p>
              <div className="h-[360px]">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={radarData} outerRadius="65%">
                    <PolarGrid stroke="#E5E7EB" />
                    <PolarAngleAxis dataKey="indicator" tick={{ fill: '#7C878E', fontSize: 11 }} />
                    <PolarRadiusAxis angle={90} domain={[0, 100]} tick={false} axisLine={false} />
                    {selected.map((app, i) => (
                      <Radar
                        key={app.id}
                        name={app.name}
                        dataKey={`app${i}`}
                        stroke={CHART_COLORS[i]}
                        fill={CHART_COLORS[i]}
                        fillOpacity={0.08}
                        strokeWidth={2}
                      />
                    ))}
                    <Legend
                      wrapperStyle={{ fontSize: '12px', paddingTop: '12px' }}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </section>

          {/* Indicator comparison table */}
          <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-24">
            <div className="bg-surface border border-border rounded-lg overflow-hidden">
              <div className="p-6 pb-3">
                <h3 className="text-lg font-semibold text-text-primary mb-0.5">
                  Indicator Comparison
                </h3>
                <p className="text-sm text-text-muted">
                  Detailed side-by-side of all 9 privacy indicators
                </p>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-t border-border bg-page">
                      <th className="text-left font-semibold text-text-muted text-xs uppercase tracking-wider px-6 py-3">
                        Indicator
                      </th>
                      {selected.map((app, i) => (
                        <th
                          key={app.id}
                          className="text-center font-semibold text-xs uppercase tracking-wider px-6 py-3"
                          style={{ color: CHART_COLORS[i] }}
                        >
                          {app.name.length > 20 ? app.name.slice(0, 20) + '...' : app.name}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border">
                    {INDICATOR_LABELS.map((label, idx) => (
                      <tr key={label} className="hover:bg-page/50 transition-colors">
                        <td className="px-6 py-2.5 font-medium text-text-primary">{label}</td>
                        {selected.map((app) => (
                          <td key={app.id} className="px-6 py-2.5 text-center">
                            {app.ind[idx] ? (
                              <CheckCircle className="w-5 h-5 text-emerald-600 inline" />
                            ) : (
                              <XCircle className="w-5 h-5 text-red-400 inline" />
                            )}
                          </td>
                        ))}
                      </tr>
                    ))}
                    {/* COPPA row */}
                    <tr className="hover:bg-page/50 transition-colors bg-page/30">
                      <td className="px-6 py-2.5 font-medium text-text-primary">Claims COPPA</td>
                      {selected.map((app) => (
                        <td key={app.id} className="px-6 py-2.5 text-center">
                          {app.coppa[1] ? (
                            <CheckCircle className="w-5 h-5 text-emerald-600 inline" />
                          ) : (
                            <XCircle className="w-5 h-5 text-red-400 inline" />
                          )}
                        </td>
                      ))}
                    </tr>
                    {/* GDPR row */}
                    <tr className="hover:bg-page/50 transition-colors bg-page/30">
                      <td className="px-6 py-2.5 font-medium text-text-primary">Claims GDPR</td>
                      {selected.map((app) => (
                        <td key={app.id} className="px-6 py-2.5 text-center">
                          {app.gdpr[1] ? (
                            <CheckCircle className="w-5 h-5 text-emerald-600 inline" />
                          ) : (
                            <XCircle className="w-5 h-5 text-red-400 inline" />
                          )}
                        </td>
                      ))}
                    </tr>
                    {/* Third parties */}
                    <tr className="hover:bg-page/50 transition-colors bg-page/30">
                      <td className="px-6 py-2.5 font-medium text-text-primary">Third Parties</td>
                      {selected.map((app) => (
                        <td key={app.id} className="px-6 py-2.5 text-center font-semibold text-text-primary">
                          {app.tpCount}
                        </td>
                      ))}
                    </tr>
                    {/* Score */}
                    <tr className="border-t-2 border-navy/20">
                      <td className="px-6 py-3 font-semibold text-navy">Total Score</td>
                      {selected.map((app) => (
                        <td key={app.id} className="px-6 py-3 text-center">
                          <span className="text-lg font-bold text-navy">{app.score}/9</span>
                        </td>
                      ))}
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </section>
        </>
      )}

      {/* Empty state */}
      {selected.length < 2 && !loading && (
        <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-24">
          <div className="bg-surface border border-border border-dashed rounded-lg p-12 text-center">
            <div className="flex items-center justify-center gap-4 mb-4">
              <div className="w-16 h-16 rounded-full bg-page border-2 border-border flex items-center justify-center">
                <Shield className="w-7 h-7 text-text-muted" />
              </div>
              <ArrowRight className="w-5 h-5 text-text-muted" />
              <div className="w-16 h-16 rounded-full bg-page border-2 border-border flex items-center justify-center">
                <Shield className="w-7 h-7 text-text-muted" />
              </div>
              <ArrowRight className="w-5 h-5 text-text-muted hidden sm:block" />
              <div className="w-16 h-16 rounded-full bg-page border-2 border-dashed border-border flex items-center justify-center hidden sm:flex">
                <Plus className="w-6 h-6 text-text-muted" />
              </div>
            </div>
            <p className="text-text-muted text-sm">
              Select at least 2 apps above to see a side-by-side comparison
            </p>
          </div>
        </section>
      )}
    </main>
  )
}
