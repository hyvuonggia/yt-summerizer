# Product Backlog — YouTube Video Summarizer

**Last Updated:** 2026-04-29

---

## New Requirements (2026-04-29)

### STY-0401: Beautify Summary Output with Rich Markup
**Priority:** P1 | **Estimate:** 2 pts
- Currently, the summary output shows as plain markdown text on the frontend. Need to render it as proper HTML/markup for better browser display.

### STY-0402: Backend Progress Updates
**Priority:** P1 | **Estimate:** 3 pts
- Backend stops at "Waiting for LLM response..." and doesn't show when output is generated. Need to add progress/status updates so users know what's happening.

### STY-0403: Language Selection for Summary Output
**Priority:** P1 | **Estimate:** 3 pts
- Allow user to select the language on frontend, then the summarization should output in that selected language.

---

## Backlog (by Priority)

### P0 — Must Have (Current Sprint)
*(None)*

### P1 — Should Have (Next Sprint)
- STY-0401: Beautify Summary Output with Rich Markup
- STY-0402: Backend Progress Updates
- STY-0403: Language Selection for Summary Output

### P2 — Could Have (Future)
- STY-0301: Authentication (from P3.1)
- STY-0302: Protected Endpoints (from P3.1)
- STY-0303: Frontend Login UI (from P3.1)

### P3 — Won't Have (This Release)
- STY-0319: Rate Limiting (optional)

---

## Notes
- All P1 items relate to improving user experience and visibility
- STY-0403 requires both frontend (language selector) and backend (pass language to LLM prompt) changes