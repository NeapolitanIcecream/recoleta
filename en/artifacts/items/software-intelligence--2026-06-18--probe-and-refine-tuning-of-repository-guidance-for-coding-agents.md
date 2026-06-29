---
source: arxiv
url: https://arxiv.org/abs/2606.20512v1
published_at: '2026-06-18T17:30:15'
authors:
- Asa Shepard
- Jeannie Albrecht
topics:
- coding-agents
- repository-guidance
- swe-bench
- prompt-tuning
- code-intelligence
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Probe-and-Refine Tuning of Repository Guidance for Coding Agents

## Summary
Probe-and-refine tuning improves coding-agent resolve rate by turning generic repository guidance into compact, failure-tested instructions. The main gain is that agents reach evaluable patches more often.

## Problem
- LLM coding agents often lack repository-specific operational knowledge, such as which files contain a subsystem, which tests to run, and which fixes tend to break related code.
- Existing AGENTS.md-style files have mixed evidence: some studies report efficiency gains, while others report lower resolve rates when agents follow bad or generic instructions.
- This matters because wrong repository guidance can send an agent to the wrong file or make it follow brittle workflows, reducing bug-fix success.

## Approach
- The method starts with a static repository knowledge base built from tree-sitter-derived structure plus generic LLM-written guidance.
- It generates 10 synthetic bug-fix probes per iteration, then uses single-shot LLM calls to attempt fixes and judge where the current guidance failed.
- It aggregates the failures into edits to the guidance file, capped at 5 edits per iteration and 3000 characters total.
- The loop runs for 3–5 iterations per repository, with no tool use, no agent loop during tuning, no reinforcement learning, and no gradient updates.
- The final guidance is reused by the same ReAct-style coding agent on SWE-bench Verified.

## Results
- On 500 SWE-bench Verified instances across 4 trials with Qwen3.5-35B-A3B at 200 steps, probe-and-refine reaches a 33.0% mean resolve rate, compared with 28.3% for static_kb and 25.5% for no_context.
- The paper reports p<0.001 for both probe-and-refine contrasts against static_kb and no_context.
- The gain comes from coverage: refined guidance produces evaluable patches for 14.5 percentage points more instances, while per-patch precision stays near 59% with p=0.119.
- Probe-and-refine has lower fallback use at 200 steps: 14.8% versus 30.8% for static_kb and 25.6% for no_context.
- The refined artifacts average 2,754 characters versus 1,687 for static_kb, and the added 104 lines are 47% procedural, 30% structural, and 23% quality-gate rules.
- The main trial reports 31 consistently unique solves for probe-and-refine guidance.

## Link
- [https://arxiv.org/abs/2606.20512v1](https://arxiv.org/abs/2606.20512v1)
