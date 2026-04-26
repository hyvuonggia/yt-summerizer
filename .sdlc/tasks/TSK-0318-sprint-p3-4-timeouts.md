# Task TSK-0318 — Timeouts and Graceful Failures

**Task ID:** TSK-0318  
**Sprint:** P3.4 — UI/UX Polishing + Reliability Enhancements  
**Status:** pending

---

## Description

Add request timeouts and graceful failure:
- HTTP timeout (30s default)
- LLM timeout (configurable)
- Cancel button for user
- Clear timeout messages

---

## Acceptance Criteria

- [ ] Timeouts configured
- [ ] Timeout shows clear message
- [ ] User can cancel request

---

## Deliverables

- Timeout config via env
- AbortController for frontend