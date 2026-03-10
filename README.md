# Privacy Policy Analyzer — K-12 EdTech (v2)

An automated tool for analyzing privacy policies of K-12 educational applications against GDPR and COPPA regulatory frameworks. Version 2 extracts **35 boolean indicators** that map 1:1 to Table 1 of the AMCIS 2026 paper, along with evidence strings, nuance fields, and composite regulatory scores.

---

## What's New in v2

| Feature | v1 | v2 |
|---|---|---|
| Indicators | 9 broad booleans | 35 specific booleans (Table 1) |
| Evidence strings | None | Every indicator has a companion `_evidence` field |
| Regulatory scores | None | GDPR %, COPPA %, Overall % composite scores |
| Nuance fields | None | Sharing direction, retention specificity, security specificity, consent specificity |
| Retention period | Not extracted | Literal phrase extracted verbatim from policy |
| Model | gpt-4o / gpt-5-nano | GPT-5.4 (temperature=0, deterministic) |
| Policy source | Single column | Runtime construction from `ppCompany` + `ppPlatform` |

---

## Quick Start

### Installation

```bash
git clone <repository-url>
cd privacy_policy_analyzer
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key to .env
```

### Full Dataset Run

```bash
python -m src.main "Master Data.csv" data/output/results.csv \
  --policy-column-primary ppCompany \
  --model gpt-5.4 \
  --concurrent \
  --max-concurrent 20
```

### Resume an Interrupted Run

```bash
python resume_first_pass.py
```

Automatically detects which apps were successfully analyzed and retries only the failures. Safe to re-run multiple times.

### Second Pass (Recover Skipped Apps)

```bash
python second_pass.py
```

Runs the analyzer on apps that were skipped due to missing/short policy text in `Master Data.csv`, pulling richer policy text from `privacy policy dataset finished.csv`. Merges results into `data/output/full_results_v2_merged.csv`.

---

## Input Format

The input CSV must contain:

| Column | Required | Description |
|---|---|---|
| `app_id` | Yes | Unique identifier |
| `app_name` | No | Application name |
| `ppCompany` | Preferred | Vendor's full privacy policy text |
| `ppPlatform` | Fallback | Platform (Apple/Google) privacy policy text |

The analyzer automatically constructs policy text at runtime:
1. `ppCompany` if ≥ 200 chars (preferred)
2. `ppPlatform` if `ppCompany` is short/absent and `ppPlatform` ≥ 200 chars
3. Concatenation of both if each is ≥ 100 chars
4. Apps with < 100 chars combined are skipped (`error = empty_or_short_policy`)

---

## Output Format

The output CSV has **102 columns**. Key column groups:

### Identifiers
- `app_id`, `app_name`, `error`

### 35 Boolean Indicators (TRUE/FALSE)
All indicators from Table 1, grouped by regulatory category:

**Controller Identity (ci_)**
`ci_controller_identity`, `ci_dpo_contact`, `ci_operator_list`

**Policy Accessibility (pa_)**
`pa_concise_transparent`, `pa_prominent_link`

**Transparency & Data (td_)**
`td_categories_disclosed`, `td_persistent_identifiers`, `td_sensitive_data`, `td_indirect_data_source`

**Purpose & Use (pu_)**
`pu_purposes_stated`, `pu_children_purpose`, `pu_secondary_use`

**Third-Party Sharing (ts_)**
`ts_recipients_disclosed`, `ts_third_party_purpose`, `ts_international_transfers`

**Retention & Erasure (re_)**
`re_retention_period`, `re_retention_specificity` *(enum)*, `re_retention_stated_period` *(literal phrase)*, `re_children_retention`

**Security (sec_)**
`sec_measures_listed`, `sec_specificity` *(enum)*, `sec_breach_notification`, `sec_coppa_safeguards`

**Consent Mechanisms (cm_)**
`cm_consent_required`, `cm_parental_consent_procedures`, `cm_consent_specificity` *(enum)*

**User Rights — GDPR (ur_)**
`ur_right_access`, `ur_right_rectification`, `ur_right_erasure`, `ur_right_restriction`,
`ur_right_portability`, `ur_right_objection`, `ur_right_withdraw_consent`, `ur_right_supervisory_complaint`

