# Task TSK-0216 — Health Endpoint

**Task ID:** TSK-0216  
**Sprint:** P2.3 — CORS/API Setup + Basic Operational Hardening  
**Status:** completed

---

## Description

Add GET /health endpoint:
- Returns status: "healthy"
- Includes timestamp
- Includes environment name (dev/prod)

---

## Acceptance Criteria

- [ ] GET /health returns 200
- [ ] Response includes status field
- [ ] (Optional) timestamp included

---

## Deliverables

- Endpoint in backend/main.py (already exists, lines 72-79)