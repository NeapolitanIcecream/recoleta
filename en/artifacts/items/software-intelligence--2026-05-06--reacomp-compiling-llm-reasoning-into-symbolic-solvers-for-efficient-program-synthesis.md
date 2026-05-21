---
source: arxiv
url: https://arxiv.org/abs/2605.05485v1
published_at: '2026-05-06T22:08:17'
authors:
- Atharva Naik
- Yash Mathur
- Prakam
- Carolyn Rose
- David Mortensen
topics:
- program-synthesis
- code-intelligence
- llm-reasoning
- symbolic-solvers
- neuro-symbolic-ai
- test-time-efficiency
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# ReaComp: Compiling LLM Reasoning into Symbolic Solvers for Efficient Program Synthesis

## Summary
ReaComp turns a small set of LLM reasoning traces into reusable symbolic program synthesizers for programming-by-example and logic-rule synthesis. The induced solvers solve many tasks with no LLM call at test time and improve LLM fallback accuracy and token use on hard cases.

## Problem
- LLMs can solve program synthesis tasks, but hard instances need many samples or refinement steps, which raises token cost and failure risk.
- Long compositional programs are difficult for unstructured LLM search; the paper reports loops, repeated attempts, and weaker accuracy as solution length grows.
- This matters for code intelligence and automated software production because repeated LLM inference is costly when many similar synthesis tasks must be solved.

## Approach
- ReaComp first collects about 100 LLM reasoning traces per benchmark, balanced across task difficulty and success or failure.
- A coding agent, such as Claude Code or Qwen with OpenHands, reads the traces and writes a standalone Python symbolic solver over a constrained DSL.
- The solver searches program candidates directly and uses the verifier to pick a candidate that matches the examples.
- At test time, the symbolic solver runs first. If it solves the task, no LLM call is made; otherwise the system falls back to LLM Best-of-K or direct-feedback search.
- The construction cost is paid once, then reused across many tasks.

## Results
- On PBEBench-Lite, the All Symbolic solver ensemble reaches 91.3% accuracy with 0 test-time LLM tokens, compared with BoK at 93.8% using 68.0M tokens. BoK + All Symbolic reaches 93.9% with 43.5M tokens, a 36% token reduction.
- On PBEBench-Hard, All Symbolic reaches 84.7% accuracy with 0 test-time LLM tokens, beating BoK at 68.4% by 16.3 percentage points. BoK + All Symbolic reaches 85.8% and uses 71.6M tokens versus 332.1M for BoK, a 78% reduction.
- On SLR-Bench, the CC symbolic solver gets 46.8% hard-tier accuracy with 0 test-time LLM tokens, compared with reported o3 at 45% and GPT-5 at 46%. DF + CC reaches 58.0% hard-tier accuracy and 86.6% overall accuracy.
- The best SLR hybrid, DF + CC + QO, reaches 86.7% overall accuracy at 138.8M tokens and $16.19, compared with reported o3 at 77.8% and $207.24.
- The no-reasoning-trace ablation is much worse on PBEBench-Hard: accuracy drops from 74.7% with CoT traces to 24.8% without CoT traces.
- In the historical linguistics transfer case, solver unions reach 80.1% accuracy zero-shot on 3,077 proto-daughter language pairs.

## Link
- [https://arxiv.org/abs/2605.05485v1](https://arxiv.org/abs/2605.05485v1)
