# Task TSK-0213 — CORS Configuration

**Task ID:** TSK-0213  
**Sprint:** P2.3 — CORS/API Setup + Basic Operational Hardening  
**Status:** pending

---

## Description

Configure CORS in FastAPI:
- Allow frontend origin (dev: localhost:3000)
- Configure via environment variable for production
- allow_methods=["*"], allow_headers=["*"]
- allow_credentials=True

---

## Acceptance Criteria

- [ ] CORS configured in backend/main.py
- [ ] Origin configurable via .env
- [ ] Frontend can call backend

---

## Deliverables

- CORS middleware in backend/main.py (already exists)
- Update: configurable origins via settings