---
source: arxiv
url: http://arxiv.org/abs/2603.04177v1
published_at: '2026-03-04T15:34:18'
authors:
- Alex Thillen
- "Niels M\xFCndler"
- Veselin Raychev
- Martin Vechev
topics:
- llm-for-code
- code-refactoring
- software-engineering-benchmark
- agent-evaluation
- static-analysis
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# CodeTaste: Can LLMs Generate Human-Level Code Refactorings?

## Summary
CODETASTE studies whether LLMs can not only “modify code correctly,” but also make refactoring decisions close to those chosen by human developers. The paper introduces a benchmark for real multi-file repository refactorings, showing that current frontier models perform strongly when executing refactorings from detailed instructions, but are clearly lacking in autonomously discovering what refactoring should be done.

## Problem
- Existing LLM coding agents can generate functionally correct patches, but often accumulate complexity, duplicated code, and architectural debt; truly sustainable software development requires **improving structure while preserving behavior**, i.e., refactoring.
- Existing refactoring benchmarks are mostly small-scope, low-difficulty tasks, making it hard to measure model capability in **real large codebases**, and they also cannot test whether models can **autonomously identify the refactorings humans would choose**.
- This matters because if agents cannot identify and execute appropriate refactorings, the codebases they build will become increasingly difficult to maintain, extend, and evolve.

## Approach
- Built **CODETASTE**: mined **100 real large multi-file refactorings** from GitHub historical commits, covering **87 repositories and 6 programming languages**.
- For each task, automatically generated a reproducible experimental environment, and evaluated using both **repository test suites** and **static rules**: requiring not only that functionality does not regress, but also that the code truly transforms from “undesired code patterns” into “desired code patterns.”
- The static rules use a rule language with **AST patterns and intra-file dataflow reasoning**, avoiding mere surface-level string matching and better capturing the semantic intent of refactoring.
- Designed two evaluation tracks: the **Instructed track** provides detailed refactoring instructions to test execution ability; the **Open track** provides only a vague improvement direction to test whether models can discover refactoring choices consistent with humans.
- In the Open track, further compared three modes: **Direct** for making changes directly, **Plan** for proposing a plan before implementation, and **Oracle Multiplan** for generating multiple plans first and then using a discriminator with full instructions to select the plan closest to the human solution.

## Results
- The benchmark itself is large in scale: each task requires modifying **91.52 files** and **2605.39 lines of code** on average; the maximum reaches **290 files** and **18821 changed lines**. Each instance runs **1638.53 tests** on average, and checks **29.66 additive rules** and **63.41 subtractive rules**.
- In the **Instructed track**, GPT-5.2 achieved the best average alignment score of **69.6%**; by comparison, SONNET 4.5 scored **32.4%**, GPT-5.1 CODEX MINI **34.6%**, and QWEN3 **11.8%**.
- On instruction execution, frontier models show relatively high IFR: GPT-5.2 **89.3%**, GPT-5.1 M **72.2%**, SONNET 4.5 **69.2%**; however, the gap in functional correctness rate PASS is substantial, with GPT-5.2 at **76.0%**, while GPT-5.1 M and SONNET 4.5 reach only **47.0%** and **43.0%**, respectively.
- In the **Open track**, where only vague goals are given, the best direct reasoning result is only **7.7% alignment** (GPT-5 CODEX); QWEN3 direct reaches just **2.3%**. The paper also summarizes that all models overall achieve **below 8% alignment** in this setting, showing that “knowing what to refactor” is far harder than “refactoring according to instructions.”
- **Propose a plan before implementation** helps significantly: GPT-5.2’s alignment improves from **7.7%** to **14.1%**, nearly doubling; the average improvement is close to **3 percentage points**, equivalent to **more than 50% relative gain**, and IFR can improve by as much as **72% relative gain**.
- Under **Oracle Multiplan**, GPT-5.2 reaches **19.4% alignment**, indicating that among the multiple candidate plans proposed by the model, there is often one closer to the human choice; however, SONNET 4.5 declines slightly from **10.2%** under Plan to **9.7%**. In addition, the highest PREC in the open track is only **21.0%**, indicating that models are often accompanied by many irrelevant changes.

## Link
- [http://arxiv.org/abs/2603.04177v1](http://arxiv.org/abs/2603.04177v1)
