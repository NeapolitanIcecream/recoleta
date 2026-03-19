---
source: arxiv
url: http://arxiv.org/abs/2603.03233v1
published_at: '2026-03-03T18:25:00'
authors:
- Zihang Zeng
- Jiaquan Zhang
- Pengze Li
- Yuan Qi
- Xi Chen
topics:
- ai-for-science
- multi-agent-systems
- bayesian-optimization
- code-generation
- low-code-platform
relevance_score: 0.11
run_id: materialize-outputs
language_code: en
---

# AI-for-Science Low-code Platform with Bayesian Adversarial Multi-Agent Framework

## Summary
This paper proposes a low-code platform for AI for Science that uses a Bayesian adversarial multi-agent framework to jointly improve code, test cases, and prompts, thereby reducing LLM hallucinations and error propagation. Its core claim is that scientific code can be generated more stably without fully trusting any single LLM, and that smaller models can achieve performance close to or even better than larger models.

## Problem
- In scientific code generation, LLMs can hallucinate not only in the code but also in the test cases; in multi-agent systems, these errors can propagate layer by layer, making the final results unreliable.
- AI4S tasks usually require complex workflows, domain constraints, and physical consistency. Ordinary unit tests are often insufficient to verify scientific correctness, and static prompting or self-correction methods are often inadequate.
- Domain experts often do not know prompt engineering, and the original requirements may be ambiguous or contain implicit expert knowledge, making it easy for models to misunderstand the task.

## Approach
- The framework uses 3 roles: the Task Manager is responsible for organizing the user's natural-language requirements into a plan and generating/updating tests; the Solution Generator produces candidate code; the Evaluator scores the code, tests, and prompts.
- It turns both “writing code” and “creating tests” into adversarial co-evolution: the TM acts like a challenger that continually designs tests better able to expose flaws, while the SG acts like a solver that continually fixes code to pass those tests.
- The key is not to rely entirely on LLMs for judgment, but to use a non-LLM Bayesian updating rule. Based on the historical performance score of prompts \(S_3\), it updates which test samples and reference code to use in the next round, thereby reducing dependence on the reliability of any single base model.
- To avoid actually executing all candidate code, they also use Bayesian optimization based on code-structure similarity, leveraging AST/code embeddings to estimate which candidates are more worth expensive testing.
- The platform also includes a low-code interface for non-programmer scientists: it first clarifies vague requirements and converts them into structured plans, subtasks, and scientific constraints, then enters iterative generation.

## Results
- On **SciCode**, the authors claim consistent gains across multiple base models; the maximum relative improvement reaches **87.1%**, corresponding to **Qwen3-8b**'s subproblem solve rate (without knowledge) improving from **13.2%** to **24.7%**.
- One representative result is that **Qwen3-14b + this framework** reaches a **30.6%** subproblem solve rate under the no-knowledge setting on SciCode, matching the **30.6%** baseline of **Qwen3-235B-A22b-Instruct**. Based on this, the authors claim that a small model can rival a model roughly **16×** larger.
- On **SciCode**, **Qwen3-32b + this framework** achieves a no-knowledge subproblem solve rate of **33.0%**, higher than the **30.6%** baseline of **Qwen3-235B**; this corresponds to the core claim in the abstract: with this framework, a **32B open-source model can outperform a 235B model** (where the comparison target is the baseline without the framework).
- Other SciCode results also show consistent gains, for example **GPT-4o** subproblem solve rate from **24.1% → 37.2%** (without knowledge, **+54.3%**), **Deepseek-v3** from **27.8% → 40.3%** (without knowledge, **+45.0%**), and **Claude-sonnet-4** from **31.3% → 42.7%** (without knowledge, **+36.4%**).
- On **ScienceAgentBench**, using **GPT-4o** as the base model, the authors claim a new SOTA, especially in **Valid Execution Rate (VER)**: **90.2%** (without knowledge) and **87.3%** (with knowledge), and they also claim to lead on **Success Rate** and **Code-Based Score**.
- The text does not provide the full table of ScienceAgentBench comparison values (Table 2 is truncated), so aside from VER, the exact baseline differences for the other metrics cannot be fully verified from the excerpt.

## Link
- [http://arxiv.org/abs/2603.03233v1](http://arxiv.org/abs/2603.03233v1)
