# TSK-0405: Improve Logging in Summarization Service

**Story:** STY-0402 | **Sprint:** P2.4 | **Status:** pending
**Assignee:** - | **Estimate:** 0.5 hrs

## Description
Improve logging in backend/services/summarization.py to show progress during LLM processing.

## Acceptance Criteria
- [ ] Log when token counting starts
- [ ] Log if transcript is truncated (with reason)
- [ ] Log when LLM API call starts
- [ ] Log when response is received (with token count)
- [ ] Remove or improve the console print statements

## Dependencies
- TSK-0404 (main.py logging)

## Execution Log
- *2026-04-29 22:00* Created by TaskManager