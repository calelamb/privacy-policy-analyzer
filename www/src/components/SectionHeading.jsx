export default function SectionHeading({ eyebrow, title, description }) {
  return (
    <div className="max-w-2xl mx-auto text-center mb-12">
      {eyebrow && (
        <p className="text-xs font-semibold uppercase tracking-[0.15em] text-royal mb-2">
          {eyebrow}
        </p>
      )}
      <h2 className="text-2xl sm:text-3xl font-bold text-navy mb-3" style={{ fontFamily: "'Merriweather', serif" }}>
        {title}
      </h2>
      {description && (
        <p className="text-text-secondary leading-relaxed">
          {description}
        </p>
      )}
    </div>
  )
}
