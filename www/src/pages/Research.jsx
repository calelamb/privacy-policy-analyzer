import { useState } from 'react'
import {
  Zap,
  CheckCircle2,
  XCircle,
  FileCode2,
  Cpu,
  Code2,
  Layers,
  FileDown,
  BookOpen,
  Shield,
  Database,
  Copy,
  Check,
} from 'lucide-react'
import SectionHeading from '../components/SectionHeading'

const indicators = [
  { name: 'Data Collection Disclosure', desc: 'Does the policy clearly disclose the types of personal data collected (PII, device details, usage data)?' },
  { name: 'Data Use Purpose Specification', desc: 'Does the policy specify purposes for data use AND limit use to those stated purposes?' },
  { name: 'Third-Party Sharing Disclosure', desc: 'Does the policy detail how student data is shared with third parties by name?' },
  { name: 'Parental Consent Mechanism', desc: 'Does the policy address obtaining verifiable parental consent for children\'s data (COPPA requirement)?' },
  { name: 'COPPA/FERPA Compliance Mention', desc: 'Does the policy explicitly mention COPPA or FERPA compliance?' },
  { name: 'Data Retention Policy', desc: 'Does the policy provide a data retention schedule or deletion timeframes?' },
  { name: 'User Data Rights', desc: 'Does the policy grant users/parents rights to access, correct, or delete their data?' },
  { name: 'Data Security & Encryption', desc: 'Does the policy mention security measures like encryption, secure servers, or access controls?' },
  { name: 'Tracking Technologies Disclosure', desc: 'Does the policy disclose use of cookies, web beacons, analytics, or tracking technologies?' },
]

const models = [
  {
    name: 'GPT-5-nano',
    verdict: 'Recommended',
    verdictColor: 'bg-byu-green/10 text-byu-green',
    cost: '$0.05 / 1M input',
    outputCost: '$0.40 / 1M output',
    perPolicy: '$0.0002 \u2013 $0.0005',
    at140k: '$30 \u2013 $70',
    reliability: '100%',
    notes: 'Best cost efficiency. 100% agreement with GPT-4o-mini on boolean fields. Selected as the production model for full-scale analysis.',
    icon: Zap,
  },
  {
    name: 'GPT-4o-mini',
    verdict: 'Runner-up',
    verdictColor: 'bg-royal/10 text-royal',
    cost: '~5\u00d7 more than nano',
    outputCost: '$0.60 / 1M output',
    perPolicy: '~$0.001 \u2013 $0.002',
    at140k: '$150 \u2013 $350',
    reliability: '100%',
    notes: '100% agreement with nano on boolean fields. Occasionally detects additional third-party entities. Very reliable but higher cost.',
    icon: CheckCircle2,
  },
  {
    name: 'GPT-4o',
    verdict: 'Not Recommended',
    verdictColor: 'bg-byu-orange/10 text-byu-orange',
    cost: '~90\u00d7 more than nano',
    outputCost: 'Significantly higher',
    perPolicy: '~$0.02 \u2013 $0.05',
    at140k: '$3,000 \u2013 $7,000',
    reliability: '90% (1/10 failure)',
    notes: 'Parsing failures at 1-in-10 rate. Less reliable than both nano and mini despite substantially higher cost. Not viable for large-scale work.',
    icon: XCircle,
  },
]

const coppaFields = [
  'Mentions COPPA (yes/no)',
  'Claims COPPA compliance (yes/no)',
  '11 categorized consent methods (signed form, credit card, phone call, video conference, government ID, knowledge-based auth, email+, school consent, other, not specified, N/A)',
  '7 exception categories (school authorization, one-time response, internal operations, child safety, multiple contact, none claimed, N/A)',
  'Age threshold stated',
]

const gdprFields = [
  'Mentions GDPR (yes/no)',
  'Claims GDPR compliance (yes/no)',
  '9 consent verification methods (written consent, email verification, parent account linking, video/phone, ID document, reasonable efforts, other, not specified, N/A)',
  '9 lawful bases claimed (consent, contract, legal obligation, vital interests, public task, legitimate interests, preventive counseling, not specified, N/A)',
  'Age threshold stated',
]

const timeline = [
  { date: 'Jan 14, 2026', title: 'Project Kickoff', desc: 'Initial commit with core analyzer architecture \u2014 Pydantic models, OpenAI integration, and CLI entry point.' },
  { date: 'Jan 21, 2026', title: 'Schema Refinement', desc: 'Cleaned output schema, removing unnecessary columns to streamline analysis output.' },
  { date: 'Feb 4, 2026', title: 'COPPA & GDPR Module', desc: 'Added detailed regulatory compliance extraction: consent methods, exceptions, lawful bases, and age thresholds.' },
  { date: 'Feb 4, 2026', title: 'Schema Compatibility Fix', desc: 'Resolved OpenAI structured output API limitations with Pydantic-generated JSON schemas.' },
  { date: 'Feb 4, 2026', title: 'Concurrent Processing', desc: 'Implemented async batch processing with configurable rate limiting for large-scale analysis.' },
  { date: 'Feb 4, 2026', title: 'Model Comparison', desc: 'Evaluated GPT-5-nano, GPT-4o-mini, and GPT-4o across cost, accuracy, and reliability metrics.' },
  { date: 'Feb 17, 2026', title: 'Cluster Analysis', desc: 'KMeans clustering on disclosure columns revealed three distinct compliance tiers.' },
]

