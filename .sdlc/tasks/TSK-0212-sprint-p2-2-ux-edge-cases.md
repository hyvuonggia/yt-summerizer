# Task TSK-0212 — UX Edge Cases

**Task ID:** TSK-0212  
**Sprint:** P2.2 — React Frontend (Form + Loading + Output/Error)  
**Status:** completed

---

## Description

Handle UX edge cases:
- Disable submit while loading (prevent double-submit)
- Clear previous errors on new submit
- Clear previous results on new submit
- Empty URL validation before sending

---

## Acceptance Criteria

- [x] Cannot submit while loading (button + input disabled, guard in handler)
- [x] Previous errors cleared on new request (`onError(null)`)
- [x] Previous results cleared on new request (`onResult(null)`)
- [x] Empty URL shows validation error (`MISSING_URL`)

---

## Deliverables

- State + validation in [frontend/src/components/SummarizeForm.tsx](../../frontend/src/components/SummarizeForm.tsx)
- Tests: [frontend/src/components/SummarizeForm.test.tsx](../../frontend/src/components/SummarizeForm.test.tsx) (UX edge-case suite)