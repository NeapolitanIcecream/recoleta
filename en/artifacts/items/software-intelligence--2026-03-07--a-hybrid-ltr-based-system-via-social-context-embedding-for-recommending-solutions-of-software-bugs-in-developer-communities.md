---
source: arxiv
url: http://arxiv.org/abs/2603.07229v1
published_at: '2026-03-07T14:24:25'
authors:
- Fouzi Harrag
- Mokdad Khemliche
topics:
- learning-to-rank
- stack-overflow-mining
- bug-solution-recommendation
- social-context-embedding
- software-repository-mining
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# A Hybrid LTR-based System via Social Context Embedding for Recommending Solutions of Software Bugs in Developer Communities

## Summary
This paper proposes a Stack Overflow answer recommendation system for software bug resolution, feeding both textual content and community social context into a learning-to-rank model to return more relevant Top-k solutions for developers. The core goal is to reduce the time developers spend manually searching through massive Q&A collections and improve the success rate of finding usable fix suggestions.

## Problem
- When developers look for bug solutions on Stack Overflow, there are many candidate answers, and manual filtering is time-consuming and may still fail to find the best answer.
- Relying only on keyword matching or standard search often makes it difficult to simultaneously leverage signals such as question text, answer quality, user interactions, and post popularity.
- This matters because Stack Overflow is a high-value crowdsourced knowledge base for software debugging and maintenance; if it cannot be searched efficiently, repair efficiency and developer experience are directly affected.

## Approach
- Treat the bug report as a query: first clean, tokenize, remove stop words, and stem the bug title, description, and reproduction steps, then use TF-IDF to retrieve relevant candidates from the Stack Overflow question repository.
- Extract and jointly model four types of features for question-answer pairs: **statistical**, **textual**, **context**, **popularity**; this also incorporates social context such as comments, user information, votes, and other community signals.
- Use a deep learning Learning-to-Rank framework to rerank candidate answers, comparing point-wise, pair-wise, and list-wise ranking learning settings.
- Use answer vote scores as relevance labels, and divide the answers under each question into 5 relevance levels based on score, as the supervised training signal.
- For system implementation, parse the 2019-03-04 Stack Overflow data dump, focusing on the Posts, Comments, and Users datasets, and build a prototype system for real-time recommendation.

## Results
- The paper claims that when "recommending the top 10 answers for each question," the system can achieve **nearly 78% correct solutions**.
- The evaluation benchmark includes **29,395** queries and answers extracted from Stack Overflow; the authors say the proposed method outperforms **two baseline variants**, but the excerpt **does not provide finer-grained numerical metrics** (such as MAP, MRR, NDCG, or significance tests).
- The authors also report a **small-scale user study** in which **2 evaluators** compared the system's results with **Google search** and **Stack Overflow search**; the conclusion is that this system performs better on the bug solution recommendation task.
- Aside from the "Top-10 nearly 78%" result, the excerpt does not provide specific numerical gaps relative to the baselines, so the magnitude of improvement cannot be quantified precisely.

## Link
- [http://arxiv.org/abs/2603.07229v1](http://arxiv.org/abs/2603.07229v1)
