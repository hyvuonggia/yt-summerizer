# Task TSK-0203 — Transcript Retrieval in API

**Task ID:** TSK-0203  
**Sprint:** P2.1 — Backend API Skeleton + Core Summarize Endpoint  
**Status:** pending

---

## Description

Implement transcript retrieval in the API endpoint:
- Call transcript service
- Handle TranscriptsDisabled exception → return 422
- Handle NoTranscriptFound → return 422 with message

---

## Acceptance Criteria

- [ ] Transcript retrieved successfully
- [ ] No subtitles returns HTTP 422 with "NO_SUBTITLES_AVAILABLE"
- [ ] Network errors handled gracefully

---

## Deliverables

- Integration in POST /api/summarize endpoint
- Uses existing `fetch_transcript()` from poc_summarize.py