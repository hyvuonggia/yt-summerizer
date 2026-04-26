# Task TSK-0107 — Token-Aware Truncation

**Task ID:** TSK-0107  
**Sprint:** P1.2 — LLM Summarization End-to-End  
**Status:** completed

---

## Description

Implement token-aware truncation using tiktoken:
- Count tokens in transcript
- Truncate to fit within model context limit (120K for DeepSeek v3.2)
- Reserve tokens for prompts (~500 tokens)
- Add ellipsis when truncating

---

## Acceptance Criteria

- [x] Token counting works with tiktoken
- [x] Truncation respects model context limit
- [x] No mid-token boundary slicing (JSON-safe)
- [x] Adds "..." when truncated

---

## Deliverables

- Functions: `count_tokens(text)`, `truncate_text_to_tokens(text, max_tokens)`
- Location: `poc_summarize.py` lines 270-331
- Uses cl100k_base encoding (GPT-4/DeepSeek compatible)