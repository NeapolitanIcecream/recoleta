---
source: arxiv
url: http://arxiv.org/abs/2604.06742v1
published_at: '2026-04-08T07:09:10'
authors:
- Ruida Hu
- Xinchen Wang
- Chao Peng
- Cuiyun Gao
- David Lo
topics:
- llm-agents
- software-generation
- benchmarking
- cli-tools
- black-box-testing
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Evaluating LLM-Based 0-to-1 Software Generation in End-to-End CLI Tool Scenarios

## Summary
CLI-Tool-Bench is a benchmark for testing whether LLM agents can build complete CLI tools from scratch with only a natural-language spec and no repository scaffold. The paper shows that current top models still fail on most tasks, with overall success staying below 43%.

## Problem
- Existing code benchmarks mostly test function completion, issue fixing, or code filling inside a preset repository, so they miss a core 0-to-1 skill: planning and building the repository itself.
- Many benchmarks use white-box unit tests tied to specific internals, which does not match how users judge CLI tools in practice: by command behavior, output, and file-system effects.
- This matters because intent-driven software generation claims to produce runnable software from scratch, and current evaluation does not measure that claim well.

## Approach
- The paper introduces **CLI-Tool-Bench**, a benchmark of **100 real-world CLI repositories** across **Python (38)**, **JavaScript (16)**, and **Go (46)**, with easy, medium, and hard tasks.
- Each task gives the agent an **empty workspace** plus a de-identified requirement derived from the original project README, full `--help` interface docs, and one verified example per command class.
- The benchmark builds end-to-end tests with an **LLM-guided schema extraction and fuzzing pipeline**: it parses command/subcommand structure, flags, argument constraints, and then generates test commands.
- Evaluation is **black-box differential testing** in isolated Docker containers. The generated tool is compared with the human-written oracle on **return code**, **stdout**, and **file-system side effects**.
- Output matching uses a multi-level metric: **Exec**, **Exact Match**, **Fuzzy Match** with normalized edit-distance threshold **0.8**, and **Semantic Match** judged by GPT-5.4. The paper reports human validation for semantic judging with **Cohen's kappa > 0.9** on **1,000** sampled output pairs.

## Results
- The benchmark contains **100 repositories** spanning **9 domains**, with difficulty split into **42 easy**, **24 medium**, and **34 hard** tasks.
- Each command class gets **50 end-to-end test cases**, including positive and negative cases.
- The paper evaluates **7 LLMs** in **2 agent frameworks**, for **14 agent configurations** total.
- The main performance claim is that **top-tier models achieve less than 43% overall success**, which the authors use as evidence that 0-to-1 software generation remains hard.
- The paper also claims that **higher token consumption does not necessarily improve performance**.
- The authors report a behavioral pattern in generated repos: agents often produce **monolithic code structures** and can fall into **infinite generation loops**. The excerpt does not provide full model-by-model quantitative tables beyond the **<43%** headline.

## Link
- [http://arxiv.org/abs/2604.06742v1](http://arxiv.org/abs/2604.06742v1)
