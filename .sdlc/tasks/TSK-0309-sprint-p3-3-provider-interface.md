# Task TSK-0309 — Provider Interface

**Task ID:** TSK-0309  
**Sprint:** P3.3 — AI Provider Selection + Backend Abstraction  
**Status:** pending

---

## Description

Define internal provider interface:
- Abstract class or Protocol
- Methods: summarize(transcript, metadata, options) -> SummaryResult
- Standard response format

---

## Acceptance Criteria

- [ ] Interface defined
- [ ] All providers implement same interface
- [ ] Response format consistent

---

## Deliverables

- Base class: `LLMProvider` (Protocol/ABC)
- Model: `SummaryResult`