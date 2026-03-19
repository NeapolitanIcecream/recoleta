---
source: arxiv
url: http://arxiv.org/abs/2603.11800v1
published_at: '2026-03-12T11:02:03'
authors:
- Ye Wang
- Wenqing Wang
- Kun Hu
- Qiao Huang
- Liping Zhao
topics:
- requirements-traceability
- trace-link-recovery
- simcse
- pretrained-language-models
- information-retrieval
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Enhancing Requirements Traceability Link Recovery: A Novel Approach with T-SimCSE

## Summary
This paper proposes T-SimCSE to recover traceability links between software requirements and natural-language artifacts when labeled data is scarce. The core idea is to first use SimCSE for semantic matching, and then rerank candidate artifacts using “specificity” to reduce incorrect links caused by overly general semantics.

## Problem
- This paper addresses the problem of **requirements traceability link recovery**: automatically identifying associations between requirements and natural-language artifacts such as use cases, design documents, and test cases.
- This is important because traceability directly affects software quality, requirements change analysis, debugging, compliance, and maintenance efficiency, while manual link creation is costly, error-prone, and hard to scale.
- Existing methods either rely on surface-level matching and thus suffer from semantic mismatch, or depend on large amounts of labeled data to train deep models, whereas in practice labeled data is very limited.

## Approach
- It first uses a **pre-trained SimCSE** sentence embedding model to encode requirements and target artifacts into vectors, and uses **cosine similarity** to obtain an initial ranking; the authors explicitly state that they perform **no additional training or fine-tuning**.
- It defines high-probability target artifacts (HPTA): for each requirement, it first selects a batch of candidate artifacts that are most similar to it.
- For each HPTA, it then finds other target artifacts similar to it (TRTA), treating these artifacts that are “close to correct candidates” as potentially indirectly relevant items and rewarding them to improve ranking.
- It introduces a new metric, **specificity**: if a target artifact is similar to many other artifacts, it is more “general” and has lower specificity; if it is similar to only a few artifacts, it is more “specific” and has higher specificity.
- Finally, it reranks through **similarity + differential reward/downweighting based on specificity**: more specific artifacts receive higher rewards, overly generic artifacts are appropriately downweighted, and then top-K are selected to establish trace links.

## Results
- The paper states that T-SimCSE was evaluated on **10 public datasets** and compared with other methods.
- The authors claim that T-SimCSE achieves **better MAP (Mean Average Precision) than the baselines across the 10 datasets**.
- The authors also claim that on the **MODIS dataset**, T-SimCSE outperforms existing methods on **F1 and F2** metrics.
- The abstract also specifically notes that T-SimCSE performs better in terms of **recall and MAP**.
- However, in the provided excerpt, **no specific numbers are given** (such as absolute MAP/F1/F2 values, improvement margins, specific baseline names, or significance tests), so it is not possible to report precise quantitative gains; the strongest concrete claim that can be confirmed is only that it “outperforms comparison methods across 10 public datasets, especially on MAP, recall, and F1/F2 on MODIS.”

## Link
- [http://arxiv.org/abs/2603.11800v1](http://arxiv.org/abs/2603.11800v1)
