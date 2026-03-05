import { useState } from 'react'
import { ChevronDown, ChevronRight } from 'lucide-react'

const federalLaws = [
  {
    name: 'COPPA',
    fullName: "Children's Online Privacy Protection Act",
    year: 1998,
    summary:
      'Requires operators of websites and online services directed at children under 13 to obtain verifiable parental consent before collecting personal information.',
    provisions: [
      'Verifiable parental consent required before data collection',
      'Clear and comprehensive privacy policy',
      'Data minimization — collect only what is necessary',
      'Parental right to review and delete child data',
      'Reasonable data security measures',
    ],
    protects: 'Children under 13',
    enforcement: 'Federal Trade Commission (FTC)',
  },
  {
    name: 'FERPA',
    fullName: 'Family Educational Rights and Privacy Act',
    year: 1974,
    summary:
      'Protects the privacy of student education records and gives parents rights to access and control disclosure of their children\'s records.',
    provisions: [
      'Parents can inspect and review education records',
      'Schools must have consent to release records',
      'Directory information may be disclosed with notice',
      'Rights transfer to student at age 18',
      'Applies to schools receiving federal funding',
    ],
    protects: 'Students in federally funded schools (K-12 and higher ed)',
    enforcement: 'U.S. Department of Education',
  },
  {
    name: 'PPRA',
    fullName: 'Protection of Pupil Rights Amendment',
    year: 1978,
    summary:
      'Protects students from surveys, analyses, or evaluations that reveal sensitive information without prior parental consent.',
    provisions: [
      'Parental consent for surveys on sensitive topics',
      'Parents can opt out of certain data collection activities',
      'Schools must notify parents of data collection policies',
      'Covers third-party surveys used in schools',
    ],
    protects: 'Students in programs funded by the U.S. Department of Education',
    enforcement: 'U.S. Department of Education',
  },
]

const stateLaws = [
  {
    state: 'California',
    laws: [
      {
        name: 'SOPIPA',
        fullName: 'Student Online Personal Information Protection Act',
        year: 2014,
        summary:
          'Prohibits operators of K-12 school-purpose websites from using student data for non-educational purposes, targeted advertising, or selling student information.',
        provisions: [
          'Ban on targeted advertising based on student data',
          'Prohibition on selling student information',
          'Required data security practices',
          'Deletion of data upon request from school or district',
        ],
      },
      {
        name: 'CCPA / CPRA',
        fullName: 'California Consumer Privacy Act / California Privacy Rights Act',
        year: '2018 / 2020',
        summary:
          'Gives California consumers broad rights over their personal information including the right to know, delete, opt out of sale, and non-discrimination.',
        provisions: [
          'Right to know what data is collected',
          'Right to delete personal information',
          'Right to opt out of data sales and sharing',
          'Enhanced protections for minors under 16',
        ],
      },
    ],
  },
  {
    state: 'Illinois',
    laws: [
      {
        name: 'BIPA',
        fullName: 'Biometric Information Privacy Act',
        year: 2008,
        summary:
          'Regulates collection and storage of biometric data (fingerprints, facial recognition, etc.) with informed consent requirements and private right of action.',
        provisions: [
          'Written consent required before collecting biometrics',
          'Published retention and destruction schedule',
          'Prohibition on selling biometric data',
          'Private right of action for violations',
        ],
      },
      {
        name: 'SOPPA',
        fullName: 'Student Online Personal Protection Act',
        year: 2021,
        summary:
          'Strengthens student data protections by requiring transparency from edtech vendors and limiting commercial use of student data.',
        provisions: [
          'Data processing agreements required with vendors',
          'Parents can review and correct student data',
          'Prohibition on targeted advertising using student data',
          'Annual data security breach notification',
        ],
      },
    ],
  },
  {
    state: 'Colorado',
    laws: [
      {
        name: 'CPA',
        fullName: 'Colorado Privacy Act',
        year: 2021,
        summary:
          'Comprehensive consumer privacy law giving Colorado residents rights over personal data, with specific provisions for data protection assessments.',
        provisions: [
          'Right to access, correct, and delete data',
          'Right to opt out of targeted advertising',
          'Data protection assessments for high-risk processing',
          'Universal opt-out mechanism support',
        ],
      },
    ],
  },
  {
    state: 'Other Notable States',
    laws: [
      {
        name: 'Various',
        fullName: 'Student Privacy Laws in 40+ States',
        year: '2014–2025',
        summary:
          'Over 40 states have enacted student privacy legislation. Common provisions include restrictions on commercial use of student data, data breach notification requirements, and transparency mandates for edtech vendors.',
        provisions: [
          'Connecticut, Virginia, Utah — comprehensive privacy acts',
          'New York — Education Law §2-d for student data',
          'Texas — SCOPE Act and student privacy protections',
          'Maryland — Student Data Privacy Act',
        ],
      },
    ],
  },
]

