---
source: hn
url: https://blog.sshh.io/p/designing-software-for-software-factories
published_at: '2026-06-13T22:34:33'
authors:
- sshh12
topics:
- software-factory
- agentic-workflows
- code-intelligence
- automated-testing
- human-in-the-loop
- multi-agent-software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Designing Software for Software Factories

## Summary
This post argues that a software factory is an AI-driven system that takes raw customer requests and bug reports, turns them into code, tests them, and ships them with limited human review. The main point is that the factory works best when the codebase has clear contracts, strong test tiers, and feedback loops that let agents keep improving future runs.

## Problem
- Software teams want AI to handle more of the development loop, but most projects still depend on humans to scope work, break down tasks, and validate changes.
- AI coding breaks down when codebases lack clear contracts, testability, or enough structure for agents to plan and verify work.
- Manual gates, shared staging bottlenecks, and weak feedback capture keep the loop slow and prevent parallel work.

## Approach
- Define a software factory as a system that can accept customer-generated RFEs and bug reports, run solution design and implementation, test changes, and deploy them with humans only for off-ramping and selected reviews.
- Add markdown-based project contracts, such as AGENTS.md files, that describe principles, architecture boundaries, validation rules, and roadmap-aware expectations.
- Make every change testable by an agent, with tiered checks that include linting, typing, unit tests, security scans, integration tests, UI-level tests, and rollout monitoring.
- Let agents run the full test loop themselves, build verification scripts, and even create or respawn test environments when shared staging is blocked.
- Feed reviewer feedback, agent traces, incidents, metrics, and customer outcomes back into the system so later runs improve.

## Results
- No experimental results or benchmark table are given in the excerpt.
- The strongest concrete claim is that modern models can write “surprisingly correct and complex software” when paired with a well-designed test harness.
- The author claims a software factory can produce “tens of thousands of lines of code shipped a day” if the right contracts are in place.
- For greenfield projects, the post recommends pairing with a coding agent for the first 3–10k lines of code and the first few end-to-end features, which the author says should take about 1–3 weeks at modern development speeds.
- For brownfield systems, the claim is that rebuilding or decomposing a subcomponent to make changes agent-testable can cost less than continuing feature work with humans in the loop, but no numeric study is provided.
- The post also claims fully autonomous second-order feedback loops have not worked well in the author’s experience and tend to produce “positive feedback slop loops”.

## Link
- [https://blog.sshh.io/p/designing-software-for-software-factories](https://blog.sshh.io/p/designing-software-for-software-factories)