**User Rights — COPPA Parental (ur_)**
`ur_parent_review_right`, `ur_parent_deletion_right`, `ur_parent_refuse_right`

**Administration & Profiling (adm_)**
`adm_profiling_disclosure`, `adm_automated_decision`

**Data Sharing Direction (re_)**
`re_sharing_direction` *(enum)*

### Evidence Fields
Every boolean indicator has a companion `_evidence` field (e.g., `ci_controller_identity_evidence`) containing the exact quote or paraphrase from the policy the model used to reach its conclusion. For FALSE indicators, the evidence explains what language would be needed to satisfy the requirement.

### Composite Scores
- `gdpr_composite_score` — count of GDPR indicators TRUE (out of 21)
- `gdpr_composite_pct` — GDPR score as percentage
- `coppa_composite_score` — count of COPPA indicators TRUE (out of 15)
- `coppa_composite_pct` — COPPA score as percentage
- `overall_composite_score` — count across all 35 indicators
- `overall_composite_pct` — overall score as percentage

### Enum Field Values

| Field | Possible Values |
|---|---|
| `re_sharing_direction` | `shares`, `does_not_share`, `conditional`, `vague_or_silent` |
| `re_retention_specificity` | `specific_timeframe`, `until_deleted`, `as_long_as_necessary`, `indefinite_or_silent` |
| `sec_specificity` | `specific_measures`, `general_language`, `silent` |
| `cm_consent_specificity` | `method_described`, `mentioned_no_method`, `not_applicable` |

---

## CLI Options

```bash
python -m src.main INPUT OUTPUT [options]

Options:
  --model               Model to use (default: gpt-5.4)
                        Choices: gpt-5.4, gpt-5.1, gpt-4.1, gpt-4.1-mini,
                                 gpt-4o, gpt-4o-mini, gpt-5-nano, gpt-3.5-turbo
  --policy-column       Primary policy text column (default: policy_text)
  --policy-column-primary  Alternative primary column with ppCompany/ppPlatform fallback
  --concurrent          Enable async concurrent processing
  --max-concurrent N    Max parallel API requests (default: 10, recommended: 20)
  --delay SECONDS       Delay between requests in non-concurrent mode (default: 0.5)
```

---

## Dataset Results (Full Run — March 2026)

| Metric | Value |
|---|---|
| Total apps in dataset | 1,694 |
| Successfully analyzed | 1,592 |
| Skipped (no policy text) | 100 |
| Failed | 2 (Matific, Newsweek) |
| Mean overall score | 36.9% |
| Mean GDPR score | 48.1% |
| Mean COPPA score | 23.9% |
| Model used | GPT-5.4 |
| Estimated cost | ~$45 |

### Key Findings
- `ci_operator_list`: 0.0% — no app provides the COPPA-required operator list
- `cm_parental_consent_procedures`: 4.6% — virtually no apps describe how they obtain parental consent
- `pa_concise_transparent`: 3.3% — almost no policies meet the concise/transparent accessibility standard
- GDPR user rights (access, erasure, rectification) score 64–72% — better disclosed than COPPA-specific requirements

---

## Project Structure

```
privacy_policy_analyzer/
├── src/
│   ├── main.py              # CLI entry point
│   ├── analyzer.py          # Core analysis logic, composite scoring
│   ├── models.py            # Pydantic output schema (35 indicators)
│   └── prompts.py           # System prompt (14 regulatory categories)
├── cluster_analysis.py      # KMeans clustering on Table 1 indicators
├── resume_first_pass.py     # Resume an interrupted analysis run
├── second_pass.py           # Second pass for skipped apps
├── data/
│   ├── input/               # Input datasets
│   └── output/              # Analysis results
│       └── K12_Privacy_Analysis_v2_Full_Dataset.csv  # Final merged dataset
└── www/                     # Research website (React/Vite)
```

---

## Research Context

This tool was developed as part of a BYU K-12 EdTech Privacy study accepted at **AMCIS 2026**. The 35 indicators align with the paper's Table 1 regulatory framework, enabling reproducible automated analysis at scale.

A companion platform, **SafeApps Utah**, is under development to make this data accessible to Utah K-12 teachers and administrators.
