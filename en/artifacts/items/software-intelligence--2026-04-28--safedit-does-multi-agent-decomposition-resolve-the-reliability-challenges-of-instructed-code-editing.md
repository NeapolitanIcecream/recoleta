---
source: arxiv
url: https://arxiv.org/abs/2604.25737v1
published_at: '2026-04-28T15:04:46'
authors:
- Noam Tarshish
- Nofar Selouk
- Daniel Hodisan
- Bar Ezra Gafniel
- Yuval Elovici
- Asaf Shabtai
- Eliya Nachmani
topics:
- instructed-code-editing
- multi-agent-systems
- code-intelligence
- llm-verification
- automated-program-repair
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# SAFEdit: Does Multi-Agent Decomposition Resolve the Reliability Challenges of Instructed Code Editing?

## Summary
SAFEdit is a GPT-4.1 multi-agent system for instruction-driven code edits. It claims higher EditBench task success by splitting each edit into planning, minimal code changes, real test execution, and up to 3 repair rounds.

## Problem
- Instructed code editing asks a model to modify existing code to match a natural-language request while preserving unrelated behavior; this matters because developer assistants often edit existing files rather than write fresh programs.
- EditBench shows that this task is hard: 39 of 40 evaluated models scored below 60% task success rate, and the best reported single-model baseline reached 64.8% under the most informative HIGHLIGHT setting.
- Common failures include misreading the instruction, changing unrelated code, missing affected call sites, and passing over test failures without a grounded repair step.

## Approach
- SAFEdit uses 3 specialized agents: a Planner writes a structured edit plan, an Editor applies only the required changes, and a Verifier runs the real unit tests in a sandbox.
- The Planner does not write code. It extracts visible code entities, states the edit intent, identifies the target location, lists required changes, and records constraints.
- The Editor treats the plan as the source of truth and tries to preserve formatting, structure, and unrelated code.
- Failed tests go through a Failure Abstraction Layer that converts raw logs into fields such as failed test, exception type, expected value, actual value, and suggested repair action.
- The edit-test-repair loop runs for at most 3 iterations, using the same GPT-4.1 backbone and test infrastructure as the ReAct baseline.

## Results
- On 445 EditBench tasks across 5 natural languages and 3 visibility variants, the evaluation produced 1,335 task-variant instances.
- SAFEdit reports 68.6% TSR in the main reported comparison, above claude-sonnet-4 at 64.8% by +3.8 percentage points.
- SAFEdit beats the implemented ReAct single-agent baseline, 68.6% vs. 60.0%, a +8.6 point gain under the same GPT-4.1 setup.
- The iterative refinement loop adds +17.4 percentage points over first-pass performance, according to the paper’s ablation claim.
- The dataset after filtering contains 89 tasks per instruction language across English, Polish, Spanish, Chinese, and Russian.
- The paper also claims its failure analysis shows fewer instruction-level hallucinations and no regression errors in SAFEdit compared with centralized single-agent reasoning baselines, but the excerpt does not provide full category counts.

## Link
- [https://arxiv.org/abs/2604.25737v1](https://arxiv.org/abs/2604.25737v1)
