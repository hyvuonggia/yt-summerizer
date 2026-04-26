# Task TSK-0306 — Summaries Table

**Task ID:** TSK-0306  
**Sprint:** P3.2 — Database + Summary Persistence (History)  
**Status:** pending

---

## Description

Create summaries table schema:
- id (UUID/INT)
- user_id (FK to users)
- video_id
- url
- transcript_stats (JSON)
- provider
- summary_text
- created_at

---

## Acceptance Criteria

- [ ] Summaries table created
- [ ] FK to users
- [ ] All fields stored

---

## Deliverables

- Model: Summary (SQLAlchemy)
- Table: `summaries`