import { Link } from 'react-router-dom'
import {
  Shield,
  FileSearch,
  Brain,
  BarChart3,
  ArrowRight,
  Database,
  Scale,
  Lock,
  Search,
  GitCompareArrows,
  Sparkles,
  Award,
} from 'lucide-react'
import StatCard from '../components/StatCard'

const highlights = [
  {
    icon: FileSearch,
    title: 'Automated Policy Analysis',
    desc: 'AI-powered extraction of 9 key privacy indicators from thousands of K-12 app privacy policies using structured LLM outputs.',
  },
  {
    icon: Scale,
    title: 'Regulatory Compliance',
    desc: 'Detailed COPPA and GDPR compliance analysis including consent methods, exceptions, lawful bases, and age thresholds.',
  },
  {
    icon: Brain,
    title: 'Multi-Model Evaluation',
    desc: 'Rigorous comparison of GPT-5-nano, GPT-4o-mini, and GPT-4o for cost, accuracy, and reliability at scale.',
  },
  {
    icon: BarChart3,
    title: 'Cluster Analysis',
    desc: 'KMeans clustering reveals three distinct compliance tiers among educational apps, from critically low to highly compliant.',
  },
]

export default function Home() {
  return (
    <main>
      {/* Hero */}
      <section className="bg-navy text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-28 pb-20">
          <div className="flex flex-wrap items-center gap-3 mb-4">
            <p className="text-xs font-semibold uppercase tracking-[0.15em] text-byu-lightblue">
              BYU EdTech Privacy Lab
            </p>
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-white/10 text-xs font-semibold text-white">
              <Award className="w-3 h-3" />
              Accepted at AMCIS 2026
            </span>
          </div>
          <h1
            className="text-4xl sm:text-5xl font-bold leading-tight mb-5 max-w-3xl"
            style={{ fontFamily: "'Merriweather', serif" }}
          >
            Protecting Student Privacy in K-12 Educational Technology
          </h1>
          <p className="text-lg text-white/70 leading-relaxed max-w-2xl mb-8">
            Researching privacy practices in K-12 educational technology. Our flagship
            study analyzes privacy policies across nearly 1,700 educational applications,
            examining how well the industry safeguards children's data under COPPA and GDPR.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link
              to="/results"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded bg-white text-navy text-sm font-semibold hover:bg-white/90 transition-colors"
            >
              View Findings
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link
              to="/research"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded border border-white/30 text-white/90 text-sm font-semibold hover:bg-white/10 transition-colors"
            >
              Methodology
            </Link>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 -mt-6 relative z-10 pb-16">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <StatCard value="1,694" label="Policies Analyzed" sublabel="K-12 educational apps" />
          <StatCard value="9" label="Privacy Indicators" sublabel="Per policy extracted" />
          <StatCard value="3" label="LLM Models Compared" sublabel="Cost & accuracy evaluated" />
          <StatCard value="22" label="Regulatory Fields" sublabel="COPPA + GDPR compliance" />
        </div>
      </section>

      {/* What We Do */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <p className="text-xs font-semibold uppercase tracking-[0.15em] text-royal mb-2">
            Research Focus
          </p>
          <h2
            className="text-2xl sm:text-3xl font-bold text-navy mb-3"
            style={{ fontFamily: "'Merriweather', serif" }}
          >
            Comprehensive Privacy Intelligence
          </h2>
          <p className="text-text-secondary max-w-2xl mx-auto">
            Our research combines large-language models with established privacy frameworks
            from Common Sense Media, the FTC, and iKeepSafe to systematically evaluate K-12 app privacy practices.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          {highlights.map(({ icon: Icon, title, desc }) => (
            <div
              key={title}
              className="bg-surface border border-border rounded-lg p-6 hover:shadow-sm transition-shadow"
            >
              <div className="w-10 h-10 rounded bg-navy/5 flex items-center justify-center text-navy mb-4">
                <Icon className="w-5 h-5" />
              </div>
              <h3 className="text-base font-semibold text-text-primary mb-1.5">{title}</h3>
              <p className="text-sm text-text-secondary leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Pipeline */}
      <section className="bg-surface border-y border-border">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center mb-12">
            <p className="text-xs font-semibold uppercase tracking-[0.15em] text-royal mb-2">
              Pipeline
            </p>
            <h2
              className="text-2xl sm:text-3xl font-bold text-navy"
              style={{ fontFamily: "'Merriweather', serif" }}
            >
              Analysis Workflow
            </h2>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { step: '1', title: 'Collect', desc: 'Gather privacy policies from K-12 educational app stores and vendor websites.' },
              { step: '2', title: 'Extract', desc: 'Process each policy through GPT-5-nano with structured output schemas via the OpenAI API.' },
              { step: '3', title: 'Analyze', desc: 'Score 9 boolean indicators plus detailed COPPA and GDPR consent and compliance fields.' },
              { step: '4', title: 'Cluster', desc: 'Apply KMeans clustering to reveal compliance tiers and identify systemic gaps.' },
            ].map(({ step, title, desc }) => (
              <div key={step} className="relative bg-page border border-border rounded-lg p-5">
                <span className="text-4xl font-bold text-navy/5 absolute top-3 right-4">
                  {step}
                </span>
                <h3 className="text-sm font-semibold text-navy mb-1.5">{title}</h3>
                <p className="text-sm text-text-secondary leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Interactive Tools */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <p className="text-xs font-semibold uppercase tracking-[0.15em] text-royal mb-2">
            Interactive Tools
          </p>
          <h2
            className="text-2xl sm:text-3xl font-bold text-navy mb-3"
            style={{ fontFamily: "'Merriweather', serif" }}
          >
            Explore the Data
          </h2>
          <p className="text-text-secondary max-w-2xl mx-auto">
            Go beyond the aggregate findings. Analyze any policy, search our database
            of {' '}897 apps, or compare tools side-by-side.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-4">
          <Link
            to="/analyze"
            className="group bg-surface border border-border rounded-lg p-6 hover:border-royal/40 hover:shadow-md transition-all"
          >
            <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-royal/10 to-navy/10 flex items-center justify-center text-royal mb-4 group-hover:scale-110 transition-transform">
              <Sparkles className="w-6 h-6" />
            </div>
            <h3 className="text-base font-semibold text-text-primary mb-1.5 group-hover:text-royal transition-colors">
              Analyze a Policy
            </h3>
            <p className="text-sm text-text-secondary leading-relaxed mb-4">
              Paste any privacy policy and get an instant AI-powered compliance assessment with downloadable reports.
            </p>
            <span className="inline-flex items-center gap-1 text-sm font-medium text-royal">
              Try it <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </span>
          </Link>

          <Link
            to="/explorer"
            className="group bg-surface border border-border rounded-lg p-6 hover:border-royal/40 hover:shadow-md transition-all"
          >
            <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-byu-green/10 to-navy/10 flex items-center justify-center text-byu-green mb-4 group-hover:scale-110 transition-transform">
              <Search className="w-6 h-6" />
            </div>
            <h3 className="text-base font-semibold text-text-primary mb-1.5 group-hover:text-royal transition-colors">
              App Explorer
            </h3>
            <p className="text-sm text-text-secondary leading-relaxed mb-4">
              Search our database of 897 K-12 apps with compliance scores, risk levels, and detailed indicator breakdowns.
            </p>
            <span className="inline-flex items-center gap-1 text-sm font-medium text-royal">
              Search apps <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </span>
          </Link>

          <Link
            to="/compare"
            className="group bg-surface border border-border rounded-lg p-6 hover:border-royal/40 hover:shadow-md transition-all"
          >
            <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-byu-orange/10 to-navy/10 flex items-center justify-center text-byu-orange mb-4 group-hover:scale-110 transition-transform">
              <GitCompareArrows className="w-6 h-6" />
            </div>
            <h3 className="text-base font-semibold text-text-primary mb-1.5 group-hover:text-royal transition-colors">
              Compare Apps
            </h3>
            <p className="text-sm text-text-secondary leading-relaxed mb-4">
              Place up to 3 apps side-by-side with overlaid radar charts and indicator-by-indicator comparisons.
            </p>
            <span className="inline-flex items-center gap-1 text-sm font-medium text-royal">
              Compare <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </span>
          </Link>
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="bg-navy rounded-lg p-10 sm:p-14 text-center text-white">
          <h2
            className="text-2xl sm:text-3xl font-bold mb-3"
            style={{ fontFamily: "'Merriweather', serif" }}
          >
            Explore the Full Results
          </h2>
          <p className="text-white/70 max-w-lg mx-auto mb-6">
            Compliance rates, cluster breakdowns, and regulatory gaps
            across nearly 1,700 K-12 educational applications.
          </p>
          <div className="flex flex-wrap justify-center gap-3">
            <Link
              to="/results"
              className="inline-flex items-center gap-2 px-6 py-2.5 rounded bg-white text-navy text-sm font-semibold hover:bg-white/90 transition-colors"
            >
              View Results
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link
              to="/explorer"
              className="inline-flex items-center gap-2 px-6 py-2.5 rounded border border-white/30 text-white/90 text-sm font-semibold hover:bg-white/10 transition-colors"
            >
              Browse All Apps
            </Link>
          </div>
        </div>
      </section>
    </main>
  )
}
