# Task TSK-0202 — Request Validation

**Task ID:** TSK-0202  
**Sprint:** P2.1 — Backend API Skeleton + Core Summarize Endpoint  
**Status:** completed

---

## Description

Implement request validation:
- Validate YouTube URL format
- Extract video ID from URL
- Return 400 for invalid URLs with error message

---

## Acceptance Criteria

- [x] Invalid URL returns HTTP 400
- [x] Error message identifies the issue
- [x] Valid URL passes validation

---

## Deliverables

- Validation logic in `backend/services/` or directly in endpoint
- Uses existing `extract_video_id()` from poc_summarize.py