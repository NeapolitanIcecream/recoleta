---
source: arxiv
url: http://arxiv.org/abs/2604.06861v1
published_at: '2026-04-08T09:22:30'
authors:
- Shiqi Kuang
- Zhao Tian
- Kaiwei Lin
- Chaofan Tao
- Shaowei Wang
- Haoli Bai
- Lifeng Shang
- Junjie Chen
topics:
- software-engineering
- llm-agents
- issue-resolution
- requirements-engineering
- code-generation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# REAgent: Requirement-Driven LLM Agents for Software Issue Resolution

## Summary
REAgent improves software issue resolution by turning vague issue reports into structured requirements before patch generation. It adds requirement generation, requirement quality scoring, and iterative requirement refinement on top of an LLM agent workflow.

## Problem
- Repository-level issue resolution is hard for LLMs because issue reports often miss key context or use ambiguous language, which leads to wrong patches.
- The paper argues that most prior systems improve tools and workflows but still treat the raw issue description as the task specification.
- This matters because repository-level performance is still low; the paper cites DeepSeek-V3.2 at 83.30% on LiveCodeBench but only 15.56% on SWE-bench Pro, and it cites prior evidence that more than 70% of issues lack elements such as reproduction steps or validation criteria.

## Approach
- REAgent first builds an **issue-oriented requirement**: a structured specification extracted from the issue plus repository context. The requirement schema covers 9 primary attributes and 17 sub-attributes, including background, reproduction steps, expected behavior, root cause, modification location, and success criteria.
- A requirement generation agent explores the repository with tools such as file retrieval, browsing, and code analysis inside a Docker environment, then fills the requirement schema with the collected context.
- A requirement assessment agent generates a patch and 10 test scripts, then scores the requirement with **Requirement Assessment Score (RAS)**, defined as the fraction of generated tests passed by the patch. A patch is accepted only when RAS = 1.0.
- If RAS is below 1.0, a requirement refinement agent diagnoses requirement defects in three categories: conflict, omission, and ambiguity. It then revises the requirement and repeats the loop.

## Results
- On 3 benchmarks and 2 base LLMs, for 6 total settings, REAgent outperforms 5 representative or state-of-the-art baselines in every setting.
- The paper reports a **9.17% to 24.83%** increase in **% Resolved** over baselines, with an average improvement of **17.40%**.
- It also reports a **22.17% to 49.50%** increase in **% Applied** over baselines.
- Benchmarks: **SWE-bench Lite**, **SWE-bench Verified**, and **SWE-bench Pro**. Base models: **DeepSeek-V3.2** and **Qwen-Plus**.
- The paper also states that REAgent keeps outperforming iterative baselines as the iteration count **N** increases, and that ablation studies with 4 variants support the contribution of each main component.
- The excerpt does not provide per-benchmark raw scores, exact baseline names for each table, or full ablation numbers.

## Link
- [http://arxiv.org/abs/2604.06861v1](http://arxiv.org/abs/2604.06861v1)
