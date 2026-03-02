import { ExternalLink, BookOpen, Award, GraduationCap, MapPin } from 'lucide-react'
import SectionHeading from '../components/SectionHeading'

const professor = {
  name: 'Dr. Mark J. Keith',
  title: 'Associate Professor of Information Systems',
  affiliation: 'Marriott School of Business, Brigham Young University',
  bio: [
    'Dr. Mark J. Keith is an Associate Professor in the Department of Information Systems at BYU\u2019s Marriott School of Business. He earned his Ph.D. in Business Administration from Arizona State University in 2009, following a B.S. and MISM from Brigham Young University.',
    'With nearly 60 peer-reviewed publications, Dr. Keith\u2019s research spans information privacy and disclosure decision-making, behavioral impacts of machine learning, human-computer interaction, and educational technology. His work on healthcare data privacy, mobile device security, and consumer privacy decision-making has been cited over 2,500 times.',
    'Before returning to BYU, Dr. Keith held positions at the University of Alabama and West Texas A&M University. He is passionate about teaching business analytics and machine learning using Python and cloud services, integrating real-world data science applications with rigorous academic foundations.',
  ],
  research: [
    'Information Privacy & Disclosure Decision-Making',
    'Behavioral Impacts of Machine Learning Feedback',
    'Healthcare Data Privacy & Patient Practices',
    'Mobile Device Security & Authentication',
    'Educational Technology (Chatbots, Game-Based Learning)',
    'Team Dynamics in Virtual Environments',
    'Consumer Privacy for Mobile Applications',
  ],
  links: [
    { label: 'BYU Faculty Page', url: 'https://marriott.byu.edu/directory/details?id=29237' },
    { label: 'Google Scholar', url: 'https://scholar.google.com/citations?user=oo9iLzcAAAAJ' },
    { label: 'ResearchGate', url: 'https://www.researchgate.net/profile/Mark-Keith-3' },
  ],
}

const teamMembers = [
  {
    name: 'Cale Lamb',
    role: 'Research Assistant',
    major: 'Computer Science',
    gradYear: '2028',
    period: 'Sep 2025 \u2013 Present',
    contributions: [
      'Designed and built the full analysis pipeline (Python, OpenAI API, Pydantic)',
      'Implemented COPPA and GDPR compliance extraction modules',
      'Conducted multi-model evaluation (GPT-5-nano vs GPT-4o-mini vs GPT-4o)',
      'Built concurrent batch processing with rate limiting and crash recovery',
      'Performed KMeans cluster analysis and compliance scoring',
      'Analyzed 1,694+ privacy policies end-to-end',
    ],
  },
  {
    name: 'Luke Corbett',
    role: 'Research Assistant',
    major: 'Information Systems',
    gradYear: '2026',
    period: 'Sep 2025 \u2013 Present',
    contributions: [
      'Data analysis and visualization (Jupyter notebooks)',
      'Merged app metadata with policy analysis results',
      'Computed disclosure scores and compliance percentages',
    ],
  },
  {
    name: 'Preston Park',
    role: 'Research Assistant',
    major: 'Information Systems',
    gradYear: '2026',
    period: 'Sep 2025 \u2013 Present',
    contributions: [
      'Contribution details to be added',
    ],
  },
  {
    name: 'Mekeli Hiller',
    role: 'Research Assistant',
    major: 'Information Systems',
    gradYear: '2026',
    period: 'Sep 2025 \u2013 Present',
    contributions: [
      'Contribution details to be added',
    ],
  },
  {
    name: 'Asante Laryea-Akrong',
    role: 'Research Assistant',
    major: 'Information Systems',
    gradYear: '2026',
    period: 'Sep 2025 \u2013 Present',
    contributions: [
      'Contribution details to be added',
    ],
  },
  {
    name: 'Logan Spencer',
    role: 'Research Assistant',
    major: 'Information Systems',
    gradYear: '2026',
    period: 'Sep 2025 \u2013 Present',
    contributions: [
      'Contribution details to be added',
    ],
  },
]

