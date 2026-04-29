# STY-0403: Language Selection for Summary Output

**Epic:** N/A | **Priority:** P1 | **Estimate:** 3 pts
**Status:** Backlog | **Owner:** ProductOwner | **Sprint:** -

## User Story
As a user, I want to select the language for the summary output on the frontend, so that the summarization is generated in my preferred language.

## Acceptance Criteria
- [ ] Given the user is on the frontend, When they are about to submit a YouTube URL, Then they should be able to select a language from a dropdown (e.g., English, Spanish, French, German, Vietnamese, etc.)
- [ ] Given the user selects a language (e.g., Vietnamese), When the summary is generated, Then the LLM should generate the summary in that selected language
- [ ] Given the user does not select any language, When the summary is generated, Then it should default to English

## Technical Notes
- **Frontend changes** (`frontend/src/components/SummarizeForm.tsx`):
  - Add a language selector dropdown
  - Pass the selected language to the API call
  - Update `frontend/src/types.ts` if needed

- **Backend changes** (`backend/main.py` and `backend/services/summarization.py`):
  - The `SummarizeRequest` model already has a `language` field (for transcript language)
  - Need to add a new field for `summary_language` or reuse the existing field with different meaning
  - Modify the LLM prompt to include the language requirement

- **LLM Prompt modification**:
  - Current prompt in `backend/services/summarization.py` doesn't specify output language
  - Need to add: "Generate the summary in [LANGUAGE]" to the user prompt

## API Design Consideration
Option A: Add new field `summary_language` to `SummarizeRequest`
Option B: Reuse existing `language` field for both transcript and summary (not recommended - confusing)

**Recommended:** Option A - add `summary_language` field

## Dependencies
- STY-0401 (optional - can be done independently)

## Definition of Ready (DoR)
- [x] Description clear and unambiguous
- [x] Acceptance criteria written in Given/When/Then
- [x] Dependencies identified (or none)
- [x] Estimate agreed (3 pts)
- [ ] Non-functional requirements captured (perf, security, a11y)

## Definition of Done (DoD)
- [ ] Code implemented and merged
- [ ] Unit + integration tests passing
- [ ] Delta coverage on new/modified code ≥ 80%
- [ ] Code reviewed by CodeReviewer (no blocking findings)
- [ ] Build green (BuildAgent) and CI green (DevOpsAgent)
- [ ] Documentation updated (DocWriter)
- [ ] Acceptance verified by ProductOwner
- [ ] No P0/P1 defects open

## Linked Tasks
- TSK-0406: Add language selector dropdown to frontend
- TSK-0407: Add summary_language field to backend request model
- TSK-0408: Modify LLM prompt to output in selected language

## Execution Log
- *2026-04-29 21:55* Created by ProductOwner - Added to backlog from new requirements