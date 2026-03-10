# Development Guide

This guide is for maintainers working on the codebase rather than just consuming the CSV outputs.

## Architecture Overview

The active pipeline is centered on the Python CLI:

1. `src/main.py` parses CLI arguments and chooses batch or single-file mode.
2. `src/analyzer.py` resolves policy text, calls the OpenAI API with a strict JSON schema, flattens the result, and computes composite scores.
3. `src/models.py` defines the structured output schema used for extraction.
4. `src/prompts.py` contains the extraction instructions that drive the model behavior.
5. Support scripts rerun failures, recover skipped policies, and cluster the final dataset.

## Active Python Modules

| Path | Role |
| --- | --- |
| `src/main.py` | CLI entry point |
| `src/analyzer.py` | core analysis, batch processing, usage tracking, schema flattening |
| `src/models.py` | Pydantic schema for structured outputs |
| `src/prompts.py` | system prompt with 14 regulatory categories |
| `resume_first_pass.py` | resume failed or partial first-pass runs |
| `second_pass.py` | retry skipped rows with alternate source text |
| `cluster_analysis.py` | clustering and downstream scoring |
| `api/main.py` | FastAPI wrapper for the interactive site |

## Structured Output Flow

The analyzer depends on a strict JSON-schema round trip:

1. `PolicyAnalysisResult` in `src/models.py` defines the canonical response shape.
2. `src/analyzer.py` converts the Pydantic schema into an OpenAI-compatible schema.
3. The chat completion is requested with `response_format = json_schema`.
4. The returned nested structure is flattened into CSV-friendly columns.
5. Composite scores are computed in Python after the model response.

Because of that design, schema changes usually require coordinated edits in:

- `src/models.py`
- `src/prompts.py`
- `src/analyzer.py`
- any downstream scripts that depend on column names

## Batch Processing Utilities

### Main CLI

```bash
python -m src.main INPUT OUTPUT [options]
```

Important flags:

- `--policy-column`
- `--policy-column-primary`
- `--id-column`
- `--name-column`
- `--model`
- `--concurrent`
- `--max-concurrent`
- `--resume-from`

### Resume flow

`resume_first_pass.py` keeps successful rows, retries failures, and rewrites the merged first-pass output.

### Second-pass flow

`second_pass.py` isolates `empty_or_short_policy` rows, looks them up in `privacy policy dataset finished.csv`, and merges recovered results back into a final dataset.

### Clustering flow

`cluster_analysis.py` clusters the analyzed dataset using a selected subset of interpretable boolean indicators.

## API And Web Layer

The repo also contains:

- `api/` - a FastAPI backend
- `www/` - a React/Vite frontend

Current status:

- The UI is useful as a presentation and demo surface.
- The `Analyze` page and `api/main.py` still assume the older 9-indicator scoring model.
- The Python batch CLI is therefore the only fully current v2 implementation.

If you update the interactive stack, plan to sync:

- `api/main.py`
- `www/src/pages/Analyze.jsx`
- any result visualizations based on legacy fields

## Legacy Or Drifted Files

These files are still worth keeping, but they do not describe the current v2 workflow:

| Path | Status |
| --- | --- |
| `src/summary_analyzer.py` | older 9-indicator summary-based analyzer |
| `tests/test_analyzer.py` | tests written against the older 9-indicator schema |
| `www/src/pages/Analyze.jsx` | interactive page tied to the older 9-indicator result model |
| `www/src/pages/Results.jsx` | static results page based on older snapshot values |

## Useful Commands

### Python

```bash
python -m src.main --help
python resume_first_pass.py
python second_pass.py
python cluster_analysis.py --help
```

### API

```bash
uvicorn api.main:app --reload
```

### Frontend

```bash
cd www
npm run dev
npm run build
```

## Editing Guidelines For Future Documentation

- Keep the root `README.md` short and directional.
- Put detailed operational guidance under `docs/`.
- When workflows change, update the docs hub first so readers know which guide is authoritative.
- If a file reflects an older workflow, label it clearly rather than letting it look current by accident.
