# Sprint P3.3 — AI Provider Selection + Backend Abstraction

**Phase:** Phase 3: Enhancements  
**Status:** pending  
**Sprint Goal:** Add multi-provider abstraction with fallback mechanism; allow provider selection in API and UI.

---

## Tasks

| Task ID | Description | Status |
|--------|-------------|--------|
| [TSK-0309](TSK-0309-sprint-p3-3-provider-interface.md) | Define internal provider interface | pending |
| [TSK-0310](TSK-0310-sprint-p3-3-provider-adapters.md) | Implement more provider adapters (OpenAI, Anthropic) | pending |
| [TSK-0311](TSK-0311-sprint-p3-3-fallback-mechanism.md) | Implement API fallback mechanism (env var primary + fallback) | pending |
| [TSK-0312](TSK-0312-sprint-p3-3-provider-field.md) | Allow optional "provider" field in API request | pending |
| [TSK-0313](TSK-0313-sprint-p3-3-frontend-selector.md) | Add provider selector in frontend UI | pending |

---

## Definition of Done

- [ ] User selects provider and receives summary from that provider
- [ ] Backend returns provider metadata in response
- [ ] Unsupported provider returns error (400)

---

## Dependencies

- **Required:** Sprint P2.3 (base API stable)

---

## Exit Criteria

- [ ] POST /api/summarize accepts "provider" field
- [ ] Provider metadata included in response
- [ ] Fallback triggers on transient errors (429/502/503)