# Task TSK-0308 — History Retrieval

**Task ID:** TSK-0308  
**Sprint:** P3.2 — Database + Summary Persistence (History)  
**Status:** pending

---

## Description

Implement history retrieval endpoint:
- GET /api/history
- Return list of user's summaries
- Include basic metadata (video_id, title, created_at)
- Sort by most recent first

---

## Acceptance Criteria

- [ ] Endpoint returns user's summaries
- [ ] Filtered by authenticated user
- [ ] Sorted by created_at desc

---

## Deliverables

- Endpoint: GET /api/history
- Response: List of summary objects