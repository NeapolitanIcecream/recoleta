---
source: arxiv
url: http://arxiv.org/abs/2603.04601v1
published_at: '2026-03-04T21:00:33'
authors:
- Hung Tran
- Langston Nashold
- Rayan Krishnan
- Antoine Bigeard
- Alex Gu
topics:
- code-generation-benchmark
- web-application-development
- browser-agent-evaluation
- agentic-coding
- software-engineering
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Vibe Code Bench: Evaluating AI Models on End-to-End Web Application Development

## Summary
This paper introduces Vibe Code Bench, an end-to-end benchmark for evaluating whether models can directly build deployable web applications from natural-language requirements. The results show that even the strongest model achieves only a 61.8% workflow pass rate on the test set, indicating that “building a complete application from scratch” is still far from being solved reliably.

## Problem
- Existing code benchmarks mostly evaluate function completion, bug fixing, or local edits, and cannot measure the real capability of building a complete application from scratch.
- For real users, what truly matters is whether a model can turn a piece of non-technical requirements into runnable, deployable, interactive software, which directly affects whether AI can expand the population of software creators.
- There is a lack of a unified, implementation-agnostic, reproducible evaluation framework, making it difficult to compare different models fairly on full application development.

## Approach
- The authors built a benchmark containing **100** web application specifications, split into **50** public validation tasks and **50** hidden test tasks, covering **964** browser workflows and **10,131** substeps.
- Each model starts from a text specification in a containerized development environment and uses a browser, terminal, and common services (such as Supabase, MailHog, and Stripe) to build a complete application within at most **5 hours**.
- During evaluation, the system does not inspect source code or fixed DOM selectors. Instead, it uses an autonomous browser agent to operate the application directly like a user; a workflow is counted as passed when **≥90%** of its substeps succeed.
- The core idea can be understood simply as: **first let the model build the application independently, then let another browser agent actually click through it and run the full process to check whether a user can really use it.**
- The paper also includes evaluator alignment analysis, comparing consistency between different automatic evaluators and human annotations, verifying that evaluator choice can significantly affect conclusions.

## Results
- Across **16** frontier models, the best test-set result is **GPT-5.3-Codex: 61.77% ± 4.71**, followed by **Claude Opus 4.6: 57.57% ± 4.37**, **GPT-5.2: 53.50% ± 5.07**, and **Claude Sonnet 4.6: 51.48% ± 4.64**; the worst, **Grok 4.1 Fast Reasoning**, achieves only **1.20% ± 1.20**.
- This benchmark is more discriminative than existing code benchmarks: the paper states that **MiniMax M2.5 and Claude Opus 4.6** differ by only **2.8%** on **SWE-Bench**, but the gap reaches **42.7%** on **Vibe Code Bench**.
- By difficulty tier, GPT-5.3-Codex achieves **81.88% / 57.91% / 13.13%** accuracy on **Easy/Medium/Hard** tasks, while the all-model averages are **44.29% / 21.36% / 6.03%**, showing that high-difficulty tasks remain almost entirely unsolved.
- External integrations significantly reduce performance: GPT-5.3-Codex drops from **71.25%** on tasks with **no integrations** to **29.58%** on tasks requiring both **Email+Stripe**; the all-model average falls from **34.18%** to **13.49%**.
- The authors find that **self-testing behavior** during development is strongly correlated with final performance, with a Pearson correlation coefficient of **r = 0.72**, indicating that models that proactively test their own applications in the browser usually perform better.
- Evaluator choice materially affects results: pairwise step-level agreement between different evaluators ranges from **31.8%–93.6%**; based on this, the paper emphasizes that evaluator alignment itself is also an important problem in this area.

## Link
- [http://arxiv.org/abs/2603.04601v1](http://arxiv.org/abs/2603.04601v1)
