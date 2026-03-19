---
source: arxiv
url: http://arxiv.org/abs/2603.07229v1
published_at: '2026-03-07T14:24:25'
authors:
- Fouzi Harrag
- Mokdad Khemliche
topics:
- learning-to-rank
- bug-solution-recommendation
- stack-overflow-mining
- social-context-embedding
- developer-community
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# A Hybrid LTR-based System via Social Context Embedding for Recommending Solutions of Software Bugs in Developer Communities

## Summary
This paper proposes a Stack Overflow bug-solution recommendation system for developer communities, using learning to rank to rerank candidate answers by combining textual content with social-context features. Its goal is to help developers find more relevant bug-fix suggestions faster, without having to manually sift through large numbers of posts.

## Problem
- When developers search Stack Overflow for software error/bug solutions, there are many candidate Q&A posts, making manual retrieval time-consuming and often failing to find the best answer.
- Relying only on keyword search or basic similarity ranking makes it difficult to fully leverage post quality, user interactions, and community signals.
- This matters because Stack Overflow has accumulated a large amount of crowdsourced software engineering knowledge, and if it cannot be mined efficiently, much of its practical debugging value is wasted.

## Approach
- After preprocessing a bug report as a query, the system first uses **TF-IDF** to retrieve a batch of the most relevant Stack Overflow questions/answers as candidates.
- It builds a **Learning-to-Rank (LTR)** reranking model that combines four categories of features: statistical features, textual features, context/social features, and popularity features.
- On the text side, it cleans, tokenizes, removes stop words from, and stems titles, bodies, and code snippets, and extracts features such as length, readability, sentiment, code ratio, and title-body similarity.
- On the social and metadata side, it uses Stack Overflow community signals such as post scores, comments, views, favorites, and user information; answer scores are discretized into 1-5 relevance labels for training.
- It uses a TensorFlow Ranking-style deep learning ranking framework and compares different LTR training methods with two baseline variants.

## Results
- The paper states that the proposed system and **2** baseline variants were evaluated on **29,395** query-answer samples from Stack Overflow.
- The clearest main result is that, when recommending **Top-10** answers for each question, the system achieves close to **78%** "correct solutions."
- The authors also claim that the proposed system **outperforms two baselines** and performs better than **Google Search** and **Stack Overflow's built-in search** for the task of bug-solution recommendation.
- The excerpt **does not provide** more detailed core quantitative metrics, such as exact values for NDCG/MAP/MRR/Precision@k, nor the precise score gaps versus the baselines.

## Link
- [http://arxiv.org/abs/2603.07229v1](http://arxiv.org/abs/2603.07229v1)
