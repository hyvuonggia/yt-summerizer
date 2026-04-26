# Sprint P2.2 — React Frontend (Form + Loading + Output/Error)

**Phase:** Phase 2: Minimum Viable Product (MVP)  
**Status:** pending  
**Sprint Goal:** Build React frontend with URL input form, loading state, summary display, and error handling.

---

## Tasks

| Task ID | Description | Status |
|--------|-------------|--------|
| [TSK-0207](TSK-0207-sprint-p2-2-react-form.md) | Build React component with URL input + submit button | pending |
| [TSK-0208](TSK-0208-sprint-p2-2-loading-state.md) | Implement loading indicator during API call | pending |
| [TSK-0209](TSK-0209-sprint-p2-2-summary-display.md) | Display summary output component | pending |
| [TSK-0210](TSK-0210-sprint-p2-2-error-handling.md) | Error banner for structured errors | pending |
| [TSK-0211](TSK-0211-sprint-p2-2-backend-integration.md) | Integrate with POST /api/summarize endpoint | pending |
| [TSK-0212](TSK-0212-sprint-p2-2-ux-edge-cases.md) | Handle UX edge cases (disable submit while loading, clear errors) | pending |

---

## Definition of Done

- [ ] Submits URL and receives summary from backend
- [ ] Shows correct message for invalid URLs
- [ ] Shows correct message for "no subtitles available"

---

## Dependencies

- **Required:** Sprint P2.1 (backend API must be working)

---

## Exit Criteria

- [ ] Frontend loads at http://localhost:3000 (or configured port)
- [ ] Entering valid YouTube URL and clicking submit shows summary
- [ ] Entering invalid URL shows error message
- [ ] Video without subtitles shows "no subtitles" message