# Task TSK-0201 — Create FastAPI App

**Task ID:** TSK-0201  
**Sprint:** P2.1 — Backend API Skeleton + Core Summarize Endpoint  
**Status:** pending

---

## Description

Create FastAPI application structure:
- Main app with lifespan handler
- POST /api/summarize endpoint
- CORS configured
- Health endpoint

---

## Acceptance Criteria

- [ ] FastAPI app runs with uvicorn
- [ ] POST /api/summarize defined
- [ ] Returns 501 (not implemented yet) or actual response

---

## Deliverables

- File: `backend/main.py`
- Already exists with CORS configured, needs implementation