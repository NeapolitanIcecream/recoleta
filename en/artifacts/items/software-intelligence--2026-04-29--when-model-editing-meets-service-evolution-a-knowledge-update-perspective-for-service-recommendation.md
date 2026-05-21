---
source: arxiv
url: https://arxiv.org/abs/2604.26686v1
published_at: '2026-04-29T13:51:56'
authors:
- Guodong Fan
- Cuiyun Gao
- Chun Yong Chong
- Lu Zhang
- Jing Li
- Jinglin Zhang
- Shizhan Chen
topics:
- service-recommendation
- model-editing
- llm-agents
- constrained-decoding
- code-intelligence
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# When Model Editing Meets Service Evolution: A Knowledge-Update Perspective for Service Recommendation

## Summary
EvoRec updates an LLM-based service recommender as APIs and services change, then constrains decoding so the model only outputs valid, non-duplicate services.

## Problem
- Service repositories change through new services, API updates, deprecated services, and version changes, so recommenders trained on old data can return stale or invalid service pipelines.
- LLMs can map natural-language requirements or code context to service sequences, but they can hallucinate service names or calls that do not exist in the current catalog.
- Full retraining or frequent fine-tuning is costly when service facts change often.

## Approach
- EvoRec uses ROME-style locate-then-edit model editing to insert or update service facts inside selected Transformer feed-forward layers.
- Each edit maps a requirement pattern or code context key to an updated target service value, using cross-entropy for the target service and KL divergence to preserve unrelated behavior.
- A retrieval-augmented prompt supplies relevant service examples from the service corpus before generation.
- Trie-guided finite-automata constrained decoding masks invalid next tokens so generated names follow the service catalog and valid list structure.
- The decoder tracks used service IDs and blocks only branches whose remaining subtree has no unused service, which prevents duplicates while allowing shared prefixes.

## Results
- The paper claims an average relative improvement of 25.9% in Recall@5 over existing baselines on real-world service datasets.
- Under evolving service scenarios, EvoRec outperforms model fine-tuning approaches by 22.3% according to the excerpt.
- The excerpt states that EvoRec improves recommendation accuracy and adaptability while keeping maintenance cost low, but it does not provide dataset names, absolute Recall@5 values, model sizes, or a full baseline table.
- The strongest concrete validity claim is that FA and Trie decoding enforce valid service names, valid separators/end tokens, and service-level deduplication during generation.

## Link
- [https://arxiv.org/abs/2604.26686v1](https://arxiv.org/abs/2604.26686v1)
