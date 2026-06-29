---
source: arxiv
url: https://arxiv.org/abs/2605.09730v3
published_at: '2026-05-10T19:57:32'
authors:
- Will LeVine
- Brendan Evers
- Sam Saltwick
- Abhay Venkatesh
topics:
- tool-use-agents
- code-intelligence
- inference-time-refinement
- software-agents
- rubric-evaluation
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# RubricRefine: Improving Tool-Use Agent Reliability with Training-Free Pre-Execution Refinement

## Summary
RubricRefine improves code-mode tool-use agents by checking tool contracts before the agent runs code. It generates a task-specific rubric, uses it to find contract errors, and repairs the code with zero execution attempts.

## Problem
- Code-mode agents can produce executable programs that call several tools, pass data between calls, and format final answers, but many failures do not raise runtime errors.
- The main failures are wrong output shape, wrong tool routing, broken argument provenance, and bad call ordering; these can finish execution and still return the wrong answer.
- This matters when a live tool call can change external state, cost money, hit rate limits, or violate safety constraints, because retrying after failure may be unacceptable.

## Approach
- The method takes the task instruction and tool registry, then generates a task-specific rubric with explicit checks for tool choice, output contracts, call signatures, and data provenance.
- A verifier scores candidate code on a 1-10 scale and returns item-level PASS/FAIL feedback with reasons and concrete repair directions.
- The generator revises the code using the rubric and verifier feedback before any environment execution occurs.
- The loop stops when the code scores 10/10, when patience is exhausted, or when the round limit is reached; the best-scoring candidate becomes the single executable action.
- The method is training-free and uses inference-time verification rather than model fine-tuning or execution feedback.

## Results
- On M3ToolEval, RubricRefine averages 0.86 success across seven models, compared with 0.62 for single-pass CodeAct, a +0.24 absolute gain.
- RubricRefine is best on every tested model: GPT-4.1-mini 0.86, GPT-4o 0.86, o3-mini 0.85, GPT-4.1 0.85, Gemma-4-26B 0.85, Qwen3.6-27B 0.84, and Sonnet-4.6 0.88.
- Against CodeAct, the paper reports per-model gains of +0.14 to +0.38 on M3ToolEval, with paired t-tests at p<0.001 for every model.
- RubricRefine beats Self-Debug, which uses real execution feedback, by +0.12 absolute on average: 0.86 vs. 0.74.
- Fixed RubricRefine improves over Self-Refine on six of seven models by +0.09 to +0.20, while full RubricRefine improves over Fixed RubricRefine by +0.04 to +0.12 on every model.
- On API-Bank, a mostly single-step benchmark, performance is flat or within noise of CodeAct on the four OpenAI models, which matches the claim that the method helps most when tasks contain inter-tool contracts.

## Link
- [https://arxiv.org/abs/2605.09730v3](https://arxiv.org/abs/2605.09730v3)
