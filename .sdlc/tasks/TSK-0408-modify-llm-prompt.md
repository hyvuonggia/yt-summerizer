# TSK-0408: Modify LLM Prompt to Output in Selected Language

**Story:** STY-0403 | **Sprint:** P2.4 | **Status:** pending
**Assignee:** - | **Estimate:** 1 hr

## Description
Modify the LLM prompt in backend/services/summarization.py to instruct the LLM to generate the summary in the selected language.

## Acceptance Criteria
- [ ] Prompt receives the summary_language parameter
- [ ] User prompt includes instruction to output in selected language
- [ ] Default behavior (no language selected) outputs in English
- [ ] Tested with at least 2 different languages

## Dependencies
- TSK-0407 (backend model updated)

## Execution Log
- *2026-04-29 22:00* Created by TaskManager