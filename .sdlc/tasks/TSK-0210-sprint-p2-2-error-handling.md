# Task TSK-0210 — Error Handling UI

**Task ID:** TSK-0210  
**Sprint:** P2.2 — React Frontend (Form + Loading + Output/Error)  
**Status:** completed

---

## Description

Error banner for structured errors:
- Display error message from API
- Map HTTP codes to user-friendly messages
- 400: "Invalid YouTube URL"
- 422: "No subtitles available for this video"
- 500: "Server error, please try again"

---

## Acceptance Criteria

- [x] Display error message from API response
- [x] User-friendly messages (not raw HTTP codes) — `INVALID_URL`, `NO_SUBTITLES_AVAILABLE`, `TRANSCRIPTS_DISABLED`, `VIDEO_NOT_FOUND`, `LLM_*`, `NETWORK_ERROR`
- [x] Clear error banner/styling (`role="alert"`)
- [x] Error clears on new submit (handled in `SummarizeForm`)

---

## Deliverables

- Component: [frontend/src/components/ErrorBanner.tsx](../../frontend/src/components/ErrorBanner.tsx)
- Tests: [frontend/src/components/ErrorBanner.test.tsx](../../frontend/src/components/ErrorBanner.test.tsx)