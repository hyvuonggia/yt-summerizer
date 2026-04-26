# Task TSK-0302 — Protected Endpoints

**Task ID:** TSK-0302  
**Sprint:** P3.1 — Authentication (Login/Session) + Protected History API  
**Status:** pending

---

## Description

Add auth-protected endpoints:
- GET /api/history (requires auth)
- POST /api/summarize (optionally protected)
- Use JWT validation or session check

---

## Acceptance Criteria

- [ ] Unauthenticated returns 401/403
- [ ] Authenticated accesses data
- [ ] User ID associated with requests

---

## Deliverables

- Protected endpoints in backend
- Auth dependency (FastAPI Depends)