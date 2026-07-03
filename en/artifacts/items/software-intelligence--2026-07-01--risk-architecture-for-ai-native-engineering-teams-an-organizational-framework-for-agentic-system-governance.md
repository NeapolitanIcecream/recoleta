---
source: arxiv
url: https://arxiv.org/abs/2607.01421v1
published_at: '2026-07-01T19:31:02'
authors:
- Laxmipriya Ganesh Iyer
topics:
- agentic-ai-governance
- engineering-management
- software-risk
- multi-agent-software-engineering
- human-ai-interaction
- ai-native-teams
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Risk Architecture for AI-Native Engineering Teams: An Organizational Framework for Agentic System Governance

## Summary
The paper argues that engineering managers need a team-level risk model for agentic AI systems because standard software ownership, testing, and escalation rules miss failures caused by probabilistic autonomous agents.

## Problem
- Conventional software risk management assumes deterministic behavior, discrete deployments, and clear component ownership; agentic AI systems break all three assumptions.
- Existing AI governance work covers policy rules such as NIST AI RMF and ISO/IEC 42001, while technical catalogs such as OWASP agentic AI guidance cover threats; neither tells an engineering manager who owns detection, rollback, or escalation.
- The paper treats cross-team boundaries as a key risk point, especially when a deterministic downstream system consumes probabilistic AI output as if it were exact.

## Approach
- It defines a 7-dimension team profile: output determinism, action autonomy, verification model, risk ownership, escalation trigger, data surface, and change velocity.
- It compares 3 team types: pure software engineering, hybrid teams, and AI-native teams.
- It builds a 6-cluster failure taxonomy: security, privacy, autonomy, change-induced failures, ownership/accountability, and dependency-boundary determinism mismatch.
- It evaluates risk coverage synthetically by scoring whether each team profile can detect, contain, and escalate a defined scenario set, including a 2-team producer-consumer boundary case.
- It grounds the scenario clusters in public incidents, including Microsoft 365 Copilot EchoLeak, OpenAI’s March 2023 chat-title and payment-data bug, Replit’s reported production database deletion, Air Canada’s chatbot case, and Australia’s Robodebt case.

## Results
- The excerpt does not provide numeric detection, containment, or escalation coverage scores; the paper says its claims are derived from a synthetic adequacy test rather than observed team behavior.
- The paper claims coverage degrades as teams move across 3 profiles: pure software engineering, hybrid, and AI-native operation.
- The main claimed gap appears at the AI-native step: uncovered high-consequence failures emerge only there, with the worst coverage at organizational boundaries.
- The paper identifies 20 scenarios across 6 clusters, including 5 scenarios for dependency-boundary determinism mismatch.
- Public grounding includes EchoLeak with CVSS 9.3 from the Microsoft CNA and 7.5 from NVD, OpenAI’s March 2023 exposure affecting about 1.2% of Plus subscribers, and Robodebt raising about $1.76B in unlawful debts.
- The concrete management output is a minimal risk assignment model: name owners for tool contracts, causal action chains, and cross-team boundaries; add semantic escalation triggers; and give teams authority for asymmetric rollback and reconciliation.

## Link
- [https://arxiv.org/abs/2607.01421v1](https://arxiv.org/abs/2607.01421v1)
