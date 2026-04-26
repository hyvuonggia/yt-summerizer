# Task TSK-0204 — LLM Summarization in API

**Task ID:** TSK-0204  
**Sprint:** P2.1 — Backend API Skeleton + Core Summarize Endpoint  
**Status:** pending

---

## Description

Implement LLM summarization in the API endpoint:
- Call summarization service
- Pass transcript + metadata to LLM
- Handle API errors gracefully

---

## Acceptance Criteria

- [ ] LLM called successfully
- [ ] Returns summary text
- [ ] Handles API errors with user-friendly messages

---

## Deliverables

- Integration in POST /api/summarize endpoint
- Uses existing `call_llm_summarize()` from poc_summarize.py