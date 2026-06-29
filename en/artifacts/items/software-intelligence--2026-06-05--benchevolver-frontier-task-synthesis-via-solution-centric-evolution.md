---
source: hn
url: https://benchevolver.github.io/
published_at: '2026-06-05T23:39:52'
authors:
- matt_d
topics:
- code-benchmarking
- code-intelligence
- software-foundation-models
- automated-evaluation
- rl-training
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# BenchEvolver: Frontier Task Synthesis via Solution-Centric Evolution

## Summary
BenchEvolver generates harder verified coding tasks by changing the reference solution first, then writing the problem and tests around that executable solution. It targets benchmark saturation in code evaluation, where current models already score near ceiling on easier LiveCodeBench splits.

## Problem
- Current coding benchmarks are saturating: frontier models exceed 99% Pass@1 on LiveCodeBench easy and over 90% on average, so these tests no longer separate strong models well.
- Hand-building harder coding datasets is slow and costly, which limits measurement of progress in code models.
- Many generated tasks change the wording or surface story while keeping similar reasoning, so they do not create enough new algorithmic demand.

## Approach
- BenchEvolver mutates the reference solution first to require a stronger algorithm, then derives the statement, examples, and hidden tests from that executable solution.
- A Proposer creates evolved solutions and task text; an Evaluator checks correctness and measures difficulty; Memory feeds accepted lineages and past failures into later search.
- Verification triangulates the evolved reference solution, a brute-force solver, and a statement-only oracle, then runs bounded repair when inconsistencies appear.
- A task is accepted only when a target model panel fails more often than on the seed task, so difficulty is measured through actual model performance.
- Example lifts include changing interval intersection for array differences into digit-DP for XOR constraints, and changing RK4 integration into nonlinear parameter and initial-state estimation with Gauss-Newton.

## Results
- On LiveCodeBench, the paper reports that frontier models exceed 99% Pass@1 on the newest easy split and over 90% on average, motivating harder evaluation.
- The authors built a 91-problem benchmark from 64 human-vetted evolved tasks and 27 difficult original LCB-v6 tasks; every problem passed correctness, quality of at least 3/5, and difficulty-range gates.
- On that benchmark, frontier Pass@1 spans 27.5% to 62.6%, giving clearer separation among strong models than saturated easy splits.
- Averaged across evaluated models, the Hard split drops from 87.0% to 45.7% Pass@1, a 41.3-point absolute reduction.
- Six competitive-programming experts reviewed 207 evolved problems across 72 seeds and rated the evolved tasks more novel, much harder, broader in algorithm coverage, and clearer than the seeds.
- With gpt-oss-20b as both evolver and target, RL training on evolved tasks improves held-out coding performance beyond training on original seeds alone; the excerpt gives no exact gain for this result.

## Link
- [https://benchevolver.github.io/](https://benchevolver.github.io/)
