# Task TSK-0101 — YouTube URL Parsing

**Task ID:** TSK-0101  
**Sprint:** P1.1 — Transcript Retrieval + Validation  
**Status:** completed

---

## Description

Implement YouTube URL parsing to extract video_id from various URL formats:
- Standard: `https://www.youtube.com/watch?v=VIDEO_ID`
- Short: `https://youtu.be/VIDEO_ID`
- Embedded: `https://www.youtube.com/embed/VIDEO_ID`
- Mobile: `https://m.youtube.com/watch?v=VIDEO_ID`

---

## Acceptance Criteria

- [x] Function accepts any valid YouTube URL format
- [x] Returns 11-character video ID string
- [x] Returns None/empty for invalid URLs
- [x] Tested in poc_summarize.py

---

## Deliverables

- Function: `extract_video_id(url: str) -> Optional[str]`
- Location: `poc_summarize.py` lines 44-79
- Tests: Manual testing confirmed