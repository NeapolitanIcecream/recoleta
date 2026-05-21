---
source: arxiv
url: https://arxiv.org/abs/2605.05400v1
published_at: '2026-05-06T19:33:08'
authors:
- Andrew Zigler
topics:
- agentic-coding
- context-engineering
- code-intelligence
- multi-agent-software-engineering
- human-ai-interaction
- software-specification
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Mise en Place for Agentic Coding: Deliberate Preparation as Context Engineering Methodology

## Summary
MEP is a preparation-first method for agentic coding that asks developers to write context, specs, and task records before agents write code. The paper's evidence is a single hackathon case, so the claims are useful but not proven against a control group.

## Problem
- AI coding agents can produce code quickly, but weak context leads to misaligned code, debugging, refactoring, and security risk.
- The paper cites GitHub Copilot studies reporting 21-55% faster task completion and a Veracode 2025 report that 45% of AI-generated code contains security flaws.
- This matters because agent speed can shift cost into verification and rework when product intent, architecture, and domain knowledge stay implicit.

## Approach
- Phase 1, contextual grounding: capture tacit domain knowledge in structured Markdown documents that agents can read.
- Phase 2, collaborative specification: use human-agent dialogue to write design artifacts with screens, interactions, data flows, quality bars, and exclusions.
- Phase 3, task decomposition: turn the spec into dependency-aware JSON task records with acceptance criteria, then assign independent tasks to parallel agents.
- The method draws on backward design and tacit knowledge externalization; the paper names the related skill context fluency.

## Results
- In a January 2026 hackathon with about 12 teams and a 5-hour build window, the practitioner spent about 2 hours preparing before implementation.
- Preparation produced 10 planning documents, 9,386 words, a product specification, and 64 structured task records.
- Four parallel subagents implemented feature areas over 184 minutes; 43 tasks were closed with a median closure time of 5.9 minutes.
- The final system had 43 TypeScript/TSX files and 8,496 lines of source code, deployed as a full-stack educational platform.
- The planning-to-code ratio was 1.10:1 by words to lines, and the paper reports about a 5.7:1 preparation-to-active-agent-implementation ratio.
- Deployment and polish produced 9 commits over 52 minutes; bug tasks resolved at median 1.2 minutes versus 9.7 minutes for implementation tasks. The paper reports near-zero architectural rework, with no control baseline, so it does not prove causation.

## Link
- [https://arxiv.org/abs/2605.05400v1](https://arxiv.org/abs/2605.05400v1)
