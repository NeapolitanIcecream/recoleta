---
source: hn
url: https://news.ycombinator.com/item?id=47317413
published_at: '2026-03-09T23:51:33'
authors:
- dsrtslnd23
topics:
- llm-architecture
- model-scaling
- mixture-of-experts
- inference-time-compute
- closed-vs-open-models
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Ask HN: Any informed guesses on the actual size/architecture of GPT-5.4 etc.?

## Summary
This is not a research paper, but a Hacker News question discussing the parameter scale, architectural form, and whether the “Pro” versions of closed-source models such as GPT-5.4, Gemini 3.1, and Opus 4.6 mainly rely on additional inference-time compute. The text itself provides no experiments, methods, or evidence, and only raises speculative questions about model size, MoE form, and inference orchestration.

## Problem
- It tries to clarify **how large current top closed-source large models actually are and what architectures they use**, compared with the best open models.
- It asks whether these models are all roughly in the same range, **around 1T parameters and possibly using MoE**, or whether closed-source models are still significantly larger.
- It further asks whether so-called **Pro versions** are separate models, or whether they mainly improve through **more inference-time compute, longer-chain reasoning, or stronger orchestration**; this matters for how the industry judges the source of capabilities and the structure of costs.

## Approach
- The text does not propose a research method; its core form is **open-ended speculation based on public product names and industry common sense**.
- The question is organized around three simple dimensions: **parameter scale**, **model architecture (such as MoE)**, and **differences in inference-time compute/orchestration**.
- It also introduces a comparison framework: placing **GPT-5.4, Gemini 3.1, Opus 4.6** and open models such as **GLM-5** on the same scale for an intuitive comparison.
- Put most simply, the “mechanism” of this content is: **asking the community for clues to judge whether capability differences come more from the trained base model or from extra runtime compute and toolchain orchestration投入的额外算力与工具链编排**.

## Results
- **It provides no quantitative results**, with no datasets, metrics, baselines, experimental setup, or numerical comparisons.
- The strongest concrete statements are only several unverified hypotheses: closed-source models may be on the order of **about 1T parameters** and **may use MoE**.
- The comparison targets raised but not answered in the text include: **GPT-5.4, Gemini 3.1, Opus 4.6, GLM-5**.
- The key judgment raised but not demonstrated by the text is that **the “Pro” version may not be a completely different model, but rather the same base model combined with more inference-time compute, longer reasoning, or stronger orchestration**.
- Because there is no evidence or experimentation, no reliable conclusion can be drawn about the magnitude of performance gains, the strengths and weaknesses of the architectures, or differences in scale.

## Link
- [https://news.ycombinator.com/item?id=47317413](https://news.ycombinator.com/item?id=47317413)
