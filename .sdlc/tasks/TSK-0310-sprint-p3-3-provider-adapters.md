# Task TSK-0310 — Provider Adapters

**Task ID:** TSK-0310  
**Sprint:** P3.3 — AI Provider Selection + Backend Abstraction  
**Status:** pending

---

## Description

Implement provider adapters:
- Keep existing OpenRouter/DeepSeek
- Add OpenAI GPT-4 adapter
- Add Anthropic Claude adapter (optional)

---

## Acceptance Criteria

- [ ] Multiple providers work
- [ ] Switchable via config
- [ ] Same interface

---

## Deliverables

- Adapters: `OpenRouterProvider`, `OpenAIProvider`, `AnthropicProvider`
- Config: select default via LLM_PROVIDER env