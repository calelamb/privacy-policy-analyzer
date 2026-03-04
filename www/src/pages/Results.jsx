import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
} from 'recharts'
import SectionHeading from '../components/SectionHeading'

const complianceData = [
  { short: 'Third-Party Sharing', rate: 79.2, count: 1105 },
  { short: 'Data Collection', rate: 77.6, count: 1083 },
  { short: 'Tracking Tech', rate: 76.9, count: 1073 },
  { short: 'User Data Rights', rate: 75.5, count: 1053 },
  { short: 'Data Retention', rate: 64.7, count: 903 },
  { short: 'Data Use Purpose', rate: 62.1, count: 866 },
  { short: 'Security', rate: 62.1, count: 866 },
  { short: 'COPPA/FERPA', rate: 42.7, count: 595 },
  { short: 'Parental Consent', rate: 32.1, count: 448 },
]

const radarData = [
  { indicator: '3rd Party', value: 79.2 },
  { indicator: 'Collection', value: 77.6 },
  { indicator: 'Tracking', value: 76.9 },
  { indicator: 'User Rights', value: 75.5 },
  { indicator: 'Retention', value: 64.7 },
  { indicator: 'Purpose', value: 62.1 },
  { indicator: 'Security', value: 62.1 },
  { indicator: 'COPPA/FERPA', value: 42.7 },
  { indicator: 'Consent', value: 32.1 },
]

const clusterData = [
  { name: 'Low Compliance', score: 4.25, count: 574, color: '#D14124', pct: '33.9%' },
  { name: 'Moderate', score: 55.63, count: 676, color: '#A39382', pct: '39.9%' },
  { name: 'High Compliance', score: 83.28, count: 444, color: '#00966C', pct: '26.2%' },
]

const regulatoryData = [
  { name: 'Mention COPPA', rate: 41.7, count: 582, fill: '#002E5D' },
  { name: 'Claim COPPA', rate: 36.6, count: 510, fill: '#0047BA' },
  { name: 'Mention GDPR', rate: 43.9, count: 613, fill: '#002E5D' },
  { name: 'Claim GDPR', rate: 22.7, count: 316, fill: '#0047BA' },
]

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white border border-border rounded px-3 py-2 shadow-sm text-sm">
        <p className="font-medium text-text-primary mb-0.5">{label?.replace('\n', ' ')}</p>
        <p className="text-royal font-semibold">{payload[0].value}%</p>
        {payload[0].payload.count && (
          <p className="text-xs text-text-muted">{payload[0].payload.count.toLocaleString()} of 1,395</p>
        )}
      </div>
    )
  }
  return null
}

