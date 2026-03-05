import { ExternalLink, FileDown } from 'lucide-react'

const resources = [
  {
    category: 'App Privacy Databases',
    items: [
      {
        name: 'ISL AppMicroscope',
        url: 'https://appmicroscope.net',
        description:
          'Interactive database for exploring app privacy behaviors, permissions, and data practices across thousands of mobile applications.',
      },
      {
        name: 'Common Sense Media Privacy Program',
        url: 'https://privacy.commonsense.org',
        description:
          'Independent privacy evaluations of popular edtech products used in K-12 classrooms, with detailed ratings and pass/fail assessments.',
      },
      {
        name: 'Student Data Privacy Consortium (SDPC)',
        url: 'https://privacy.a4l.org',
        description:
          'Collaborative effort helping schools and vendors manage student data privacy through standardized agreements and a searchable registry.',
      },
    ],
  },
  {
    category: 'Government Registries',
    items: [
      {
        name: 'California Data Broker Registry',
        url: 'https://oag.ca.gov/data-brokers',
        description:
          'Official registry of data brokers required to register under the California Delete Act, maintained by the CA Attorney General.',
      },
      {
        name: "FTC Children's Privacy",
        url: 'https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa',
        description:
          'Federal Trade Commission resources on COPPA enforcement, rulemaking, and compliance guidance for operators of child-directed services.',
      },
    ],
  },
  {
    category: 'Research & Reports',
    items: [
      {
        name: "Common Sense Media — State of Kids' Privacy",
        url: 'https://www.commonsensemedia.org/kids-action/research',
        description:
          "Annual research reports examining the state of children's privacy across apps, platforms, and connected devices.",
      },
      {
        name: 'iKeepSafe COPPA & FERPA Resources',
        url: 'https://ikeepsafe.org',
        description:
          'Certification body and resource hub for COPPA, FERPA, and state-level student privacy compliance in edtech products.',
      },
      {
        name: 'Future of Privacy Forum — K-12 Resources',
        url: 'https://fpf.org/issues/k-12-education/',
        description:
          'Research, toolkits, and policy recommendations for protecting student privacy in educational technology from a leading think tank.',
      },
    ],
  },
]

export default function Resources() {
  return (
    <main className="pt-14">
      {/* Header */}
      <div className="bg-navy text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <p className="text-xs font-semibold uppercase tracking-[0.15em] text-byu-lightblue mb-2">
            Reference
          </p>
          <h1
            className="text-3xl sm:text-4xl font-bold mb-3"
            style={{ fontFamily: "'Merriweather', serif" }}
          >
            Privacy Resources
          </h1>
          <p className="text-white/70 max-w-2xl leading-relaxed">
            Curated links to major privacy databases, government registries, and research
            organizations relevant to K-12 edtech data protection.
          </p>
        </div>
      </div>

      {/* Our Research — AMCIS Paper */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 -mt-5 relative z-10 pb-6">
        <a
          href="/AMCIS_2026_EdTech_Privacy_Policies.pdf"
          target="_blank"
          rel="noopener noreferrer"
          className="group block bg-surface border border-border border-l-4 border-l-royal rounded-lg p-6 hover:shadow-sm transition-all"
        >
          <div className="flex items-start justify-between gap-4">
            <div>
              <span className="inline-block text-[10px] font-semibold uppercase tracking-wider text-royal bg-royal/10 rounded px-2 py-0.5 mb-2">
                Our Research — AMCIS 2026
              </span>
              <h3 className="text-base font-semibold text-text-primary group-hover:text-royal transition-colors mb-1">
                The State of Privacy Policy Regulatory Compliance for Educational Technology
              </h3>
              <p className="text-sm text-text-muted leading-relaxed max-w-3xl">
                Full paper analyzing 1,500 EdTech privacy policies across U.S. school districts,
                evaluating adherence to COPPA and GDPR disclosure requirements using LLM-based
                structured extraction. Accepted at AMCIS 2026.
              </p>
            </div>
            <FileDown className="w-5 h-5 text-text-muted flex-shrink-0 mt-1 group-hover:text-royal transition-colors" />
          </div>
        </a>
      </section>

      {/* Resource sections */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10 pb-24">
        {resources.map((section) => (
          <section key={section.category}>
            <h2 className="text-lg font-semibold text-text-primary mb-4">{section.category}</h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {section.items.map((item) => (
                <a
                  key={item.name}
                  href={item.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group bg-surface border border-border rounded-lg p-5 hover:border-royal/40 hover:shadow-sm transition-all"
                >
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <h3 className="text-sm font-semibold text-text-primary group-hover:text-royal transition-colors">
                      {item.name}
                    </h3>
                    <ExternalLink className="w-4 h-4 text-text-muted flex-shrink-0 mt-0.5 group-hover:text-royal transition-colors" />
                  </div>
                  <p className="text-xs text-text-muted leading-relaxed">{item.description}</p>
                  <span className="inline-block mt-3 text-[10px] font-semibold uppercase tracking-wider text-text-muted bg-page border border-border rounded px-2 py-0.5">
                    {section.category}
                  </span>
                </a>
              ))}
            </div>
          </section>
        ))}
      </div>
    </main>
  )
}
