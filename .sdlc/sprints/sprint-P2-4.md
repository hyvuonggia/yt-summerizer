# Sprint P2.4 — UI Enhancements & User Experience

**Phase:** Phase 2: Backend Integration
**Status:** pending
**Sprint Goal:** Beautify summary output with rich markup, add backend progress updates, and implement language selection for summary output.

---

## Stories

| Story ID | Title | Estimate |
|----------|-------|----------|
| [STY-0401](STY-0401-beautify-summary-output.md) | Beautify Summary Output with Rich Markup | 2 pts |
| [STY-0402](STY-0402-backend-progress-updates.md) | Backend Progress Updates | 3 pts |
| [STY-0403](STY-0403-language-selection.md) | Language Selection for Summary Output | 3 pts |

**Total:** 8 pts

---

## Tasks (To Be Created)

| Task ID | Story | Description | Status |
|---------|-------|-------------|--------|
| TSK-0401 | STY-0401 | Add markdown-to-HTML library to frontend | pending |
| TSK-0402 | STY-0401 | Update SummaryDisplay to use rendered HTML | pending |
| TSK-0403 | STY-0401 | Add CSS styling for rendered summary | pending |
| TSK-0404 | STY-0402 | Add progress logging in backend main.py | pending |
| TSK-0405 | STY-0402 | Improve logging in summarization service | pending |
| TSK-0406 | STY-0403 | Add language selector dropdown to frontend | pending |
| TSK-0407 | STY-0403 | Add summary_language field to backend request model | pending |
| TSK-0408 | STY-0403 | Modify LLM prompt to output in selected language | pending |

---

## Definition of Done

- [ ] All 3 stories implemented and merged
- [ ] Unit + integration tests passing
- [ ] Delta coverage on new/modified code ≥ 80%
- [ ] Code reviewed by CodeReviewer (no blocking findings)
- [ ] Build green (BuildAgent) and CI green (DevOpsAgent)
- [ ] Documentation updated (DocWriter)
- [ ] Acceptance verified by ProductOwner
- [ ] No P0/P1 defects open

---

## Dependencies

- **Required:** Sprint P2.3 (CORS, logging, env variables in place)
- **Required:** Sprint P2.2 (frontend form and display working)

---

## Exit Criteria

- [ ] Summary displays as formatted HTML (not plain text)
- [ ] Backend logs show progress during summarization
- [ ] User can select output language and summary appears in that language