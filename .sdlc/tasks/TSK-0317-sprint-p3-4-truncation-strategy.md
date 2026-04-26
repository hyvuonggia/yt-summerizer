# Task TSK-0317 — Consistent Truncation Strategy

**Task ID:** TSK-0317  
**Sprint:** P3.4 — UI/UX Polishing + Reliability Enhancements  
**Status:** pending

---

## Description

Consistent truncation strategy across providers:
- Use provider-specific token limits
- Reserve tokens for prompts
- Add truncation metadata
- Same truncation code used in Phase 1/2

---

## Acceptance Criteria

- [ ] All providers use consistent truncation
- [ ] Truncation info in response
- [ ] No token overflow errors

---

## Deliverables

- Unified truncation service
- Provider-specific limits config