---
source: arxiv
url: http://arxiv.org/abs/2604.13946v2
published_at: '2026-04-15T14:58:26'
authors:
- Duy Tung Doan
- Quang Huy Phung
- Dzung Nguyen
- Khac-Hoai Nam Bui
topics:
- multi-agent-code-generation
- code-intelligence
- plan-code-coevolution
- automated-debugging
- llm-agents
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# CollabCoder: Plan-Code Co-Evolution via Collaborative Decision-Making for Efficient Code Generation

## Summary
CollabCoder is a multi-agent code generation method that updates either the plan or the code during debugging instead of keeping the original plan fixed. The paper claims this raises Pass@1 on standard and contest-level benchmarks while cutting token use and API calls against recent agent baselines.

## Problem
- Existing agentic code generators often keep the initial plan fixed, even when test failures show the plan itself is wrong or incomplete.
- Many systems debug code in a reactive trial-and-error loop, with weak error attribution and little use of prior failed attempts.
- This matters because complex programming tasks on benchmarks like LiveCodeBench and xCodeEval need both correct high-level reasoning and correct implementation; wasted retries increase cost and still miss bugs.

## Approach
- CollabCoder uses three agents: a planning agent, a coding agent, and a debugging agent.
- The debugging agent has a Collaborative Decision-Making module that analyzes three signals each iteration: plan quality, code quality, and plan-code alignment.
- It then chooses one action for the next step: revise the plan or revise the code. The choice is made by aggregating confidence and consistency scores with fixed trust weights: plan 0.4, code 0.3, alignment 0.3.
- A Reasoning Trajectory module stores debugging history across iterations and turns past failures plus current test feedback into an updated repair strategy, so the system avoids repeating weak fixes.
- The process runs iteratively until tests pass or the iteration budget ends; the paper uses 5 iterations for CollabCoder.

## Results
- On basic code generation benchmarks with **Qwen2.5-Coder-32B**, CollabCoder gets **82.50 average Pass@1**, ahead of **CodeSIM 80.22**, **MapCoder 79.84**, and **ThinkCoder 77.02**. It uses **2468.22 / 1606.88 token I/O** and **4.12 API calls**, versus **CodeSIM 2191.03 / 2593.04** and **4.87 calls**, and **MapCoder 5848.39 / 3309.55** and **9.05 calls**.
- With **GPT-4o mini**, CollabCoder reaches **83.25 average Pass@1**, above **CodeSIM 81.52** and **MapCoder 77.80**. Its per-dataset scores are **96.34 HE**, **84.76 HE-ET**, **91.69 MBPP**, **60.20 MBPP-ET**.
- With **Seed-Coder-8B**, CollabCoder gets **76.26 average Pass@1**, slightly above **CodeSIM 75.51** and above **ThinkCoder 71.08** and **MapCoder 68.78**; it uses **5.06 API calls** versus **6.69** for CodeSIM and **9.84** for MapCoder.
- On contest-level benchmarks using **GPT-4o mini**, CollabCoder reports **41.96 Pass@1 on LiveCodeBench** and **47.16 on xCodeEval**, for **44.56 average**. Baselines are **CodeSIM 39.53 average** and **MapCoder 37.70 average**.
- On those contest benchmarks, CollabCoder uses **12.27 API calls**, lower than **17.16** for CodeSIM and **22.41** for MapCoder, with token I/O **15155.93 / 4491.37** versus **20907.82 / 13151.10** for CodeSIM and **28437.65 / 17692.18** for MapCoder.
- The abstract summarizes the harder-benchmark gain as **11-20%** over strong baselines on **LiveCodeBench** and **xCodeEval**, with **4-10 fewer API calls per execution** on average.

## Link
- [http://arxiv.org/abs/2604.13946v2](http://arxiv.org/abs/2604.13946v2)