const bibtex = `@inproceedings{keith2026edtech,
  title     = {Protecting Student Privacy in K-12 Educational Technology},
  author    = {Keith, Mark J. and Corbett, Luke and Hiller, Mekeli and Lamb, Cale and Laryea-Akrong, Asante and Park, Preston and Spencer, Logan},
  booktitle = {Proceedings of the Americas Conference on Information Systems (AMCIS)},
  year      = {2026},
  address   = {Minneapolis, MN},
  note      = {Forthcoming}
}`

function CiteAndEthics() {
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(bibtex).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }

  return (
    <section className="bg-surface border-y border-border">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 pb-24">
        <SectionHeading
          eyebrow="Attribution"
          title="Cite This Work"
        />

        <div className="max-w-3xl mx-auto space-y-6">
          {/* APA Citation */}
          <div className="bg-page border border-border rounded-lg p-6">
            <div className="flex items-center gap-2 mb-3">
              <BookOpen className="w-4 h-4 text-royal" />
              <h3 className="text-sm font-semibold text-text-primary">APA Citation</h3>
            </div>
            <p className="text-sm text-text-secondary leading-relaxed">
              Keith, M. J., Corbett, L., Hiller, M., Lamb, C., Laryea-Akrong, A., Park, P., &amp; Spencer, L. (2026). Protecting student privacy in K-12 educational technology. <em>Proceedings of the Americas Conference on Information Systems (AMCIS)</em>. Minneapolis, MN.
            </p>
          </div>

          {/* BibTeX */}
          <div className="bg-page border border-border rounded-lg p-6">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-text-primary">BibTeX</h3>
              <button
                onClick={handleCopy}
                className="inline-flex items-center gap-1.5 text-xs font-medium text-royal hover:text-navy transition-colors"
              >
                {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                {copied ? 'Copied' : 'Copy'}
              </button>
            </div>
            <pre className="text-xs text-text-secondary bg-navy/[0.03] rounded p-4 overflow-x-auto leading-relaxed">
              {bibtex}
            </pre>
          </div>

          {/* Ethics & Data */}
          <div className="grid md:grid-cols-2 gap-4">
            <div className="bg-page border border-border rounded-lg p-6">
              <div className="flex items-center gap-2 mb-3">
                <Shield className="w-4 h-4 text-royal" />
                <h3 className="text-sm font-semibold text-text-primary">Ethics Review</h3>
              </div>
              <p className="text-sm text-text-secondary leading-relaxed">
                This study's IRB status is under review with BYU's Institutional Review Board.
              </p>
            </div>

            <div className="bg-page border border-border rounded-lg p-6">
              <div className="flex items-center gap-2 mb-3">
                <Database className="w-4 h-4 text-royal" />
                <h3 className="text-sm font-semibold text-text-primary">Data Availability</h3>
              </div>
              <p className="text-sm text-text-secondary leading-relaxed">
                The analyzed dataset is available upon request. Contact the principal investigator for access.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default function Research() {
  return (
    <main className="pt-14">
      {/* Page header */}
      <div className="bg-navy text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <p className="text-xs font-semibold uppercase tracking-[0.15em] text-byu-lightblue mb-2">
            Methodology
          </p>
          <h1
            className="text-3xl sm:text-4xl font-bold mb-3"
            style={{ fontFamily: "'Merriweather', serif" }}
          >
            Research Design & Approach
          </h1>
          <p className="text-white/70 max-w-2xl leading-relaxed">
            Our pipeline combines large-language models with established privacy frameworks
            from Common Sense Media, the FTC, and iKeepSafe to evaluate K-12 app privacy practices at scale.
          </p>
          <a
            href="/AMCIS_2026_EdTech_Privacy_Policies.pdf"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 mt-4 bg-white/10 hover:bg-white/20 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
          >
            <FileDown className="w-4 h-4" />
            Download AMCIS 2026 Paper (PDF)
          </a>
        </div>
      </div>

      {/* 9 Indicators */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <SectionHeading
          eyebrow="Extraction Framework"
          title="9 Privacy Indicators"
          description="Each policy is evaluated against these boolean indicators derived from academic research on K-12 privacy risk assessment."
        />

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {indicators.map(({ name, desc }, i) => (
            <div key={name} className="bg-surface border border-border rounded-lg p-4 hover:shadow-sm transition-shadow">
              <div className="flex items-start gap-3">
                <span className="shrink-0 w-7 h-7 rounded bg-navy/5 flex items-center justify-center text-xs font-bold text-navy">
                  {i + 1}
                </span>
                <div>
                  <h3 className="font-semibold text-sm text-text-primary mb-1">{name}</h3>
                  <p className="text-xs text-text-muted leading-relaxed">{desc}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* COPPA & GDPR */}
      <section className="bg-surface border-y border-border">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <SectionHeading
            eyebrow="Regulatory Deep-Dive"
            title="COPPA & GDPR Analysis"
            description="Beyond the 9 boolean indicators, each policy is analyzed for detailed regulatory compliance across 22 additional fields."
          />

          <div className="grid md:grid-cols-2 gap-5">
            <div className="bg-page border border-border rounded-lg p-6">
              <div className="flex items-center gap-3 mb-5">
                <div className="w-9 h-9 rounded bg-royal/10 flex items-center justify-center">
                  <Layers className="w-4.5 h-4.5 text-royal" />
                </div>
                <div>
                  <h3 className="font-semibold text-text-primary">COPPA Compliance</h3>
                  <p className="text-xs text-text-muted">Children's Online Privacy Protection Act</p>
                </div>
              </div>
              <ul className="space-y-2.5">
                {coppaFields.map((f) => (
                  <li key={f} className="flex items-start gap-2 text-sm text-text-secondary">
                    <CheckCircle2 className="w-4 h-4 text-royal shrink-0 mt-0.5" />
                    {f}
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-page border border-border rounded-lg p-6">
              <div className="flex items-center gap-3 mb-5">
                <div className="w-9 h-9 rounded bg-navy/10 flex items-center justify-center">
                  <Layers className="w-4.5 h-4.5 text-navy" />
                </div>
                <div>
                  <h3 className="font-semibold text-text-primary">GDPR Compliance</h3>
                  <p className="text-xs text-text-muted">General Data Protection Regulation</p>
                </div>
              </div>
              <ul className="space-y-2.5">
                {gdprFields.map((f) => (
                  <li key={f} className="flex items-start gap-2 text-sm text-text-secondary">
                    <CheckCircle2 className="w-4 h-4 text-navy shrink-0 mt-0.5" />
                    {f}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Model Comparison */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <SectionHeading
          eyebrow="Model Evaluation"
          title="LLM Comparison"
          description="We compared three OpenAI models to find the optimal balance of cost, accuracy, and reliability for large-scale privacy policy analysis."
        />

        <div className="grid lg:grid-cols-3 gap-4">
          {models.map(({ name, verdict, verdictColor, cost, outputCost, perPolicy, at140k, reliability, notes, icon: Icon }) => (
            <div key={name} className="bg-surface border border-border rounded-lg p-6 hover:shadow-sm transition-shadow">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-text-primary">{name}</h3>
                <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${verdictColor}`}>
                  {verdict}
                </span>
              </div>

              <div className="space-y-2.5 text-sm mb-4">
                <div className="flex justify-between">
                  <span className="text-text-muted">Input Cost</span>
                  <span className="text-text-primary font-medium">{cost}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Output Cost</span>
                  <span className="text-text-primary font-medium">{outputCost}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Per Policy</span>
                  <span className="text-text-primary font-medium">{perPolicy}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Est. 140K Policies</span>
                  <span className="text-text-primary font-medium">{at140k}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Reliability</span>
                  <span className="text-text-primary font-medium">{reliability}</span>
                </div>
              </div>

              <p className="text-xs text-text-muted pt-3 border-t border-border leading-relaxed">
                {notes}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Tech Stack */}
      <section className="bg-surface border-y border-border">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <SectionHeading
            eyebrow="Implementation"
            title="Technical Architecture"
          />

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {[
              { icon: Code2, title: 'Python + Pydantic', desc: 'Type-safe structured outputs with schema validation' },
              { icon: Cpu, title: 'OpenAI API', desc: 'Structured output with JSON schema enforcement' },
              { icon: Zap, title: 'Async Processing', desc: 'Concurrent batch analysis with rate limiting' },
              { icon: FileCode2, title: 'Scikit-learn', desc: 'KMeans clustering for compliance tier analysis' },
            ].map(({ icon: Icon, title, desc }) => (
              <div key={title} className="bg-page border border-border rounded-lg p-5 text-center">
                <Icon className="w-6 h-6 text-navy mx-auto mb-2.5" />
                <h3 className="font-semibold text-sm text-text-primary mb-1">{title}</h3>
                <p className="text-xs text-text-muted">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Timeline */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <SectionHeading
          eyebrow="Development"
          title="Project Timeline"
        />

        <div className="max-w-2xl mx-auto">
          <div className="relative">
            <div className="absolute left-3 top-2 bottom-2 w-px bg-border" />
            <div className="space-y-6">
              {timeline.map(({ date, title, desc }, i) => (
                <div key={i} className="relative pl-10">
                  <div className="absolute left-1.5 top-1.5 w-3 h-3 rounded-full bg-navy border-2 border-page" />
                  <p className="text-xs font-medium text-royal mb-0.5">{date}</p>
                  <h3 className="text-sm font-semibold text-text-primary mb-0.5">{title}</h3>
                  <p className="text-sm text-text-secondary leading-relaxed">{desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Cite This Work & Ethics */}
      <CiteAndEthics />
    </main>
  )
}
