# Research Team Guide

This guide is the fastest way to understand how the project is used in practice without reading the implementation files.

## What The Project Does

The analyzer reads privacy policy text for K-12 educational apps and produces:

- 35 boolean disclosure indicators aligned to the AMCIS 2026 Table 1 framework
- A short evidence field for each indicator
- Third-party sharing details
- Nested COPPA and GDPR summary fields
- Composite GDPR, COPPA, and overall compliance scores

The extraction logic is intentionally conservative. If a policy does not explicitly say something, the analyzer is supposed to mark it absent.

## Typical Workflow

### 1. Prepare the environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your OpenAI API key to `.env`:

```bash
OPENAI_API_KEY=...
```

### 2. Run the main analysis

For the current dataset in this repo, the first-pass command is:

```bash
python -m src.main "Master Data.csv" "data/output/full_results_v2.csv" \
  --policy-column-primary ppCompany \
  --model gpt-5.4 \
  --concurrent \
  --max-concurrent 20
```

What happens during that run:

1. Each row is matched by `app_id` and optionally `app_name`.
2. Policy text is resolved from the requested column, or from `ppCompany` and `ppPlatform` when needed.
3. Policies under 100 characters are skipped with `error = empty_or_short_policy`.
4. Successful analyses are written to the output CSV with periodic checkpoint saves.

### 3. Resume if the run stops

```bash
python resume_first_pass.py
```

This script reuses `data/output/full_results_v2.csv`, keeps successful rows, retries `analysis_failed` rows, and appends anything not yet processed.

### 4. Recover skipped apps with richer policy text

```bash
python second_pass.py
```

This script:

1. Reads apps skipped in the first pass because the policy text was too short.
2. Pulls matching apps from `privacy policy dataset finished.csv`.
3. Re-runs analysis on rows with usable text.
4. Writes a merged file to `data/output/full_results_v2_merged.csv`.

### 5. Optionally cluster the final results

```bash
python cluster_analysis.py data/output/full_results_v2_merged.csv
```

This adds a `compliance_cluster` label and a `compliance_score` percentage for downstream comparison work.

## Input Expectations

The active workflow expects these columns:

| Column | Purpose |
| --- | --- |
| `app_id` | stable row identifier |
| `app_name` | human-readable app name |
| `ppCompany` | vendor privacy policy text |
| `ppPlatform` | app-store privacy label or alternate policy text |

Policy selection logic in the analyzer:

1. Use the requested policy column if it contains at least 100 characters.
2. Otherwise prefer `ppCompany` when it is substantive.
3. Use `ppPlatform` if the company policy is missing or too short.
4. Concatenate both when neither alone is ideal but useful text exists.

## Main Output Files

| File | What it contains |
| --- | --- |
| `data/output/full_results_v2.csv` | first-pass batch output |
| `data/output/full_results_v2_resume.csv` | temporary resume output before merge |
| `data/output/second_pass_results.csv` | recovered rows from the second pass |
| `data/output/full_results_v2_merged.csv` | recommended post-recovery dataset |
| `*_clustered.csv` | clustering-enriched output from `cluster_analysis.py` |

## How To Read The Results

- Boolean indicator columns are the primary compliance calls.
- Every boolean indicator has a matching `_evidence` column.
- Composite score columns summarize how many indicators were satisfied:
  - `gdpr_composite_score`
  - `gdpr_composite_pct`
  - `coppa_composite_score`
  - `coppa_composite_pct`
  - `overall_composite_score`
  - `overall_composite_pct`
- `error` is blank for successful analyses and populated for skips or failed API calls.

See [Output reference](output-reference.md) for the full schema.

## Important Project Reality

The Python batch pipeline is the authoritative research workflow. The API and web app are useful for demos, but parts of that layer still assume the older 9-indicator version and should not be treated as the primary research interface until they are updated.
