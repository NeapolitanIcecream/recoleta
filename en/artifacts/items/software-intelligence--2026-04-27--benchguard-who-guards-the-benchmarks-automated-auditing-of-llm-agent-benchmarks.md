---
source: arxiv
url: https://arxiv.org/abs/2604.24955v1
published_at: '2026-04-27T19:51:25'
authors:
- Xinming Tu
- Tianze Wang
- Yingzhou
- Lu
- Kexin Huang
- Yuanhao Qu
- Sara Mostafavi
topics:
- llm-agent-benchmarks
- benchmark-auditing
- execution-based-evaluation
- human-ai-review
- code-evaluation
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# BenchGuard: Who Guards the Benchmarks? Automated Auditing of LLM Agent Benchmarks

## Summary
BenchGuard audits execution-based LLM agent benchmarks by checking whether instructions, reference solutions, evaluation scripts, and environments agree. The paper claims it finds benchmark defects that human reviewers missed, at low audit cost.

## Problem
- Execution-based benchmarks can score agents incorrectly when task text, gold code, evaluator logic, or environment settings conflict.
- These errors matter because they can make valid agent solutions fail, make tasks unsolvable, and distort leaderboard scores.

## Approach
- BenchGuard takes four artifacts per task: instruction, ground-truth program, evaluation script, and environment configuration.
- A structured LLM audit checks the artifacts in six steps: task understanding, gold-program correctness, evaluator logic, task specification, environment checks, and deduplication.
- Deterministic static checks run with the LLM audit, and optional agent programs or execution logs add evidence when available.
- Findings are labeled by a 4-category, 14-subcategory defect taxonomy covering ground truth, evaluation, instruction, and environment issues; each finding includes severity, confidence, and cited evidence.

## Results
- On ScienceAgentBench, the audit found 12 defects confirmed by the original authors across 102 tasks, including fatal task errors, metric mismatches, and evaluators that reject correct outputs.
- On ScienceAgentBench definition-only auditing, Claude Opus 4.6 reached 83.3% exact recall and 91.7% recall with partial matches; the five-model union reached 91.7% exact recall and 100% with partial matches.
- Adding agent programs on ScienceAgentBench raised Claude Opus 4.6 to 91.7% exact recall and 100% recall with partial matches; the five-model union reached 100% exact recall.
- On BIXBench Verified-50, the five-model union exactly matched 20 of 24 expert-identified atomic issues, 83.3% exact recall, and matched 23 of 24 with partial matches, 95.8% recall.
- The best single BIXBench model, Claude Opus 4.6, exactly matched 13 of 24 issues, 54.2% recall, at $5.98 for 50 tasks.
- Full five-model audits cost $14.38 for 50 BIXBench tasks and $22.72 for 102 ScienceAgentBench tasks in definition-only mode; the paper also states that a 50-task bioinformatics audit costs under $15.

## Link
- [https://arxiv.org/abs/2604.24955v1](https://arxiv.org/abs/2604.24955v1)
