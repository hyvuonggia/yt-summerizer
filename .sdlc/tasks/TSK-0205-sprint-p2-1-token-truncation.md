# Task TSK-0205 — Token Truncation in API

**Task ID:** TSK-0205  
**Sprint:** P2.1 — Backend API Skeleton + Core Summarize Endpoint  
**Status:** pending

---

## Description

Implement token-aware truncation in the API endpoint:
- Use tiktoken to count transcript tokens
- Truncate to fit model context limit
- Add truncation info to response metadata

---

## Acceptance Criteria

- [ ] Token counting works in API
- [ ] Truncation applied when needed
- [ ] Response includes transcript_stats

---

## Deliverables

- Integration in POST /api/summarize endpoint
- Uses existing `count_tokens()`, `truncate_text_to_tokens()`