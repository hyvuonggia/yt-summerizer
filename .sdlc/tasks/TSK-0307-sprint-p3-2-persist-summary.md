# Task TSK-0307 — Persist Summary

**Task ID:** TSK-0307  
**Sprint:** P3.2 — Database + Summary Persistence (History)  
**Status:** pending

---

## Description

On summarization, persist summary to database:
- Save to summaries table after LLM call
- Associate with current user (from auth)
- Store all metadata

---

## Acceptance Criteria

- [ ] Summary saved after creation
- [ ] User ID associated
- [ ] All metadata stored

---

## Deliverables

- Service: `save_summary()` in backend
- Called after LLM response