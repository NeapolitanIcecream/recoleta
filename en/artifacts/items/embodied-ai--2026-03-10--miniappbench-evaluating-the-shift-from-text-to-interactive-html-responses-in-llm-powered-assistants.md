---
source: arxiv
url: http://arxiv.org/abs/2603.09652v1
published_at: '2026-03-10T09:30:03'
authors:
- Zuhao Zhang
- Chengyue Yu
- Yuante Li
- Chenyi Zhuang
- Linjian Mo
- Shuai Li
topics:
- llm-evaluation
- interactive-html
- web-generation
- benchmark
- agentic-evaluation
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# MiniAppBench: Evaluating the Shift from Text to Interactive HTML Responses in LLM-Powered Assistants

## Summary
This paper introduces **MiniAppBench** and **MiniAppEval** to evaluate whether large models can go beyond text responses and generate interactive HTML MiniApps that follow real-world principles. The authors argue that existing code/web benchmarks overlook open-ended interaction and implicit rule modeling, making them inadequate for measuring this new form of human-AI interaction capability.

## Problem
- Existing benchmarks mainly evaluate **algorithmic correctness** or **static webpage reconstruction**, and cannot determine whether a model has truly generated an interactive application that matches user intent.
- MiniApps are open-ended tasks with no single correct answer; therefore, evaluation methods **based on fixed test cases, screenshot comparison, or reference implementation comparison** are not suitable.
- This matters because LLM assistants are shifting from “providing textual explanations” to “directly delivering executable interactive applications.” Without reliable evaluation, it is difficult to drive progress in real product settings.

## Approach
- Construct **MiniAppBench**: distill tasks from a real-world application with **10M+ generations**, resulting in **500** tasks covering **6** domains and **25** fine-grained categories.
- The data is filtered through a multi-stage pipeline: from tens of millions of real queries, cleaned down to **3,234** candidates, then narrowed to **1,123** high-quality seeds, expanded to **1,974** candidates, and finally stratified-sampled into **500** official tasks.
- Each task is organized around three evaluation dimensions: **Intention** (whether the user goal is achieved), **Static** (whether structure/syntax/accessibility are reasonable), and **Dynamic** (whether multi-step interactions, state transitions, and edge cases are correct).
- Propose **MiniAppEval**: using browser automation (Playwright) + an LLM agent to click, type, and observe execution results like a human, without relying on a single ground truth, but instead performing exploratory validation based on query-specific evaluation references.
- To ensure fairness, all models generate a single-file, directly runnable **index.html**, executed and scored independently in a unified Chromium sandbox.

## Results
- In terms of benchmark scale, MiniAppBench contains **500** tasks, with a difficulty distribution of **30% Easy / 40% Medium / 30% Hard**.
- In terms of task source, the authors state that the data comes from a real production environment and is distilled from **10M+** generation records, making it closer to real usage scenarios than synthetic benchmarks.
- Model experiments show that current LLMs still perform weakly: in the provided table, the best open-source model is **GLM-4.7**, with an overall average pass rate of only **18.31%**; its scores on **Easy/Mid/Hard** are **36.30% / 15.06% / 4.41%**, respectively.
- Other open-source models are even lower, for example **GLM-4.5-Air** averages **7.09%**, **Kimi-K2-Instruct** averages **6.19%**, **Qwen3-235B-A22B** averages **2.88%**, and **Qwen3-32B** averages **0.66%**.
- By domain, **GLM-4.7** is relatively stronger on **Lifestyle 48.39%**, **Visualization 35.19%**, and **Tools 20.00%**, but remains limited on **Games 12.50%** and **Science 10.49%**, indicating that consistently generating high-quality MiniApps across domains is still difficult.
- Regarding the evaluator itself, the abstract explicitly claims that **MiniAppEval has high agreement with human judgment** and can serve as a reliable standard; however, the current excerpt **does not provide specific correlation or agreement values**.

## Link
- [http://arxiv.org/abs/2603.09652v1](http://arxiv.org/abs/2603.09652v1)
