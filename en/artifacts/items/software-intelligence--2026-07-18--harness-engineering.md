---
source: hn
url: https://github.com/lopopolo/harness-engineering
published_at: '2026-07-18T23:27:36'
authors:
- handfuloflight
topics:
- software-foundation-model
- code-intelligence
- automated-software-production
- agent-network
- human-ai-interaction
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Harness Engineering

## Summary
Harness engineering improves coding-agent performance by keeping the model and agent fixed while shaping their context, tools, constraints, and feedback environment. The repository presents this as last-mile engineering for making an organization's requirements and operational knowledge usable by agents.

## Problem
- General model weights do not contain an organization's changing operational state, local terminology, quality standards, procedures, exception history, or authority relationships.
- Agents may produce code without understanding nonfunctional requirements such as reliability, security, compatibility, maintainability, performance, and operational risk.
- This matters because agents need organizational context and proof mechanisms to make reliable changes to real systems, including cases where people do not review the implementation directly.

## Approach
- Hold the model and coding agent constant as a black box, then improve the external levers of context and tools.
- Encode organizational requirements and decisions in the repository through retrievable documentation, examples, playbooks, executable constraints, and proof checks.
- Use files such as `AGENTS.md` and a thesis index to route work to relevant guidance, cases, and validation procedures.
- Feed accepted work, corrections, failures, and user responses back into the harness so later agent runs inherit accumulated organizational judgment.
- Treat deployment as a last-mile layer that supplies the agent's context, capabilities, authority, and evidence of outcome.

## Results
- The excerpt reports no controlled benchmark, dataset, metric, or baseline comparison.
- It claims that pointing agents at the author's accumulated writing and media can improve agent output by “100x,” but provides no measurement method or experimental evidence for that figure.
- The strongest supported result is a design claim: a curated harness can make organizational coherence cumulative across agent-maintained artifacts by turning local knowledge and feedback into reusable context, tools, examples, and checks.

## Link
- [https://github.com/lopopolo/harness-engineering](https://github.com/lopopolo/harness-engineering)
