---
source: arxiv
url: https://arxiv.org/abs/2607.01087v1
published_at: '2026-07-01T15:44:15'
authors:
- James C. Davis
- Paschal C. Amusuo
- Tanmay Singla
- "Berk \xC7akar"
- Kirsten A. Davis
topics:
- agentic-software-engineering
- code-intelligence
- software-governance
- human-ai-interaction
- ai-coding-agents
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Cheap Code, Costly Judgment: A Case Study on Governable Agentic Software Engineering

## Summary
The paper studies how one engineer kept AI-agent coding work controllable during a fast 12-week build. It claims the scarce work moved to judgment: spotting repeated failures and turning them into architecture, tests, lints, validators, gates, and agent instructions.

## Problem
- AI coding agents can create large amounts of code, but their output is unreliable, context-sensitive, and hard to trust at repository scale.
- Human inspection slows down high-volume agent work, while multi-agent work can raise output without clear quality control.
- The practical problem is how to keep agent-written systems inspectable, correctable, and maintainable while preserving speed.

## Approach
- The authors report a first-person case study: one expert engineer used Claude through VS Code for 12 weeks to build a document accessibility remediation system for Office and PDF files.
- The empirical record includes 88 contemporaneous field notes, 18,662 commits, about 420 KLOC of production code, and 1.16 MLOC of tests, lints, documentation, and agent tooling.
- They coded each field note as a critical incident, then built an 11-iteration codebook. A second author recoded 10 sampled incidents and matched 10/10 on incident class, 6/7 on category, and 5/7 on the third coding layer.
- The core mechanism is "failure → governance": repeated agent failures reveal a missing constraint, and the engineer adds a durable control or architectural change so later agent work is bounded.
- Architecture changes prevent some failure classes by construction, such as typed component catalogs and bounded seams. Controls detect failures after they occur, such as lints, tests, validators, gates, and mediators.

## Results
- The project produced about 420 KLOC of production code plus 1.16 MLOC of supporting artifacts in 12 weeks, with 18,662 commits and about 1.6 million lines of active artifacts analyzed.
- The coded corpus had 88 incidents. Engineering reflection dominated with 72 incidents; the largest categories were controls with 35 incidents and architecture with 20 incidents.
- The case reports a working system that can process Office and PDF files and pass or improve accessibility checks. The subject's course slide decks process in about 60 seconds at about $1 per deck.
- Total project cost was about $60K: $50K salary, $2K inference, $6K Google Cloud hosting, and $2K Claude subscriptions.
- The paper's main claimed result is a testable process model of governance conversion, grounded in the case rather than in a controlled benchmark. It does not claim a new model architecture or a head-to-head coding-agent accuracy result.

## Link
- [https://arxiv.org/abs/2607.01087v1](https://arxiv.org/abs/2607.01087v1)
