# Task TSK-0105 — LLM Integration

**Task ID:** TSK-0105  
**Sprint:** P1.2 — LLM Summarization End-to-End  
**Status:** completed

---

## Description

Implement LLM call via OpenRouter single provider:
- Initialize OpenAI client with OpenRouter base URL
- Call DeepSeek v3.2 (or configured model)
- Handle API errors with retry logic
- Return summary and stats

---

## Acceptance Criteria

- [x] Successfully calls OpenRouter API
- [x] Returns coherent summary text
- [x] Includes retry logic for transient errors
- [x] Prints cost estimation

---

## Deliverables

- Function: `call_llm_summarize(transcript_text, metadata)`
- Location: `poc_summarize.py` lines 429-571
- Returns: `(summary_text, stats_dict)`