---
source: hn
url: https://twitter.com/tplr_ai/status/2031388295972929720
published_at: '2026-03-10T22:51:03'
authors:
- rzk
topics:
- distributed-training
- llm-pretraining
- trustless-compute
- decentralized-ai
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Covenant-72B: Pre-Training a 72B LLM with Trustless Peers Over-the-Internet

## Summary
This item points to an X/Twitter post, but the only body text currently provided is a placeholder saying that JavaScript needs to be enabled, leaving almost no paper content available for analysis. Based on the title, the paper appears to discuss pre-training a 72B large language model via trustless peer nodes over the Internet, but the specific methods and results cannot be confirmed from the given text.

## Problem
- It attempts to address how to jointly complete pre-training of a very large model (72B) using distributed, trustless peers on the Internet **without relying on a centralized trusted cluster**.
- This problem matters because large-model training usually requires expensive, centralized infrastructure; if collaborative training over the open Internet is possible, it could significantly lower barriers to entry and increase decentralization.
- However, the provided text does not include the paper body, so its exact research problem definition, threat model, and system constraints cannot be confirmed.

## Approach
- Based on the title, the core mechanism is presumably to have multiple **trustless peer nodes over the Internet** jointly participate in pre-training a 72B LLM, without requiring mutual trust between nodes.
- The simplest interpretation is to split and coordinate a training workload that would normally run in a single controlled cluster across many Internet participants, while requiring some mechanism to handle unreliable or potentially malicious nodes.
- Because the content is missing, it is not possible to confirm which specific techniques were used, such as parameter synchronization, gradient verification, fault tolerance, incentive design, bandwidth optimization, or security protocols.
- It also cannot be confirmed whether “Covenant-72B” refers to training from scratch, continued pre-training, or another training paradigm.

## Results
- The given text contains **no verifiable quantitative results**, so no metrics, datasets, baselines, or comparison values can be extracted.
- The strongest concrete claim that can be confirmed from the title alone is that the authors claim to have completed pre-training work on a **72B-parameter LLM** called **Covenant-72B**, and that the training setup involved “**trustless peers over-the-Internet**”.
- It is not possible to confirm training throughput, convergence quality, cost, stability, security, or the degree of improvement over traditional centralized training.

## Link
- [https://twitter.com/tplr_ai/status/2031388295972929720](https://twitter.com/tplr_ai/status/2031388295972929720)
