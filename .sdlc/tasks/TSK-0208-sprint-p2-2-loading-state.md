# Task TSK-0208 — Loading State

**Task ID:** TSK-0208  
**Sprint:** P2.2 — React Frontend (Form + Loading + Output/Error)  
**Status:** completed

---

## Description

Implement loading indicator during API call:
- Show spinner or progress indicator
- Disable submit button while loading
- Display step information (fetching transcript, calling LLM, etc.)

---

## Acceptance Criteria

- [x] Spinner/loading shown during API call (`role="status"` live region)
- [x] Button disabled while loading (label switches to "Summarizing\u2026")
- [x] User knows work is in progress

---

## Deliverables

- Inline loading state in [frontend/src/components/SummarizeForm.tsx](../../frontend/src/components/SummarizeForm.tsx)
- CSS spinner in [frontend/src/styles.css](../../frontend/src/styles.css)
- Tests: [frontend/src/components/SummarizeForm.test.tsx](../../frontend/src/components/SummarizeForm.test.tsx) (loading-state cases)