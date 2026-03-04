import { ExternalLink, BookOpen, Award, GraduationCap, MapPin, Mail } from 'lucide-react'
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
    name: 'Luke Corbett',
    role: 'Research Assistant',
    major: 'Information Systems',
    gradYear: '2026',
    period: 'Sep 2025 \u2013 Present',
  },
  {
    name: 'Mekeli Hiller',
    role: 'Research Assistant',
    major: 'Information Systems',
    gradYear: '2026',
    period: 'Sep 2025 \u2013 Present',
  },
  {
    name: 'Cale Lamb',
    role: 'Research Assistant',
    major: 'Computer Science',
    gradYear: '2028',
    period: 'Sep 2025 \u2013 Present',
  },
  {
    name: 'Asante Laryea-Akrong',
    role: 'Research Assistant',
    major: 'Information Systems',
    gradYear: '2026',
    period: 'Sep 2025 \u2013 Present',
  },
  {
    name: 'Preston Park',
    role: 'Research Assistant',
    major: 'Information Systems',
    gradYear: '2026',
    period: 'Sep 2025 \u2013 Present',
  },
  {
    name: 'Logan Spencer',
    role: 'Research Assistant',
    major: 'Information Systems',
    gradYear: '2026',
    period: 'Sep 2025 \u2013 Present',
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

      {/* Contact */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-10">
        <div className="bg-surface border border-border rounded-lg p-6 flex flex-col sm:flex-row items-start sm:items-center gap-4">
          <div className="w-10 h-10 rounded bg-royal/10 flex items-center justify-center shrink-0">
            <Mail className="w-5 h-5 text-royal" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-text-primary mb-0.5">Contact</h3>
            <p className="text-sm text-text-secondary">
              For inquiries about the lab, collaboration, or data access, reach out to the principal investigator.
            </p>
          </div>
          <div className="flex flex-wrap gap-3 text-sm">
            <a
              href="mailto:mark_keith@byu.edu"
              className="inline-flex items-center gap-1.5 text-royal hover:underline font-medium"
            >
              mark_keith@byu.edu
            </a>
            <a
              href="https://marriott.byu.edu/directory/details?id=29237"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-royal hover:underline font-medium"
            >
              <ExternalLink className="w-3.5 h-3.5" />
              Faculty Page
            </a>
          </div>
        </div>
      </section>

      {/* Student Contributors */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-24">
        <SectionHeading
          eyebrow="Research Team"
          title="Student Contributors"
        />

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {teamMembers.map(({ name, role, major, gradYear, period }) => (
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

              <div className="grid grid-cols-3 gap-3">
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
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}
