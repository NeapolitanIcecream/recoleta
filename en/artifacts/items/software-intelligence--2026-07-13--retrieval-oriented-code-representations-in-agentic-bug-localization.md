---
source: arxiv
url: https://arxiv.org/abs/2607.11046v1
published_at: '2026-07-13T03:18:22'
authors:
- Genevieve Caumartin
- Tse-Hsun
- Chen
- Diego Elias Costa
topics:
- code-retrieval
- bug-localization
- software-agents
- code-representation
- llm-ranking
- context-engineering
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Retrieval-Oriented Code Representations in Agentic Bug Localization

## Summary
The paper studies how the textual representation of repository files affects file-level bug localization for software agents. Role-aware summaries usually provide the best accuracy-cost balance, while combining representations and LLM reranking improves coverage.

## Problem
- Repository-scale bug localization must identify relevant files among hundreds or thousands of candidates before an agent can generate or validate a patch.
- Raw source code can exceed context limits and increase token and retrieval costs, while file paths omit useful semantic information.
- The study measures how representation choice affects retrieval accuracy, ranking quality, and representation footprint on Long Code Arena and SWE-bench Verified.

## Approach
- Compare five file representations: file paths, raw source code, role-aware summaries, detailed technical summaries, and synthetic bug-report summaries.
- Retrieve candidate files with BM25, dense embeddings, or LLMs, then use reciprocal rank fusion or an LLM to rerank candidates.
- Measure localization with MAP and Hit@k, while estimating cost through token-based representation footprint and summary-generation API cost.
- Test the strongest methods inside the Agentless file-localization pipeline.

## Results
- Role-aware summaries improve Hit@5 over file-path representations by up to 40% while using a representation footprint 10.4 to 20.9 times smaller than raw source code.
- Reciprocal rank fusion of complementary LLM retrieval results reaches Hit@5 of 89.3% on Long Code Arena and 83.4% on SWE-bench Verified.
- Combining representations improves localization by up to 31.9%, and LLM post-retrieval ranking improves results by up to 42.0%.
- In the Agentless case study, role-aware summaries with LLM ranking reach 94% Hit@6, a 4.7 percentage-point gain over the baseline.
- The paper reports no single representation that wins across every model, dataset, and pipeline stage; role-aware summaries provide the strongest overall cost-effectiveness trade-off, while raw source code can perform well at much higher cost.

## Link
- [https://arxiv.org/abs/2607.11046v1](https://arxiv.org/abs/2607.11046v1)
