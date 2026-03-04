import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="bg-navy text-white/70">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 text-sm">
          <div>
            <p className="font-semibold text-white mb-2">BYU EdTech Privacy Lab</p>
            <p className="leading-relaxed">
              Analyzing privacy practices in K-12 educational technology to protect student data.
            </p>
          </div>

          <div>
            <p className="font-semibold text-white mb-2">Research</p>
            <div className="space-y-1.5">
              <Link to="/" className="block hover:text-white transition-colors">Home</Link>
              <Link to="/research" className="block hover:text-white transition-colors">Research</Link>
              <Link to="/results" className="block hover:text-white transition-colors">Results</Link>
              <Link to="/team" className="block hover:text-white transition-colors">Team</Link>
            </div>
          </div>

          <div>
            <p className="font-semibold text-white mb-2">Tools</p>
            <div className="space-y-1.5">
              <Link to="/analyze" className="block hover:text-white transition-colors">Analyze a Policy</Link>
              <Link to="/explorer" className="block hover:text-white transition-colors">App Explorer</Link>
              <Link to="/compare" className="block hover:text-white transition-colors">Compare Apps</Link>
              <Link to="/resources" className="block hover:text-white transition-colors">Resources</Link>
              <Link to="/legislation" className="block hover:text-white transition-colors">Legislation</Link>
            </div>
          </div>

          <div>
            <p className="font-semibold text-white mb-2">Affiliation</p>
            <p className="leading-relaxed">
              Department of Information Systems<br />
              Marriott School of Business<br />
              Brigham Young University<br />
              Provo, Utah
            </p>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-white/10 text-center text-xs text-white/40 space-y-1">
          <p>AMCIS 2026 &middot; K-12 EdTech Privacy Policy Research &middot; Brigham Young University</p>
          <p>Supported by the Department of Information Systems, Marriott School of Business &middot; Site updated March 2026</p>
        </div>
      </div>
    </footer>
  )
}
