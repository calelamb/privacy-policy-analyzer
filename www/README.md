# Website

This folder contains the React/Vite frontend used to present the research project and provide an interactive analysis experience.

## Commands

```bash
npm install
npm run dev
npm run build
npm run preview
npm run lint
```

The Vite dev server proxies `/api` requests to `http://localhost:8000`, so the FastAPI backend should be running when you test the interactive analyzer:

```bash
uvicorn api.main:app --reload
```

## What Lives Here

| Path | Purpose |
| --- | --- |
| `src/App.jsx` | top-level routing |
| `src/pages/` | public site pages |
| `src/components/` | shared layout and UI components |
| `src/index.css` | global styling and theme |
| `public/` | static assets, including the AMCIS paper PDF |

## Current Status

This frontend is useful for demos and research presentation, but it is not fully synchronized with the current v2 analyzer:

- The Python CLI analyzer now returns a 35-indicator schema.
- The interactive `Analyze` page still expects the older 9-indicator result shape.
- Some static results pages also reflect older snapshot metrics.

Treat the frontend as a presentation layer until the UI and API are updated to the current v2 output contract.

For the authoritative research workflow, use the Python documentation in:

- [`../docs/research-team-guide.md`](../docs/research-team-guide.md)
- [`../docs/output-reference.md`](../docs/output-reference.md)