export default function Team() {
  return (
    <main className="pt-14">
      {/* Page header */}
      <div className="bg-navy text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <p className="text-xs font-semibold uppercase tracking-[0.15em] text-byu-lightblue mb-2">
            Our Team
          </p>
          <h1
            className="text-3xl sm:text-4xl font-bold mb-3"
            style={{ fontFamily: "'Merriweather', serif" }}
          >
            The People Behind the Research
          </h1>
          <p className="text-white/70 max-w-2xl leading-relaxed">
            A team from BYU's Department of Information Systems, combining expertise in
            privacy research, data science, and software engineering.
          </p>
        </div>
      </div>

      {/* Principal Investigator */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-surface border border-border rounded-lg overflow-hidden">
          <div className="bg-navy/[0.03] border-b border-border px-6 py-3">
            <p className="text-xs font-semibold uppercase tracking-[0.15em] text-royal">
              Principal Investigator
            </p>
          </div>

          <div className="p-6 sm:p-8 lg:p-10">
            <div className="flex flex-col lg:flex-row gap-8 lg:gap-12">
              {/* Left column */}
              <div className="lg:w-72 shrink-0">
                <div className="w-32 h-32 rounded-lg bg-navy flex items-center justify-center mb-5">
                  <span className="text-3xl font-bold text-white">MK</span>
                </div>

                <h2
                  className="text-2xl font-bold text-navy mb-0.5"
                  style={{ fontFamily: "'Merriweather', serif" }}
                >
                  {professor.name}
                </h2>
                <p className="text-sm font-medium text-royal mb-0.5">{professor.title}</p>
                <p className="text-sm text-text-muted mb-5">{professor.affiliation}</p>

                <div className="space-y-2 mb-5 text-sm text-text-secondary">
                  <div className="flex items-center gap-2">
                    <GraduationCap className="w-4 h-4 text-text-muted" />
                    Ph.D., Arizona State University
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin className="w-4 h-4 text-text-muted" />
                    Provo, Utah
                  </div>
                  <div className="flex items-center gap-2">
                    <BookOpen className="w-4 h-4 text-text-muted" />
                    ~60 Peer-Reviewed Publications
                  </div>
                  <div className="flex items-center gap-2">
                    <Award className="w-4 h-4 text-text-muted" />
                    2,500+ Citations
                  </div>
                </div>

                <div className="space-y-1.5">
                  {professor.links.map(({ label, url }) => (
                    <a
                      key={label}
                      href={url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-1.5 text-sm text-royal hover:underline"
                    >
                      <ExternalLink className="w-3.5 h-3.5" />
                      {label}
                    </a>
                  ))}
                </div>
              </div>

              {/* Right column */}
              <div className="flex-1 min-w-0">
                <h3 className="text-xs font-semibold uppercase tracking-[0.15em] text-text-muted mb-3">
                  Biography
                </h3>
                <div className="space-y-3 mb-8">
                  {professor.bio.map((p, i) => (
                    <p key={i} className="text-sm text-text-secondary leading-relaxed">{p}</p>
                  ))}
                </div>

                <h3 className="text-xs font-semibold uppercase tracking-[0.15em] text-text-muted mb-3">
                  Research Interests
                </h3>
                <div className="flex flex-wrap gap-2">
                  {professor.research.map((area) => (
                    <span
                      key={area}
                      className="px-2.5 py-1 rounded bg-navy/5 border border-border text-sm text-text-primary"
                    >
                      {area}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Student Contributors */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-24">
        <SectionHeading
          eyebrow="Research Team"
          title="Student Contributors"
          description="Items marked \u201cTBD\u201d are placeholders to be updated with actual details."
        />

        <div className="grid md:grid-cols-2 gap-4">
          {teamMembers.map(({ name, role, major, gradYear, period, contributions }) => (
            <div key={name} className="bg-surface border border-border rounded-lg p-6 hover:shadow-sm transition-shadow">
              <div className="flex items-start gap-3 mb-4">
                <div className="w-11 h-11 rounded bg-navy/5 flex items-center justify-center shrink-0">
                  <span className="text-sm font-semibold text-navy">
                    {name.split(' ').map(n => n[0]).join('').slice(0, 2)}
                  </span>
                </div>
                <div>
                  <h3 className="font-semibold text-text-primary">{name}</h3>
                  <p className="text-sm text-royal">{role}</p>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3 mb-4">
                <div className="bg-page border border-border-light rounded px-3 py-2 text-center">
                  <p className="text-[10px] uppercase tracking-wider text-text-muted mb-0.5">Major</p>
                  <p className="text-xs font-medium text-text-primary">{major}</p>
                </div>
                <div className="bg-page border border-border-light rounded px-3 py-2 text-center">
                  <p className="text-[10px] uppercase tracking-wider text-text-muted mb-0.5">Graduation</p>
                  <p className="text-xs font-medium text-text-primary">{gradYear}</p>
                </div>
                <div className="bg-page border border-border-light rounded px-3 py-2 text-center">
                  <p className="text-[10px] uppercase tracking-wider text-text-muted mb-0.5">Period</p>
                  <p className="text-xs font-medium text-text-primary">{period}</p>
                </div>
              </div>

              <h4 className="text-[10px] font-semibold uppercase tracking-wider text-text-muted mb-2">Contributions</h4>
              <ul className="space-y-1.5">
                {contributions.map((c, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-text-secondary">
                    <span className="w-1 h-1 rounded-full bg-navy mt-2 shrink-0" />
                    {c}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}
