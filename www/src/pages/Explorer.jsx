import { useState, useEffect, useMemo } from 'react'
import {
  Search,
  ChevronDown,
  ChevronUp,
  ChevronLeft,
  ChevronRight,
  Shield,
  ShieldAlert,
  ShieldCheck,
  CheckCircle,
  XCircle,
  Filter,
  ArrowUpDown,
} from 'lucide-react'
import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from 'recharts'
import SectionHeading from '../components/SectionHeading'

const INDICATOR_KEYS = [
  'data_collection_disclosure',
  'data_use_purpose_specification',
  'third_party_sharing_disclosure',
  'parental_consent_mechanism',
  'coppa_ferpa_compliance_mention',
  'data_retention_policy',
  'user_data_rights',
  'data_security_encryption',
  'tracking_technologies_disclosure',
]

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
  'User Rights',
  'Security',
  'Tracking',
]

const PER_PAGE = 20

const riskBadge = (risk) => {
  const styles = {
    Low: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    Medium: 'bg-amber-50 text-amber-700 border-amber-200',
    High: 'bg-red-50 text-red-700 border-red-200',
  }
  return styles[risk] || styles.Medium
}

const riskIcon = (risk) => {
  if (risk === 'Low') return <ShieldCheck className="w-4 h-4" />
  if (risk === 'High') return <ShieldAlert className="w-4 h-4" />
  return <Shield className="w-4 h-4" />
}

function ScoreBar({ score }) {
  const pct = (score / 9) * 100
  const color = score >= 7 ? '#00966C' : score >= 4 ? '#A39382' : '#D14124'
  return (
    <div className="flex items-center gap-2">
      <div className="w-20 bg-border-light rounded-full h-1.5">
        <div className="h-1.5 rounded-full transition-all" style={{ width: `${pct}%`, backgroundColor: color }} />
      </div>
      <span className="text-xs font-semibold text-text-primary w-6">{score}/9</span>
    </div>
  )
}

