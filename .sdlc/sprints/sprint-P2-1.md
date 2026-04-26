# Sprint P2.1 — Backend API Skeleton + Core Summarize Endpoint

**Phase:** Phase 2: Minimum Viable Product (MVP)  
**Status:** pending  
**Sprint Goal:** Build FastAPI backend with POST /api/summarize endpoint, request validation, transcript retrieval, LLM integration, and proper response schemas.

---

## Tasks

| Task ID | Description | Status |
|--------|-------------|--------|
| [TSK-0201](TSK-0201-sprint-p2-1-fastapi-app.md) | Create FastAPI app with POST /api/summarize | pending |
| [TSK-0202](TSK-0202-sprint-p2-1-request-validation.md) | Implement request validation (extract video ID, reject invalid URLs) | pending |
| [TSK-0203](TSK-0203-sprint-p2-1-transcript-retrieval.md) | Implement transcript retrieval in API | pending |
| [TSK-0204](TSK-0204-sprint-p2-1-llm-summarization.md) | Implement LLM summarization in API | pending |
| [TSK-0205](TSK-0205-sprint-p2-1-token-truncation.md) | Implement token-aware truncation in API | pending |
| [TSK-0206](TSK-0206-sprint-p2-1-response-schema.md) | Define response schema (summary, video_id, provider, stats) | pending |

---

## Definition of Done

- [ ] Calling endpoint with valid URL returns summary JSON
- [ ] Invalid URL returns structured error (400)
- [ ] Missing subtitles returns structured "no subtitles" error (422)

---

## Dependencies

- **Required:** Sprint P1.2 (LLM integration logic exists in poc_summarize.py)

---

## Implementation Notes

Current state in `backend/main.py`:
- FastAPI app configured with CORS middleware
- POST /api/summarize endpoint exists but returns 501 (skeleton)
- Request/Response models defined in backend/models.py

Tasks remaining:
- Implement actual summarization logic (migrate from poc_summarize.py)
- Add proper error handling for invalid URLs
- Return structured JSON with summary, video_id, provider, stats

---

## Exit Criteria

- [ ] `POST /api/summarize` with valid URL returns 200 with summary JSON
- [ ] Invalid URL returns 400 with error message
- [ ] No subtitles returns 422 with "NO_SUBTITLES_AVAILABLE" message