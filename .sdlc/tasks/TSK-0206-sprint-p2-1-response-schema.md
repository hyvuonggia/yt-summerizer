# Task TSK-0206 — Response Schema

**Task ID:** TSK-0206  
**Sprint:** P2.1 — Backend API Skeleton + Core Summarize Endpoint  
**Status:** pending

---

## Description

Define response schema for POST /api/summarize:
- `summary`: string - the generated summary
- `video_id`: string - YouTube video ID
- `provider`: string - LLM provider used (e.g., "openrouter")
- `transcript_stats`: object - word count, token count, truncated flag

---

## Acceptance Criteria

- [ ] Response includes summary text
- [ ] Response includes video_id
- [ ] Response includes provider name
- [ ] Response includes transcript_stats

---

## Deliverables

- Schema defined in `backend/models.py`
- Example response:
```json
{
  "summary": "**Main Topic**: ...",
  "video_id": "dQw4w9WgXcQ",
  "provider": "deepseek/deepseek-v3.2",
  "transcript_stats": {
    "word_count": 1500,
    "token_count": 45000,
    "truncated": false
  }
}
```