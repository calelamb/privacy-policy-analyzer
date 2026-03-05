# Lessons Learned

## Session: 2026-02-04

### Lesson 1: Always Check clauderc First
**Mistake:** Jumped straight into implementation without reading `.clauderc` guidelines.

**Rule:** At session start, check for `.clauderc` in home directory and project root. Follow workflow instructions before any non-trivial work.

**Pattern to avoid:** Starting implementation without plan mode or task tracking.

---

### Lesson 2: OpenAI Structured Output Schema Limitations
**Issue:** Pydantic's `model_json_schema()` generates schemas with `$ref`, `allOf`, and `anyOf` constructs that OpenAI's structured output API rejects.

**Solution:** Created `_make_openai_compatible_schema()` function to:
- Inline all `$ref` references
- Convert `anyOf` with null (Optional types) to base type only
- Merge `allOf` constructs
- Remove `title` fields

**Rule:** When using Pydantic models with OpenAI structured output, always post-process the schema for compatibility.

---

### Lesson 3: Plan Mode for Multi-File Changes
**Context:** Task required changes to 3 files (models.py, prompts.py, analyzer.py) with new enums, models, and integration code.

**Rule:** Any task touching 3+ files or adding new architectural components (enums, models, helper functions) should:
1. Enter plan mode
2. Write plan to `tasks/todo.md`
3. Get approval before implementing
4. Track progress with checkboxes

---
