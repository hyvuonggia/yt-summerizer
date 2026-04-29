# TSK-0407: Add summary_language Field to Backend Request Model

**Story:** STY-0403 | **Sprint:** P2.4 | **Status:** pending
**Assignee:** - | **Estimate:** 0.5 hrs

## Description
Add a new field `summary_language` to the SummarizeRequest model in backend/models.py to accept the desired output language.

## Acceptance Criteria
- [ ] New field `summary_language` added to SummarizeRequest
- [ ] Field is optional with default value "en"
- [ ] Field accepts language names (e.g., "English", "Spanish", "Vietnamese")
- [ ] API schema updated accordingly

## Dependencies
- None (backend model change)

## Execution Log
- *2026-04-29 22:00* Created by TaskManager