function AppDetail({ app }) {
  const radarData = RADAR_LABELS.map((label, i) => ({
    indicator: label,
    value: app.ind[i] ? 100 : 0,
  }))

  return (
    <tr>
      <td colSpan={5} className="p-0">
        <div className="bg-page border-t border-b border-royal/20 p-6 animate-in fade-in">
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Indicators */}
            <div className="lg:col-span-1">
              <h4 className="text-sm font-semibold text-text-primary mb-3">Privacy Indicators</h4>
              <div className="space-y-1.5">
                {INDICATOR_LABELS.map((label, i) => (
                  <div key={label} className="flex items-center justify-between text-sm">
                    <span className="text-text-secondary">{label}</span>
                    {app.ind[i] ? (
                      <CheckCircle className="w-4 h-4 text-emerald-600" />
                    ) : (
                      <XCircle className="w-4 h-4 text-red-400" />
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Radar */}
            <div className="lg:col-span-1">
              <h4 className="text-sm font-semibold text-text-primary mb-3">Compliance Radar</h4>
              <div className="h-[220px]">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={radarData} outerRadius="70%">
                    <PolarGrid stroke="#E5E7EB" />
                    <PolarAngleAxis dataKey="indicator" tick={{ fill: '#7C878E', fontSize: 10 }} />
                    <PolarRadiusAxis angle={90} domain={[0, 100]} tick={false} axisLine={false} />
                    <Radar dataKey="value" stroke="#002E5D" fill="#002E5D" fillOpacity={0.15} strokeWidth={2} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Summary */}
            <div className="lg:col-span-1">
              <h4 className="text-sm font-semibold text-text-primary mb-3">Regulatory Status</h4>
              <div className="space-y-3">
                <div className="bg-surface border border-border rounded-lg p-3">
                  <p className="text-xs text-text-muted mb-1">COPPA</p>
                  <div className="flex items-center gap-2 text-sm">
                    <span className="text-text-secondary">Mentions:</span>
                    <span className="font-medium">{app.coppa[0] ? 'Yes' : 'No'}</span>
                    <span className="text-text-muted mx-1">|</span>
                    <span className="text-text-secondary">Claims:</span>
                    <span className="font-medium">{app.coppa[1] ? 'Yes' : 'No'}</span>
                  </div>
                </div>
                <div className="bg-surface border border-border rounded-lg p-3">
                  <p className="text-xs text-text-muted mb-1">GDPR</p>
                  <div className="flex items-center gap-2 text-sm">
                    <span className="text-text-secondary">Mentions:</span>
                    <span className="font-medium">{app.gdpr[0] ? 'Yes' : 'No'}</span>
                    <span className="text-text-muted mx-1">|</span>
                    <span className="text-text-secondary">Claims:</span>
                    <span className="font-medium">{app.gdpr[1] ? 'Yes' : 'No'}</span>
                  </div>
                </div>
                <div className="bg-surface border border-border rounded-lg p-3">
                  <p className="text-xs text-text-muted mb-1">Third Parties</p>
                  <p className="text-lg font-bold text-navy">{app.tpCount}</p>
                  <p className="text-xs text-text-muted">entities identified</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </td>
    </tr>
  )
}

export default function Explorer() {
  const [apps, setApps] = useState([])
  const [loading, setLoading] = useState(true)
  const [query, setQuery] = useState('')
  const [riskFilter, setRiskFilter] = useState('All')
  const [sortBy, setSortBy] = useState('name')
  const [sortDir, setSortDir] = useState('asc')
  const [page, setPage] = useState(0)
  const [expandedId, setExpandedId] = useState(null)

  useEffect(() => {
    fetch('/apps.json')
      .then((r) => r.json())
      .then((data) => {
        setApps(data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  const filtered = useMemo(() => {
    let list = apps
    if (query) {
      const q = query.toLowerCase()
      list = list.filter((a) => a.name.toLowerCase().includes(q))
    }
    if (riskFilter !== 'All') {
      list = list.filter((a) => a.risk === riskFilter)
    }
    list = [...list].sort((a, b) => {
      let cmp = 0
      if (sortBy === 'name') cmp = a.name.localeCompare(b.name)
      else if (sortBy === 'score') cmp = a.score - b.score
      else if (sortBy === 'risk') {
        const order = { High: 0, Medium: 1, Low: 2 }
        cmp = order[a.risk] - order[b.risk]
      }
      return sortDir === 'asc' ? cmp : -cmp
    })
    return list
  }, [apps, query, riskFilter, sortBy, sortDir])

  const totalPages = Math.ceil(filtered.length / PER_PAGE)
  const pageApps = filtered.slice(page * PER_PAGE, (page + 1) * PER_PAGE)

  const toggleSort = (col) => {
    if (sortBy === col) setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'))
    else {
      setSortBy(col)
      setSortDir(col === 'name' ? 'asc' : 'desc')
    }
    setPage(0)
  }

  const stats = useMemo(() => {
    if (!apps.length) return {}
    const avgScore = (apps.reduce((s, a) => s + a.score, 0) / apps.length).toFixed(1)
    const high = apps.filter((a) => a.risk === 'High').length
    const low = apps.filter((a) => a.risk === 'Low').length
    return { total: apps.length, avgScore, high, low }
  }, [apps])

  return (
    <main className="pt-14">
      {/* Header */}
      <div className="bg-navy text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <p className="text-xs font-semibold uppercase tracking-[0.15em] text-byu-lightblue mb-2">
            Database
          </p>
          <h1
            className="text-3xl sm:text-4xl font-bold mb-3"
            style={{ fontFamily: "'Merriweather', serif" }}
          >
            App Explorer
          </h1>
          <p className="text-white/70 max-w-2xl leading-relaxed">
            Search and explore compliance profiles for {stats.total || '...'} educational apps
            analyzed in our study. Click any app to see its full privacy assessment.
          </p>
        </div>
      </div>

      {/* Stats bar */}
      {!loading && (
        <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 -mt-5 relative z-10 pb-6">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
            <div className="bg-surface border border-border border-l-4 border-l-royal rounded-lg p-4">
              <p className="text-xl font-bold text-navy">{stats.total}</p>
              <p className="text-sm font-medium text-text-primary mt-0.5">Apps Analyzed</p>
            </div>
            <div className="bg-surface border border-border border-l-4 border-l-navy rounded-lg p-4">
              <p className="text-xl font-bold text-navy">{stats.avgScore}/9</p>
              <p className="text-sm font-medium text-text-primary mt-0.5">Avg Score</p>
            </div>
            <div className="bg-surface border border-border border-l-4 border-l-byu-green rounded-lg p-4">
              <p className="text-xl font-bold text-navy">{stats.low}</p>
              <p className="text-sm font-medium text-text-primary mt-0.5">Low Risk</p>
            </div>
            <div className="bg-surface border border-border border-l-4 border-l-byu-orange rounded-lg p-4">
              <p className="text-xl font-bold text-navy">{stats.high}</p>
              <p className="text-sm font-medium text-text-primary mt-0.5">High Risk</p>
            </div>
          </div>
        </section>
      )}

      {/* Search + filters */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-4">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
            <input
              type="text"
              placeholder="Search apps by name..."
              className="w-full pl-9 pr-4 py-2.5 border border-border rounded-lg text-sm bg-surface text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-royal/40"
              value={query}
              onChange={(e) => {
                setQuery(e.target.value)
                setPage(0)
              }}
            />
          </div>
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-text-muted" />
            {['All', 'Low', 'Medium', 'High'].map((r) => (
              <button
                key={r}
                onClick={() => {
                  setRiskFilter(r)
                  setPage(0)
                }}
                className={`px-3 py-2 rounded-lg text-xs font-medium border transition-colors ${
                  riskFilter === r
                    ? 'bg-navy text-white border-navy'
                    : 'bg-surface text-text-secondary border-border hover:border-royal/40'
                }`}
              >
                {r === 'All' ? 'All Risk' : `${r} Risk`}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Results table */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-24">
        <div className="bg-surface border border-border rounded-lg overflow-hidden">
          {loading ? (
            <div className="p-12 text-center text-text-muted">Loading app database...</div>
          ) : filtered.length === 0 ? (
            <div className="p-12 text-center text-text-muted">No apps match your search.</div>
          ) : (
            <>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-border bg-page">
                      <th
                        className="text-left font-semibold text-text-muted text-xs uppercase tracking-wider px-6 py-3 cursor-pointer select-none hover:text-text-primary"
                        onClick={() => toggleSort('name')}
                      >
                        <span className="inline-flex items-center gap-1">
                          App Name
                          <ArrowUpDown className="w-3 h-3" />
                        </span>
                      </th>
                      <th
                        className="text-center font-semibold text-text-muted text-xs uppercase tracking-wider px-6 py-3 cursor-pointer select-none hover:text-text-primary"
                        onClick={() => toggleSort('score')}
                      >
                        <span className="inline-flex items-center gap-1">
                          Score
                          <ArrowUpDown className="w-3 h-3" />
                        </span>
                      </th>
                      <th
                        className="text-center font-semibold text-text-muted text-xs uppercase tracking-wider px-6 py-3 cursor-pointer select-none hover:text-text-primary"
                        onClick={() => toggleSort('risk')}
                      >
                        <span className="inline-flex items-center gap-1">
                          Risk
                          <ArrowUpDown className="w-3 h-3" />
                        </span>
                      </th>
                      <th className="text-center font-semibold text-text-muted text-xs uppercase tracking-wider px-6 py-3">
                        COPPA
                      </th>
                      <th className="text-center font-semibold text-text-muted text-xs uppercase tracking-wider px-6 py-3">
                        GDPR
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border">
                    {pageApps.map((app) => (
                      <>
                        <tr
                          key={app.id}
                          onClick={() => setExpandedId(expandedId === app.id ? null : app.id)}
                          className="hover:bg-page/50 transition-colors cursor-pointer"
                        >
                          <td className="px-6 py-3">
                            <div className="flex items-center gap-2">
                              {expandedId === app.id ? (
                                <ChevronUp className="w-4 h-4 text-text-muted flex-shrink-0" />
                              ) : (
                                <ChevronDown className="w-4 h-4 text-text-muted flex-shrink-0" />
                              )}
                              <span className="font-medium text-text-primary">{app.name}</span>
                            </div>
                          </td>
                          <td className="px-6 py-3">
                            <div className="flex justify-center">
                              <ScoreBar score={app.score} />
                            </div>
                          </td>
                          <td className="px-6 py-3 text-center">
                            <span
                              className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold border ${riskBadge(app.risk)}`}
                            >
                              {riskIcon(app.risk)}
                              {app.risk}
                            </span>
                          </td>
                          <td className="px-6 py-3 text-center">
                            {app.coppa[1] ? (
                              <CheckCircle className="w-4 h-4 text-emerald-600 inline" />
                            ) : (
                              <XCircle className="w-4 h-4 text-red-400 inline" />
                            )}
                          </td>
                          <td className="px-6 py-3 text-center">
                            {app.gdpr[1] ? (
                              <CheckCircle className="w-4 h-4 text-emerald-600 inline" />
                            ) : (
                              <XCircle className="w-4 h-4 text-red-400 inline" />
                            )}
                          </td>
                        </tr>
                        {expandedId === app.id && <AppDetail app={app} />}
                      </>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Pagination */}
              <div className="flex items-center justify-between px-6 py-3 border-t border-border bg-page">
                <p className="text-xs text-text-muted">
                  Showing {page * PER_PAGE + 1}–{Math.min((page + 1) * PER_PAGE, filtered.length)} of{' '}
                  {filtered.length} apps
                </p>
                <div className="flex items-center gap-1">
                  <button
                    onClick={() => setPage((p) => Math.max(0, p - 1))}
                    disabled={page === 0}
                    className="p-1.5 rounded border border-border hover:bg-surface disabled:opacity-30 disabled:cursor-not-allowed"
                  >
                    <ChevronLeft className="w-4 h-4" />
                  </button>
                  <span className="text-xs text-text-muted px-2">
                    {page + 1} / {totalPages}
                  </span>
                  <button
                    onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
                    disabled={page >= totalPages - 1}
                    className="p-1.5 rounded border border-border hover:bg-surface disabled:opacity-30 disabled:cursor-not-allowed"
                  >
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      </section>
    </main>
  )
}
