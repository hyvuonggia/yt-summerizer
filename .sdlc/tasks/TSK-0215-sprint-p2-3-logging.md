# Task TSK-0215 — Logging

**Task ID:** TSK-0215  
**Sprint:** P2.3 — CORS/API Setup + Basic Operational Hardening  
**Status:** pending

---

## Description

Add request/response logging:
- Log request start/end timestamps
- Log transcript fetch outcomes
- Log LLM call latency
- NEVER log transcript content or secrets

---

## Acceptance Criteria

- [ ] Request logging in endpoint
- [ ] Transcript outcome logged
- [ ] LLM latency logged
- [ ] No secrets in logs

---

## Deliverables

- Logging in backend endpoint (using Python logging)