export default function Results() {
  return (
    <main className="pt-14">
      {/* Page header */}
      <div className="bg-navy text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <p className="text-xs font-semibold uppercase tracking-[0.15em] text-byu-lightblue mb-2">
            Findings
          </p>
          <h1
            className="text-3xl sm:text-4xl font-bold mb-3"
            style={{ fontFamily: "'Merriweather', serif" }}
          >
            Analysis Results
          </h1>
          <p className="text-white/70 max-w-2xl leading-relaxed">
            Key findings from 1,694 K-12 educational app privacy policies (1,395 valid).
            The data reveals significant gaps in regulatory compliance and transparency.
            Data current as of February 2026.
          </p>
        </div>
      </div>

      {/* Key Takeaways */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 -mt-5 relative z-10 pb-10">
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {[
            { label: 'Highest Compliance', value: '79.2%', desc: 'Third-party sharing disclosure', color: 'border-l-byu-green' },
            { label: 'Lowest Compliance', value: '32.1%', desc: 'Parental consent mechanism', color: 'border-l-byu-orange' },
            { label: 'Low-Compliance Apps', value: '574', desc: '33.9% of all analyzed apps', color: 'border-l-byu-orange' },
            { label: 'GDPR Claim Gap', value: '21.2%', desc: 'Mention but don\'t claim compliance', color: 'border-l-royal' },
          ].map(({ label, value, desc, color }) => (
            <div key={label} className={`bg-surface border border-border border-l-4 ${color} rounded-lg p-4`}>
              <p className="text-xl font-bold text-navy">{value}</p>
              <p className="text-sm font-medium text-text-primary mt-0.5">{label}</p>
              <p className="text-xs text-text-muted mt-0.5">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Bar Chart */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="bg-surface border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-text-primary mb-1">Privacy Indicator Compliance Rates</h3>
          <p className="text-sm text-text-muted mb-6">Percentage of valid policies (n=1,395) meeting each indicator</p>
          <div className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={complianceData} layout="vertical" margin={{ left: 20, right: 30, top: 5, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                <XAxis type="number" domain={[0, 100]} tick={{ fill: '#7C878E', fontSize: 12 }} tickFormatter={(v) => `${v}%`} />
                <YAxis type="category" dataKey="short" tick={{ fill: '#1a1a2e', fontSize: 12 }} width={120} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="rate" radius={[0, 4, 4, 0]} fill="#002E5D" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      {/* Radar + Clusters */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid lg:grid-cols-2 gap-5">
          {/* Radar */}
          <div className="bg-surface border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-text-primary mb-1">Compliance Radar</h3>
            <p className="text-sm text-text-muted mb-4">Overall shape of K-12 app privacy compliance</p>
            <div className="h-[320px]">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData} outerRadius="70%">
                  <PolarGrid stroke="#E5E7EB" />
                  <PolarAngleAxis dataKey="indicator" tick={{ fill: '#7C878E', fontSize: 11 }} />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fill: '#C7C9C7', fontSize: 10 }} />
                  <Radar
                    dataKey="value"
                    stroke="#002E5D"
                    fill="#002E5D"
                    fillOpacity={0.15}
                    strokeWidth={2}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Clusters */}
          <div className="bg-surface border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-text-primary mb-1">Compliance Clusters</h3>
            <p className="text-sm text-text-muted mb-4">KMeans clustering reveals three distinct tiers</p>
            <div className="h-[180px] mb-5">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={clusterData}
                    dataKey="count"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    innerRadius={45}
                    outerRadius={80}
                    paddingAngle={2}
                    strokeWidth={0}
                  >
                    {clusterData.map((entry, i) => (
                      <Cell key={i} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const d = payload[0].payload
                        return (
                          <div className="bg-white border border-border rounded px-3 py-2 shadow-sm text-sm">
                            <p className="font-medium text-text-primary">{d.name}</p>
                            <p className="text-xs text-text-muted">{d.count} apps ({d.pct})</p>
                            <p className="text-xs text-text-muted">Avg score: {d.score}%</p>
                          </div>
                        )
                      }
                      return null
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="space-y-2.5">
              {clusterData.map(({ name, score, count, color, pct }) => (
                <div key={name} className="flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: color }} />
                    <span className="text-sm text-text-primary">{name}</span>
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-semibold text-text-primary">{score}%</span>
                    <span className="text-xs text-text-muted ml-1.5">({count} apps)</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Regulatory */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="bg-surface border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-text-primary mb-1">Regulatory Compliance: COPPA vs. GDPR</h3>
          <p className="text-sm text-text-muted mb-6">
            A notable gap exists between apps that <em>mention</em> GDPR and those that <em>claim</em> compliance (43.9% vs. 22.7%).
          </p>
          <div className="h-[280px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={regulatoryData} margin={{ left: 10, right: 30, top: 5, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                <XAxis dataKey="name" tick={{ fill: '#1a1a2e', fontSize: 12 }} interval={0} />
                <YAxis domain={[0, 50]} tick={{ fill: '#7C878E', fontSize: 12 }} tickFormatter={(v) => `${v}%`} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="rate" radius={[4, 4, 0, 0]}>
                  {regulatoryData.map((entry, i) => (
                    <Cell key={i} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      {/* Table */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 pb-24">
        <div className="bg-surface border border-border rounded-lg overflow-hidden">
          <div className="p-6 pb-3">
            <h3 className="text-lg font-semibold text-text-primary mb-0.5">Detailed Compliance Breakdown</h3>
            <p className="text-sm text-text-muted">All 9 privacy indicators across 1,395 valid policies</p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-t border-border bg-page">
                  <th className="text-left font-semibold text-text-muted text-xs uppercase tracking-wider px-6 py-3">Indicator</th>
                  <th className="text-right font-semibold text-text-muted text-xs uppercase tracking-wider px-6 py-3">Compliant</th>
                  <th className="text-right font-semibold text-text-muted text-xs uppercase tracking-wider px-6 py-3">Non-Compliant</th>
                  <th className="text-right font-semibold text-text-muted text-xs uppercase tracking-wider px-6 py-3">Rate</th>
                  <th className="text-left font-semibold text-text-muted text-xs uppercase tracking-wider px-6 py-3 w-44"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {complianceData.map(({ short, rate, count }) => (
                  <tr key={short} className="hover:bg-page/50 transition-colors">
                    <td className="px-6 py-3 font-medium text-text-primary">{short}</td>
                    <td className="px-6 py-3 text-right text-text-secondary">{count.toLocaleString()}</td>
                    <td className="px-6 py-3 text-right text-text-muted">{(1395 - count).toLocaleString()}</td>
                    <td className="px-6 py-3 text-right font-semibold text-navy">{rate}%</td>
                    <td className="px-6 py-3">
                      <div className="w-full bg-border-light rounded-full h-1.5">
                        <div
                          className="h-1.5 rounded-full"
                          style={{
                            width: `${rate}%`,
                            backgroundColor: rate >= 70 ? '#00966C' : rate >= 50 ? '#A39382' : '#D14124',
                          }}
                        />
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </main>
  )
}
