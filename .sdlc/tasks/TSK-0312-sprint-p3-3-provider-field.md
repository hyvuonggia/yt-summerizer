# Task TSK-0312 — Provider Field in API

**Task ID:** TSK-0312  
**Sprint:** P3.3 — AI Provider Selection + Backend Abstraction  
**Status:** pending

---

## Description

Allow optional provider field in API request:
- Request: `{ "url": "...", "provider": "openai" }`
- Validate provider (return 400 if unsupported)
- Use requested provider or default

---

## Acceptance Criteria

- [ ] Provider field accepted in request
- [ ] Unsupported returns 400
- [ ] Provider metadata in response

---

## Deliverables

- Request model: add optional "provider" field
- Validation: check provider exists