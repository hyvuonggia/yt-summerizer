# Task TSK-0311 — Fallback Mechanism

**Task ID:** TSK-0311  
**Sprint:** P3.3 — AI Provider Selection + Backend Abstraction  
**Status:** pending

---

## Description

Implement API fallback mechanism:
- Primary provider from env
- Fallback provider(s) from env
- On transient errors (429/502/503/timeouts), auto-retry fallback
- Preserve same transcript + prompt + options

---

## Acceptance Criteria

- [ ] Primary provider configured
- [ ] Fallback provider configured
- [ ] Retry on transient errors
- [ ] Same request across providers

---

## Deliverables

- Config: LLM_PRIMARY, LLM_FALLBACK env vars
- Service: auto-fallback logic