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
- software-engineering
relevance_score: 0.81
run_id: materialize-outputs
language_code: en
---

# Enhancing Requirements Traceability Link Recovery: A Novel Approach with T-SimCSE

## Summary
This paper proposes T-SimCSE to recover traceability links between requirements and natural-language software artifacts when labeled data is scarce. Its core idea is to use SimCSE-based semantic similarity and then rerank candidate artifacts with "specificity" to improve retrieval quality.

## Problem
- The problem addressed is **requirements traceability link recovery**: automatically identifying the correct links between requirements and artifacts such as use cases, design documents, and tests.
- This is important because trace links directly affect software quality, change impact analysis, debugging, compliance, and maintenance efficiency.
- Existing IR methods are often inaccurate due to vocabulary mismatch, while supervised deep learning methods usually require large amounts of labeled data, which are very limited in practice.

## Approach
- Use the **pre-trained SimCSE** sentence embedding model to directly compute semantic similarity between requirements (source artifact) and target artifacts (target artifact), without additional training or fine-tuning on traceability datasets.
- First obtain a ranked candidate list based on requirement–target artifact similarity, then compute pairwise similarity among target artifacts to find other artifacts similar to high-probability candidates.
- Introduce the **specificity** metric: if a target artifact is similar to many other artifacts, it is more "general" and has lower specificity; if it is similar to only a few artifacts, it has higher specificity.
- Based on specificity, design a **rewarding / reranking** mechanism: more specific artifacts receive higher rewards and move up in ranking, while candidates that are semantically too general and easily resemble many artifacts are appropriately down-weighted.
- Finally, establish trace links on the reranked **top-K** target artifacts, thereby balancing direct semantic matching and indirect relational signals.

## Results
- The paper states that T-SimCSE was evaluated on **10 public datasets** and compared with other methods.
- The abstract explicitly claims that T-SimCSE performs better on **Recall** and **MAP**.
- The contribution section of the introduction further claims that T-SimCSE outperforms existing methods on **F1** and **F2** scores on the **MODIS** dataset.
- The paper also claims that its **MAP across all 10 datasets** is better than the baseline methods.
- However, the provided excerpt **does not include specific values** (such as absolute Recall/MAP/F1/F2 numbers, improvement margins, or baseline-specific figures), so the quantitative gains cannot be listed precisely.

## Link
- [http://arxiv.org/abs/2603.11800v1](http://arxiv.org/abs/2603.11800v1)
