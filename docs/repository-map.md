# Repository Map

This file explains what lives where and which parts of the repository are active, experimental, or historical.

## Active Code Paths

| Path | Status | Notes |
| --- | --- | --- |
| `src/` | active | core v2 analyzer, schema, prompt, and CLI |
| `resume_first_pass.py` | active | retries failed or unfinished first-pass work |
| `second_pass.py` | active | recovers skipped apps from the richer dataset |
| `cluster_analysis.py` | active | clustering and score augmentation |
| `data/input/` | active | place small local input files here |
| `data/output/` | active | analyzer outputs, merged files, reports |
| `docs/` | active | organized documentation for this repo |

## Web And API

| Path | Status | Notes |
| --- | --- | --- |
| `api/` | prototype | FastAPI wrapper around the analyzer |
| `www/` | prototype | React/Vite site for public-facing research presentation |

Important caveat:

- The core analyzer is v2 and uses 35 indicators.
- Parts of `api/` and `www/` still assume the older 9-indicator workflow.

## Legacy Or One-Off Utilities

| Path | Status | Notes |
| --- | --- | --- |
| `src/summary_analyzer.py` | legacy | older summary-field analyzer |
| `tests/test_analyzer.py` | legacy | tests for the older schema |
| `check_columns.py` | utility | helper for inspecting new CSV or Excel files |
| `create_test_sample.py` | utility | one-off dataset sampling helper |
| `test_api.py` | utility | quick API key connectivity check |

## Research Artifacts And Notes

The root directory also contains supporting material that is useful context but not part of the active runtime:

| Path | Type |
| --- | --- |
| `IMPLEMENTATION_SPEC.md` | implementation brief used during the v2 refactor |
| `model_comparison_report.md` | benchmark report |
| `tasks/todo.md` | working notes |
| `tasks/lessons.md` | lessons learned log |
| `*.docx`, `*.pdf`, `*.tt`, `lukescript.txt*` | research artifacts and background material |

## Large Working Data Files In Root

Several large CSV files live at the repository root because they are working research datasets:

- `Master Data.csv`
- `privacy policy dataset finished.csv`
- `appmicroscope_data_clean_cert - appmicroscope_data_clean_cert.csv`
- sample CSVs used during iteration

If the repo is cleaned up further later, those files are the most likely candidates for a dedicated `data/raw/` or `data/reference/` layout.
