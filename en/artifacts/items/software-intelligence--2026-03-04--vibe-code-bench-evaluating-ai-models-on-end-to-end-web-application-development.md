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
- benchmarking
- code-generation
- web-app-development
- agentic-coding
- browser-agent-evaluation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Vibe Code Bench: Evaluating AI Models on End-to-End Web Application Development

## Summary
This paper introduces Vibe Code Bench, a benchmark specifically designed to evaluate whether models can **end-to-end build and deploy complete Web applications** from natural-language requirements. The results show that even the strongest model achieves only **61.8%** accuracy on the test set, indicating that reliable automatic development “from zero to one” is still far from solved.

## Problem
- Existing code benchmarks mostly evaluate function generation, patch fixing, or local tasks, and cannot measure whether a model can **build a complete usable application from scratch**.
- Real-world “vibe coding” requires spanning multi-file development, configuration, deployment, databases, authentication, payment/email integration, and frontend interaction, which is more important and more difficult than isolated coding tasks.
- The lack of a unified, reproducible, implementation-agnostic evaluation method can lead the industry to overestimate model capabilities in real software production.

## Approach
- The authors built a benchmark containing **100** Web application specifications: **50** public validation tasks and **50** held-out test tasks, totaling **964** browser workflows and **10,131** substeps.
- In a unified agent development environment, each model starts from a natural-language requirement and uses a browser, terminal, and common services (such as **Supabase, MailHog, Stripe**) to complete application development within at most **5 hours**.
- Evaluation does not inspect internal code; instead, an autonomous browser agent executes end-to-end user flows on the deployed application. If **≥90%** of substeps in a workflow succeed, that workflow is counted as passed.
- The authors evaluated **16** frontier models and measured accuracy, cost, latency, error patterns, and the relationship between “whether the model self-tests during generation” and final performance.
- They also conducted an evaluator alignment study, using cross-evaluator comparisons and external human annotations to test whether the browser evaluator is stable and reliable.

## Results
- The best model on the test set is **GPT-5.3-Codex: 61.77±4.71%**; next are **Claude Opus 4.6: 57.57±4.37%**, **GPT-5.2: 53.50±5.07%**, **Claude Opus 4.6 Thinking: 53.50±4.68%**, and **Claude Sonnet 4.6: 51.48±4.64%**. This shows that automatic development of complete Web applications remains a frontier challenge rather than a problem that is essentially solved.
- The benchmark has strong discriminative power: the paper states that **MiniMax M2.5 and Claude Opus 4.6** differ by only **2.8%** on **SWE-Bench**, but by **42.7%** on **Vibe Code Bench**.
- Difficulty stratification shows a sharp performance drop: for **GPT-5.3-Codex**, Easy/Medium/Hard are **81.88% / 57.91% / 13.13%** respectively; the averages across all models are **44.29% / 21.36% / 6.03%**.
- External integrations significantly increase difficulty: **GPT-5.3-Codex** scores **71.25%** on tasks without integrations, but drops to **29.58%** when both **Email+Stripe** are required; the all-model average falls from **34.18%** to **13.49%**.
- In terms of cost/latency, **GPT-5.3-Codex** reaches **61.77%** with an average cost of **$11.91** and latency of **75.8 minutes**; **Claude Opus 4.6** achieves comparable performance at lower cost/latency: **57.57%**, **$8.69**, **21.3 minutes**.
- Self-testing behavior is a strong predictive signal: the paper reports that the correlation between browser self-testing frequency during generation and final performance is **Pearson r = 0.72**; evaluator choice also matters significantly, with pairwise step-level agreement across different evaluators ranging from **31.8%–93.6%**.

## Link
- [http://arxiv.org/abs/2603.04601v1](http://arxiv.org/abs/2603.04601v1)
