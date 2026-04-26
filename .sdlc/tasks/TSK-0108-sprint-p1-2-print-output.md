# Task TSK-0108 — Print Summary Output

**Task ID:** TSK-0108  
**Sprint:** P1.2 — LLM Summarization End-to-End  
**Status:** completed

---

## Description

Print summary to stdout with metadata:
- Video information (title, channel, duration)
- Transcript statistics (language, snippet count, token count)
- LLM API details (model, tokens, cost)
- The summary text formatted nicely
- Processing time

---

## Acceptance Criteria

- [x] Prints video metadata
- [x] Prints transcript statistics
- [x] Prints LLM API stats (tokens, cost)
- [x] Prints the summary text
- [x] Prints total processing time

---

## Deliverables

- Function: `print_real_llm_output(transcript_data, metadata, summary, stats)`
- Location: `poc_summarize.py` lines 611-661
- Output: Formatted to stdout