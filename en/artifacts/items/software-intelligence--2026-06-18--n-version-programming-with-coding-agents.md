---
source: arxiv
url: https://arxiv.org/abs/2606.20158v1
published_at: '2026-06-18T12:23:02'
authors:
- Javier Ron
- Benoit Baudry
- Martin Monperrus
topics:
- coding-agents
- n-version-programming
- software-reliability
- code-intelligence
- automated-testing
- multi-agent-software-engineering
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# N-Version Programming with Coding Agents

## Summary
The paper tests whether AI coding agents can make N-version programming practical for software reliability. It finds that agent versions share many failures, yet majority voting still cuts observed failures.

## Problem
- N-version programming depends on versions failing independently, but the Knight-Leveson study showed that human-written versions often fail on the same inputs.
- AI coding agents can now generate many implementations cheaply, so the paper asks whether agent, model, and language diversity reduces shared failure modes.
- This matters for automated software production because redundant agent-written code may improve reliability only if voting masks enough defects.

## Approach
- The authors reproduce the Knight-Leveson Launch Interceptor Program experiment with AI coding agents.
- They generate 69 implementations across 5 agent harnesses, 23 model configurations, and 3 languages: Python, Rust, and Pascal.
- Each version must pass a 200-case acceptance screen against a Python oracle validated by 82 unit tests.
- The 48 admitted versions run on the same 1,000,000 randomized inputs, with a failure recorded when any of 241 output bits differs from the oracle.
- The study measures coincident failures, pairwise failure correlation, language and agent effects, LIC-level fault sources, and all 3-version majority-vote units.

## Results
- 48 of 69 generated versions passed acceptance, a 70% admission rate. Cursor passed 6/6, Claude Code 13/15, Codex 11/15, Gemini 8/15, and OpenCode 10/18.
- Admission varied by language: Python 18/23, Rust 17/23, and Pascal 13/23.
- The independence model failed: the campaign found 429 coincident-failure cases where random independence predicted 115.36, with z=29.20.
- Of the 48 admitted versions, 27 had zero failures on the 1,000,000-case campaign; the worst version failed 10,469 inputs.
- Across all 17,296 three-version units, mean failure count fell from 387.44 for single versions to 130.99 for majority-vote triples.
- 11,844 of the 17,296 three-version units had zero observed failures on the 1,000,000 randomized inputs.

## Link
- [https://arxiv.org/abs/2606.20158v1](https://arxiv.org/abs/2606.20158v1)
