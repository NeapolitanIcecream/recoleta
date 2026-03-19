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
- interactive-html
- benchmarking
- llm-evaluation
- browser-automation
- code-generation
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# MiniAppBench: Evaluating the Shift from Text to Interactive HTML Responses in LLM-Powered Assistants

## Summary
This paper proposes **MiniAppBench** and **MiniAppEval** to evaluate large models' ability to move from text responses to generating interactive HTML MiniApps. The core argument is that evaluating only code correctness or static pages is no longer sufficient; evaluation must cover real-world principles and interaction logic.

## Problem
- Existing code/web benchmarks mainly measure algorithmic correctness, static layout, or fixed scripted flows, and cannot assess whether a model truly generates an interactive application that matches user intent.
- MiniApp generation is an open-ended task with no single ground-truth answer; the same requirement can have multiple valid implementations, so traditional reference-based evaluation is not suitable.
- This matters because human-AI interaction is shifting from pure text toward “executable responses,” requiring models to turn implicit common sense and real-world rules into interfaces and behaviors.

## Approach
- Build **MiniAppBench**: distill data from a real-world application scenario with **10M+ generations**, resulting in **500** tasks covering **6** domains and **25** fine-grained categories.
- The data is filtered through a multi-stage pipeline: from tens of millions of real queries, clean and sample down to **3,234** candidates, select **1,123** high-quality seed queries, expand to **1,974** candidates, and then stratified-sample the final **500** tasks.
- Each task is evaluated along three dimensions: **Intention** (whether the user goal is achieved), **Static** (static quality such as structure/syntax/accessibility), and **Dynamic** (runtime interactions, state transitions, and edge-case handling).
- Propose **MiniAppEval**: use an LLM agent + **Playwright** for human-like exploratory testing, collecting evidence through clicking, typing, dragging, and observing the DOM/logs/source code, rather than relying on fixed scripts or a single reference implementation.
- Standardize generation settings: require the model to output a single-file, directly runnable `index.html`, executed uniformly in an isolated Chromium environment to reduce interference from external factors.

## Results
- In terms of benchmark scale, the authors claim this is the **first** comprehensive benchmark for “principle-driven, interactive application generation,” containing **500** tasks across **6** domains, with a difficulty distribution of **30% Easy / 40% Medium / 30% Hard**.
- Model performance shows the tasks are difficult: among the open models in the table, **GLM-4.7** has the highest average pass rate at only **18.31%**; its **Easy/Mid/Hard** scores are **36.30% / 15.06% / 4.41%**, respectively.
- Other open models perform even worse: for example, **GLM-4.5-Air** averages **7.09%**, **Kimi-K2-Instruct** **6.19%**, **Qwen3-235B-A22B** **2.88%**, and **Qwen3-32B** **0.66%**, indicating that current models as a whole still struggle to reliably generate high-quality MiniApps.
- By domain, **GLM-4.7** performs relatively better on **Lifestyle 48.39%**, **Visualization 35.19%**, and **Tools 20.00%**, but remains clearly limited on **Science 10.49%** and **Games 12.50%**.
- The paper also claims that **MiniAppEval is highly aligned with human judgment** and can serve as a reliable evaluation standard; however, the provided excerpt does not include specific agreement figures.

## Link
- [http://arxiv.org/abs/2603.09652v1](http://arxiv.org/abs/2603.09652v1)
