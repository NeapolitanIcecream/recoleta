---
source: arxiv
url: https://arxiv.org/abs/2605.25665v1
published_at: '2026-05-25T10:15:24'
authors:
- Satadru Sengupta
- Tamunokorite Briggs
- Ivan Myshakivskyi
topics:
- software-foundation-models
- code-intelligence
- multi-agent-software-engineering
- automated-software-production
- human-ai-interaction
- agent-verification
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Meta-Engineering Harnesses for AI-Native Software Production: A Contract-Driven Adversarial Verification Architecture with Early Deployment Report

## Summary
The paper proposes a contract-driven harness for AI-native software production, aimed at making agent-built software easier to verify, deploy, and improve over repeated work.

## Problem
- AI coding agents can build useful artifacts, but production work needs ongoing verification, maintenance, deployment, and upgrades.
- Small service firms often need websites, booking, payments, workflow automation, and AI-agent interfaces without having internal technical teams.
- Single prompts and one-off human review miss hidden assumptions, contract gaps, model blind spots, and business-rule failures.

## Approach
- The harness turns raw operational requests into explicit contracts that specify behavior, roles, APIs, state transitions, invariants, errors, auth rules, QA targets, and acceptance criteria.
- A two-pass contract compiler first expands missing assumptions, then removes unsupported scope and rewrites ambiguous clauses.
- Role-specialized agents handle separate jobs: contract compilation, implementation, adversarial test generation, product review, architecture review, security review, QA, shipping, and arbitration.
- Verification uses independent builder and tester agents for contract-based tests, plus role-based review passes for product, architecture, UX, security, backend, frontend, and deployment risks.
- A four-way arbiter classifies failures as bug, spec gap, noise, or contract ambiguity, then routes the next action to implementation fixes, contract updates, verifier calibration, or a restart.

## Results
- Early deployment covered 3–4 weeks and 17 features, including in-app payments, scheduling, a product landing page, Slack notifications, an MCP search tool integration, 6 provider websites, and bug fixes.
- The system generated 18 adversarial test suites across features, plus 15 additional calibration suites for the scheduling module.
- It caught 5 bugs or implementation gaps before merge, including a missing Slack notification field and a codebase-standards violation.
- In the payments case study, the backend reached passing CI in 2 cycles, but later missed 2 business-logic cases: deposit deduction and discount calculation.
- The frontend payment flow was implemented in 1 attempt, but React Native dependency and environment issues required human intervention.
- The paper reports early operational evidence, not a controlled benchmark against SWE-bench, SWE-agent, or other baselines.

## Link
- [https://arxiv.org/abs/2605.25665v1](https://arxiv.org/abs/2605.25665v1)
