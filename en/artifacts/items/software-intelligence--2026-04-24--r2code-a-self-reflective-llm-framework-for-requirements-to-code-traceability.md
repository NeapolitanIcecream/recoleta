---
source: arxiv
url: http://arxiv.org/abs/2604.22432v1
published_at: '2026-04-24T10:47:56'
authors:
- Yifei Wang
- Jacky Keung
- Xiaoxue Ma
- Zhenyu Mao
- Kehui Chen
- Yishu Li
topics:
- requirements-traceability
- code-intelligence
- llm-for-software-engineering
- retrieval-augmented-generation
- software-maintenance
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# R2Code: A Self-Reflective LLM Framework for Requirements-to-Code Traceability

## Summary
R2Code is an LLM-based framework for linking natural-language requirements to the code that implements them. It aims to raise trace-link accuracy and cut LLM context cost by combining structured requirement-code alignment, self-checking, and adaptive retrieval.

## Problem
- The paper targets requirements-to-code traceability: given a requirement, find the file, class, or method that implements it.
- This matters for software maintenance, change impact analysis, and program understanding, where missing or stale trace links increase manual effort.
- Prior IR, embedding, and simple RAG methods often depend on word overlap, miss cross-level semantic matches between requirements and code, and waste tokens by passing broad context to the LLM.

## Approach
- R2Code breaks each requirement into four parts: intent, actions, conditions, and outputs. It also summarizes each code entity into four matching parts: function intent, control flow, variable effects, and return states.
- A Bidirectional Alignment Network (BAN) scores a requirement-code pair in two directions: top-down checks whether the code covers the requirement, and bottom-up checks whether the code logic matches the requirement. The final BAN score is a weighted mix of both directions.
- A Self-Reflective Consistency Verification (SRCV) step asks the LLM to explain why a link holds, then scores whether that explanation stays consistent with the original requirement. This consistency score adjusts the initial link confidence to reduce false positives.
- A Dynamic Context-Adaptive Retrieval (DCAR) step builds compact evidence for the LLM. It caches code summaries, estimates requirement complexity, changes the retrieval budget per requirement, and filters retrieved items by semantic overlap before final reasoning.

## Results
- On five public datasets across multiple domains and two programming languages, R2Code reports an average **F1 gain of 7.4%** over the strongest baselines.
- The paper states that R2Code consistently outperforms strong **IR baselines, dense retrieval, and RAG-based baselines** on these five datasets.
- With adaptive context control, R2Code reports up to **41.7% lower token consumption** than fixed or broader retrieval setups.
- The excerpt says the evaluation includes **precision, recall, F1, MRR, and precision/recall@k**, but it does not provide per-dataset numbers, baseline names with exact scores, latency values, or cost figures in the shown text.
- The robustness claim covers **five datasets**, multiple application domains, and **two languages: Java and C#**.

## Link
- [http://arxiv.org/abs/2604.22432v1](http://arxiv.org/abs/2604.22432v1)
