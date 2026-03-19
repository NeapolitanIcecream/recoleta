---
source: hn
url: https://www.thedeepview.com/articles/nvidia-boosts-open-models-with-nemotron-3-super
published_at: '2026-03-11T23:09:15'
authors:
- teleforce
topics:
- open-models
- large-language-models
- agentic-ai
- mixture-of-experts
- long-context
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# Nvidia boosts open models with Nemotron 3 Super 120B parameter, 1M token context

## Summary
Nvidia has released Nemotron 3 Super, an open large model aimed at complex agentic systems, featuring 120B parameters, an MoE architecture, a 1 million token context window, and stronger reasoning capabilities. Its core selling point is not only open weights, but also open training data, recipes, and evaluation processes to advance the open ecosystem.

## Problem
- Complex agentic AI systems require stronger reasoning, longer context, and higher throughput, but existing open models remain limited in performance, efficiency, and reproducibility.
- Many “open-source” models only release weights without releasing training data and methods, making it difficult for the community to reproduce, customize, and continuously improve them.
- As the North American open-model ecosystem competes with open models such as DeepSeek and Qwen, it needs stronger and more transparent alternatives, which is important for both enterprise adoption and ecosystem development.

## Approach
- Nvidia introduced Nemotron 3 Super: a 120B-parameter open model for complex agentic systems, using a mixture-of-experts architecture and emphasizing advanced reasoning capabilities.
- The model supports a **1 million token** context window, aiming to handle longer-chain tasks, cross-document reasoning, and multi-step agent workflows.
- In addition to opening the model weights, Nvidia also released “data and recipes,” including pre-training and post-training datasets, training environments, and evaluation recipes, lowering the barriers to reproduction and secondary development.
- Officially, it is positioned as an upgrade that is more efficient, more accurate, and faster than its predecessor, with a “4x larger” Ultra model planned for the future.

## Results
- On the **Artificial Analysis benchmark**, Nemotron 3 Super reportedly outperformed several models from **OpenAI, Amazon, and Google**, though the article did not provide specific scores.
- On reasoning workloads, Nvidia claims it can be **2.2x faster than GPT-OSS**.
- Early adopter **CrowdStrike** said the model achieved **3x higher accuracy** in production compared with the model it had previously been using, and performed “exceptionally well” on internal threat-hunting benchmarks, though no specific benchmark names or figures were disclosed.
- In terms of model specifications, the key figures given in the article include **120B parameters** and a **1M token context window**.
- In terms of ecosystem investment, the report says Nvidia plans to invest **$26 billion over the next 5 years** to build the open-model ecosystem, but this is strategic investment information rather than a model performance metric.

## Link
- [https://www.thedeepview.com/articles/nvidia-boosts-open-models-with-nemotron-3-super](https://www.thedeepview.com/articles/nvidia-boosts-open-models-with-nemotron-3-super)
