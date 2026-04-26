# Sprint P2.3 — CORS/API Setup + Basic Operational Hardening

**Phase:** Phase 2: Minimum Viable Product (MVP)  
**Status:** pending  
**Sprint Goal:** Configure CORS, environment variables, logging, and health endpoint for production-readiness.

---

## Tasks

| Task ID | Description | Status |
|--------|-------------|--------|
| [TSK-0213](TSK-0213-sprint-p2-3-cors-configuration.md) | Configure CORS in FastAPI for dev/prod origins | pending |
| [TSK-0214](TSK-0214-sprint-p2-3-env-variables.md) | Add environment variable handling (.env) | pending |
| [TSK-0215](TSK-0215-sprint-p2-3-logging.md) | Add request/response logging without secrets | pending |
| [TSK-0216](TSK-0216-sprint-p2-3-health-endpoint.md) | Add GET /health endpoint | pending |

---

## Definition of Done

- [ ] Frontend successfully calls backend with CORS enabled
- [ ] Health endpoint returns expected status
- [ ] Logs show observability without leaking secrets

---

## Dependencies

- **Required:** Sprint P2.2 (frontend needs CORS)

---

## Exit Criteria

- [ ] CORS allows requests from frontend origin
- [ ] GET /health returns { "status": "healthy" }
- [ ] Logs include request start/end, transcript outcomes, LLM latency