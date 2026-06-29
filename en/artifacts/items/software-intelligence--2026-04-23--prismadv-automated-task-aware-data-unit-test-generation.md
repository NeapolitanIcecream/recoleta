---
source: arxiv
url: http://arxiv.org/abs/2604.21765v1
published_at: '2026-04-23T15:18:50'
authors:
- Hao Chen
- Arnab Phani
- Sebastian Schelter
topics:
- data-validation
- code-intelligence
- llm-for-code
- test-generation
- prompt-optimization
relevance_score: 0.83
run_id: materialize-outputs
language_code: en
---

# PrismaDV: Automated Task-Aware Data Unit Test Generation

## Summary
PrismaDV generates data unit tests that use both dataset profiles and downstream task code, so the tests match the real assumptions of each task. The paper also adds SIFTA, a prompt-tuning method that updates the system from sparse test and task execution outcomes.

## Problem
- Existing data validation tools such as Deequ, TFDV, and Great Expectations mostly inspect data samples and ignore the code that consumes the data.
- That gap causes two failures: missed task-specific data bugs that break downstream jobs, and overly strict checks that raise false alarms for data conditions the task can handle.
- Writing and maintaining task-specific data tests by hand is costly, especially when one dataset feeds many downstream services that change over time.

## Approach
- PrismaDV builds a task-specific test by combining a sample dataset with the downstream task's source code.
- It profiles the data, detects which columns and column combinations the code accesses, and traces where those fields flow through the program.
- It uses LLM-based modules to turn those code locations into explicit natural-language data assumptions, stored in a bipartite data-code assumption graph that links columns to inferred assumptions and code spans.
- It converts that graph into executable constraints for a target validation system such as Deequ or Great Expectations, then filters out invalid constraints and any constraint that already fails on the known-good sample.
- SIFTA improves prompts over time using scarce execution feedback: it tracks which constraint failures coincide with downstream task failures via a failure-precision signal, backtraces them to assumptions and code, and feeds that signal into prompt optimization.

## Results
- The paper reports two new benchmarks: ICDBench with 63 hand-crafted constraint-discovery cases, and EIDBench with 60 downstream tasks across 5 public datasets and 25 error cases per dataset.
- PrismaDV beats strong baselines by more than 20 F1 points on ICDBench.
- PrismaDV beats task-agnostic and task-aware baselines by more than 26 F1 points on EIDBench.
- With SIFTA, learned prompts outperform both hand-written prompts and prompts from a generic prompt optimizer.
- The excerpt does not provide the exact final F1 values, baseline names, or per-dataset metric tables; it gives only the margin claims above.
- The authors also release code, benchmarks, and a prototype implementation at the stated GitHub repository.

## Link
- [http://arxiv.org/abs/2604.21765v1](http://arxiv.org/abs/2604.21765v1)
