---
source: hn
url: https://www.thedeepview.com/articles/nvidia-boosts-open-models-with-nemotron-3-super
published_at: '2026-03-11T23:09:15'
authors:
- teleforce
topics:
- open-llm
- agentic-ai
- mixture-of-experts
- long-context
- open-source-models
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Nvidia boosts open models with Nemotron 3 Super 120B parameter, 1M token context

## Summary
Nvidia has released the open-source large model Nemotron 3 Super, a 120B-parameter model aimed at complex agentic AI systems, emphasizing longer context, stronger reasoning, and more open training recipes. Its significance lies not only in model performance, but also in simultaneously opening weights, data, and training methods to help advance the open-source ecosystem.

## Problem
- Open-source large model ecosystems often open only the weights, without releasing training data, post-training workflows, or evaluation recipes, making it difficult for external teams to reproduce, customize, and deploy them reliably.
- Models for complex agentic AI systems need to combine long context, strong reasoning ability, and high efficiency; otherwise, they become costly, slow, and unstable in real production environments.
- The North American open-source model ecosystem has recently faced pressure in influence from Chinese open-source models, so it needs stronger and more transparent open models to improve ecosystem competitiveness.

## Approach
- Nvidia launched Nemotron 3 Super: a 120B-parameter model with a mixture-of-experts architecture and a 1M token context window, positioned as a foundation model for complex agentic AI systems.
- The core mechanism can be understood simply as enabling the model to reason over extremely long text spans, while using the mixture-of-experts architecture to call on different “specialized modules” more efficiently across tasks, thereby improving speed and accuracy.
- In addition to opening the model weights, Nvidia also released the training “data and recipes,” including pre-training and post-training datasets, training environments, and evaluation procedures.
- The release emphasizes reproducibility and customizability, with the goal of making it easier for developers and enterprises to adapt and deploy based on the same methodology.

## Results
- On the Artificial Analysis benchmark, Nemotron 3 Super outperformed several models from OpenAI, Amazon, and Google, though the article does not provide specific scores or a full comparison table.
- Nvidia says it can be **2.2x** faster than GPT-OSS on reasoning workloads.
- CrowdStrike said that after getting early access, the model achieved **3x** higher accuracy than the model it had previously used in production, and performed “exceptionally well” on internal threat hunting benchmarks.
- The model size is **120B parameters**, with a **1 million token** context window.
- Nvidia also said it will soon release an Ultra version that is “**4x larger**.”
- The article does not provide paper-style standard academic datasets, error bars, or detailed ablation studies, so the quantitative evidence mainly comes from benchmark ranking descriptions and feedback from early enterprise adoption.

## Link
- [https://www.thedeepview.com/articles/nvidia-boosts-open-models-with-nemotron-3-super](https://www.thedeepview.com/articles/nvidia-boosts-open-models-with-nemotron-3-super)
