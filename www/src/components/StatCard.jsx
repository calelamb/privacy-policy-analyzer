export default function StatCard({ value, label, sublabel }) {
  return (
    <div className="bg-surface rounded-lg border border-border p-5 text-center">
      <p className="text-2xl font-bold text-navy">{value}</p>
      <p className="text-sm font-medium text-text-primary mt-1">{label}</p>
      {sublabel && <p className="text-xs text-text-muted mt-0.5">{sublabel}</p>}
    </div>
  )
}
