# Documentation Hub

This repository now separates documentation by audience so the research team does not have to dig through implementation notes or one-off files to find the current workflow.

## Recommended Reading Paths

| If you need to... | Read this |
| --- | --- |
| Understand the project at a high level | [Research team guide](research-team-guide.md) |
| Interpret output columns and scores | [Output reference](output-reference.md) |
| Maintain or extend the codebase | [Development guide](development-guide.md) |
| Find where things live in the repo | [Repository map](repository-map.md) |

## Current Source Of Truth

These files define the active v2 analyzer behavior:

- [`src/models.py`](../src/models.py) - structured output schema
- [`src/prompts.py`](../src/prompts.py) - extraction rules given to the model
- [`src/analyzer.py`](../src/analyzer.py) - core analysis pipeline, scoring, batch processing
- [`src/main.py`](../src/main.py) - CLI entry point
- [`resume_first_pass.py`](../resume_first_pass.py) - rerun failed or incomplete first-pass work
- [`second_pass.py`](../second_pass.py) - recover apps skipped for missing or short policy text
- [`cluster_analysis.py`](../cluster_analysis.py) - post-processing and clustering

## Current Status Notes

- The Python CLI pipeline is the authoritative v2 workflow.
- The API and website layers are still partly aligned to the older 9-indicator presentation. Treat them as prototypes until they are synchronized with the v2 schema.

## Reference Material

These files are useful background context, but they are not onboarding docs:

- [`IMPLEMENTATION_SPEC.md`](../IMPLEMENTATION_SPEC.md)
- [`model_comparison_report.md`](../model_comparison_report.md)
- [`tasks/todo.md`](../tasks/todo.md)
- [`tasks/lessons.md`](../tasks/lessons.md)
