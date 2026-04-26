# Task TSK-0210 — Error Handling UI

**Task ID:** TSK-0210  
**Sprint:** P2.2 — React Frontend (Form + Loading + Output/Error)  
**Status:** pending

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

- [ ] Display error message from API response
- [ ] User-friendly messages (not raw HTTP codes)
- [ ] Clear error banner/styling
- [ ] Error clears on new submit

---

## Deliverables

- Component: `src/components/ErrorBanner.tsx`
- Maps backend error codes to UI messages