function LawCard({ law }) {
  const [open, setOpen] = useState(false)

  return (
    <div className="bg-surface border border-border rounded-lg overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between p-5 text-left hover:bg-page/50 transition-colors"
      >
        <div>
          <div className="flex items-center gap-2.5 flex-wrap">
            <span className="text-sm font-semibold text-navy">{law.name}</span>
            <span className="text-[10px] font-semibold uppercase tracking-wider text-text-muted bg-page border border-border rounded px-2 py-0.5">
              {law.year}
            </span>
          </div>
          <p className="text-xs text-text-muted mt-0.5">{law.fullName}</p>
        </div>
        {open ? (
          <ChevronDown className="w-4 h-4 text-text-muted flex-shrink-0" />
        ) : (
          <ChevronRight className="w-4 h-4 text-text-muted flex-shrink-0" />
        )}
      </button>

      {open && (
        <div className="px-5 pb-5 border-t border-border pt-4 space-y-3 text-sm">
          <p className="text-text-secondary leading-relaxed">{law.summary}</p>

          <div>
            <p className="font-medium text-text-primary text-xs uppercase tracking-wider mb-1.5">
              Key Provisions
            </p>
            <ul className="space-y-1">
              {law.provisions.map((p, i) => (
                <li key={i} className="flex items-start gap-2 text-text-secondary">
                  <span className="text-royal mt-1">&#8226;</span>
                  {p}
                </li>
              ))}
            </ul>
          </div>

          {law.protects && (
            <div className="flex gap-2">
              <span className="font-medium text-text-primary text-xs uppercase tracking-wider">
                Protects:
              </span>
              <span className="text-text-secondary text-xs">{law.protects}</span>
            </div>
          )}

          {law.enforcement && (
            <div className="flex gap-2">
              <span className="font-medium text-text-primary text-xs uppercase tracking-wider">
                Enforcement:
              </span>
              <span className="text-text-secondary text-xs">{law.enforcement}</span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default function Legislation() {
  return (
    <main className="pt-14">
      {/* Header */}
      <div className="bg-navy text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <p className="text-xs font-semibold uppercase tracking-[0.15em] text-byu-lightblue mb-2">
            Legal Landscape
          </p>
          <h1
            className="text-3xl sm:text-4xl font-bold mb-3"
            style={{ fontFamily: "'Merriweather', serif" }}
          >
            Privacy Legislation
          </h1>
          <p className="text-white/70 max-w-2xl leading-relaxed">
            Federal and state privacy laws relevant to K-12 educational technology.
            Understanding this legal landscape is essential for evaluating edtech privacy practices.
          </p>
        </div>
      </div>

      {/* Federal laws */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <h2 className="text-lg font-semibold text-text-primary mb-4">Federal Laws</h2>
        <div className="space-y-3">
          {federalLaws.map((law) => (
            <LawCard key={law.name} law={law} />
          ))}
        </div>
      </section>

      {/* State laws */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 pb-24">
        <h2 className="text-lg font-semibold text-text-primary mb-4">State Laws</h2>
        <div className="space-y-8">
          {stateLaws.map((group) => (
            <div key={group.state}>
              <h3 className="text-sm font-semibold text-text-muted uppercase tracking-wider mb-3">
                {group.state}
              </h3>
              <div className="space-y-3">
                {group.laws.map((law) => (
                  <LawCard key={law.name + group.state} law={law} />
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}
