# Sprint P2.2 — React Frontend (Form + Loading + Output/Error)

**Phase:** Phase 2: Minimum Viable Product (MVP)  
**Status:** completed  
**Sprint Goal:** Build React frontend with URL input form, loading state, summary display, and error handling.

---

## Tasks

| Task ID | Description | Status |
|--------|-------------|--------|
| [TSK-0207](../tasks/TSK-0207-sprint-p2-2-react-form.md) | Build React component with URL input + submit button | completed |
| [TSK-0208](../tasks/TSK-0208-sprint-p2-2-loading-state.md) | Implement loading indicator during API call | completed |
| [TSK-0209](../tasks/TSK-0209-sprint-p2-2-summary-display.md) | Display summary output component | completed |
| [TSK-0210](../tasks/TSK-0210-sprint-p2-2-error-handling.md) | Error banner for structured errors | completed |
| [TSK-0211](../tasks/TSK-0211-sprint-p2-2-backend-integration.md) | Integrate with POST /api/summarize endpoint | completed |
| [TSK-0212](../tasks/TSK-0212-sprint-p2-2-ux-edge-cases.md) | Handle UX edge cases (disable submit while loading, clear errors) | completed |

---

## Definition of Done

- [x] Submits URL and receives summary from backend
- [x] Shows correct message for invalid URLs
- [x] Shows correct message for "no subtitles available"

---

## Dependencies

- **Required:** Sprint P2.1 (backend API must be working)

---

## Exit Criteria

- [x] Frontend loads at http://localhost:3000 (Vite dev server, configurable)
- [x] Entering valid YouTube URL and clicking submit shows summary
- [x] Entering invalid URL shows error message
- [x] Video without subtitles shows "no subtitles" message

---

## Implementation Notes

- Stack: React 18 + TypeScript + Vite, tested with Vitest + React Testing Library (TDD).
- Location: [frontend/](../../frontend/) (created in this sprint).
- Backend base URL is configurable via `VITE_API_BASE_URL` (defaults to `http://localhost:8000`).
- 23 tests across 4 suites cover the API client, form, loading, summary display, error mapping, and UX edge cases.
- Run `npm install && npm test` (and `npm run dev`) from `frontend/`.