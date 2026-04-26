# Task TSK-0209 — Summary Display

**Task ID:** TSK-0209  
**Sprint:** P2.2 — React Frontend (Form + Loading + Output/Error)  
**Status:** pending

---

## Description

Display summary output component:
- Render formatted summary text
- Show video metadata (title, channel)
- Show additional stats (provider, token count)
- Use proper formatting (headings, bullet points)

---

## Acceptance Criteria

- [ ] Summary displayed when API succeeds
- [ ] Video info shown (title, channel)
- [ ] Stats shown (provider, tokens)
- [ ] Formatted nicely (not raw text blob)

---

## Deliverables

- Component: `src/components/SummaryDisplay.tsx`
- Renders: `{ summary, video_id, provider, transcript_stats }`