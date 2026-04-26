# Task TSK-0106 — Prompt Engineering

**Task ID:** TSK-0106  
**Sprint:** P1.2 — LLM Summarization End-to-End  
**Status:** completed

---

## Description

Implement system and user prompts for summarization:
- System prompt: instructions for YouTube video summarization
- User prompt: video context + transcript text
- Format: structured summary (main topic, key points, conclusion)

---

## Acceptance Criteria

- [x] System prompt includes summarization guidelines
- [x] User prompt includes video metadata (title, channel, duration)
- [x] Response format defined (summary, key points, conclusion)
- [x] JSON-safe output (no incomplete UTF-8)

---

## Deliverables

- Function: `create_summarization_prompt(transcript_text, metadata)`
- Location: `poc_summarize.py` lines 334-383
- Returns: `[{role: "system", content: ...}, {role: "user", content: ...}]`