# Privacy Policy Analyzer

Research toolkit for analyzing K-12 edtech privacy policies against GDPR and COPPA disclosure requirements. The current v2 pipeline extracts 35 table-aligned indicators, supporting evidence, third-party sharing details, and composite compliance scores from policy text.

## Start Here

- [Documentation hub](docs/README.md)
- [Research team guide](docs/research-team-guide.md)
- [Output reference](docs/output-reference.md)
- [Development guide](docs/development-guide.md)
- [Repository map](docs/repository-map.md)

## Quick Start

Install Python dependencies and configure your API key:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then add `OPENAI_API_KEY` to `.env` and run a batch analysis:

```bash
python -m src.main "Master Data.csv" "data/output/full_results_v2.csv" \
  --policy-column-primary ppCompany \
  --model gpt-5.4 \
  --concurrent \
  --max-concurrent 20
```

Common follow-up commands:

```bash
python resume_first_pass.py
python second_pass.py
python cluster_analysis.py data/output/full_results_v2_merged.csv
```

## What Is Current

- `src/` is the source of truth for the v2 analyzer.
- `resume_first_pass.py`, `second_pass.py`, and `cluster_analysis.py` are the active batch-processing utilities.
- `docs/` contains the organized project documentation for researchers and developers.

## What Needs Caution

- `api/` and `www/` exist and are useful for demos, but parts of that stack still reflect the older 9-indicator workflow rather than the current 35-indicator v2 schema.
- `src/summary_analyzer.py` and `tests/test_analyzer.py` are legacy 9-indicator artifacts and should not be treated as the current research pipeline.

## Reference Material

- [Implementation spec](IMPLEMENTATION_SPEC.md)
- [Model comparison report](model_comparison_report.md)
- [Task notes](tasks/todo.md)
- [Lessons learned](tasks/lessons.md)
