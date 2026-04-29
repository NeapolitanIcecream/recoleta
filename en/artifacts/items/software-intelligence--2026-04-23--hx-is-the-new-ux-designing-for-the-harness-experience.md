---
source: hn
url: https://neurometric.substack.com/p/hx-is-the-new-ux-what-you-need-to
published_at: '2026-04-23T23:39:45'
authors:
- robmay
topics:
- agentic-interfaces
- human-ai-interaction
- design-methodology
- ai-agents
- control-and-audit
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# HX Is the New UX: Designing for the Harness Experience

## Summary
The piece argues that software design needs to shift from classic user experience toward "Harness Experience" for AI agents. Its main claim is that when agents act for people, design should focus on steering, trust, audit, and handoff rather than screen-by-screen navigation.

## Problem
- Traditional UX assumes a human moves through screens, forms, and funnels to complete a task.
- Agentic software can bypass those interfaces by calling APIs, checking context, and acting directly, which makes many old UI patterns less useful.
- This matters because people still need control over agent behavior: they must set intent, judge outcomes, inspect decisions, and step in when needed.

## Approach
- The article proposes **HX (Harness Experience)** as a design discipline for the relationship between a human and one or more acting agents.
- Its core mechanism is simple: treat the human as a director of agent work, not a click-by-click operator of the product.
- It names three design pillars: **steerability** (express goals, constraints, and corrections), **transparency and auditability** (show why the agent acted in a form a non-engineer can inspect), and **intervention points** (let humans pause, take over, and return control without losing context).
- It also suggests new design primitives for agent systems: handling latency, exposing uncertainty, and making verification fast because the human role shifts toward quality control.

## Results
- The excerpt does **not** provide experiments, benchmarks, datasets, or quantitative comparisons.
- It makes a structural claim: in tasks like travel booking, an agent can skip the website funnel and work through APIs plus user context such as calendar and preference history.
- It gives one concrete confidence example, saying an agent operating at **78% confidence** should expose that uncertainty rather than hide it.
- Its strongest claim is conceptual: products built for smooth obedience can fail when an agent diverges from user intent, while HX aims to reduce that risk through steerability, auditability, and intervention design.

## Link
- [https://neurometric.substack.com/p/hx-is-the-new-ux-what-you-need-to](https://neurometric.substack.com/p/hx-is-the-new-ux-what-you-need-to)
