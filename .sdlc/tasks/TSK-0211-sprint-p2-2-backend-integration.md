# Task TSK-0211 — Backend Integration

**Task ID:** TSK-0211  
**Sprint:** P2.2 — React Frontend (Form + Loading + Output/Error)  
**Status:** completed

---

## Description

Integrate React frontend with backend API:
- Use fetch or axios to POST /api/summarize
- Send JSON body: `{ "url": "<youtube_url>" }`
- Handle response JSON
- Handle network errors

---

## Acceptance Criteria

- [x] API called successfully (POST `/api/summarize` with `{ url }`)
- [x] Response parsed correctly into `SummarizeResponse`
- [x] Network errors handled (`NETWORK_ERROR`) and FastAPI `detail.error_code` propagated

---

## Deliverables

- API client: [frontend/src/api.ts](../../frontend/src/api.ts)
- Types: [frontend/src/types.ts](../../frontend/src/types.ts)
- Tests: [frontend/src/api.test.ts](../../frontend/src/api.test.ts)
- Configurable base URL via `VITE_API_BASE_URL` ([frontend/.env.example](../../frontend/.env.example))