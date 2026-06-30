---
source: arxiv
url: https://arxiv.org/abs/2606.30524v1
published_at: '2026-06-29T16:29:31'
authors:
- Abu Saleh
- Tesfay Welegebreal Tesfay
- Phuong T. Nguyen
- Juri Di Rocco
- Muhammad Umar Zeshan
- Davide Di Ruscio
topics:
- readme-generation
- multi-agent-systems
- rag
- software-documentation
- code-intelligence
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# The Illusion of Agentic Complexity in README.md Generation: Evaluating Single-Agent vs. Multi-Agent RAG Systems

## Summary
The paper tests whether multi-agent RAG is worth its cost for generating GitHub README files. It finds that a single-agent RAG system matches autonomous MAS on lexical scores at much lower cost, while human-provided plans give the best quality.

## Problem
- README files are often written by hand, become incomplete or outdated, and affect how users understand and adopt a repository.
- Multi-agent software engineering systems often assume that splitting work across agents improves output, but the paper tests whether that extra cost helps for README generation.
- The task matters because repository-level documentation needs source-code grounding, correct commands, clear sections, and consistent formatting.

## Approach
- The study compares four outputs: Single-Agent RAG, autonomous MAS RAG, Dev-Plan MAS, and LARCH, with original README files used as reference.
- The dataset contains 180 GitHub repositories created after August 2025: 118 Python, 49 JavaScript, and 13 Go. Dev-Plan is tested on a 20-repository subset.
- The pipeline removes existing Markdown files, indexes source and configuration files with syntax-aware chunking, embeds chunks with `text-embedding-3-small`, stores them in ChromaDB, and uses `gpt-5.1` for generation.
- The Single-Agent system retrieves section-relevant code chunks and writes the whole README in one prompt. MAS uses a profiler, planner, section writers, reviewer, and aggregator. Dev-Plan replaces the MAS planner with a human-written JSON plan.
- Evaluation uses ROUGE, BERTScore, token count, runtime, manual coverage against a 12-section README taxonomy, and an LLM judge scored on a 10-point scale.

## Results
- On 180 repositories, Single-Agent slightly beats autonomous MAS on ROUGE-L F1: 0.2007 vs. 0.1964. Both beat LARCH, which scores 0.1022 ROUGE-L F1.
- Single-Agent uses 7,840 tokens and 40 seconds per README on average. MAS uses 56,242 tokens and 78 seconds, about 7.1x more tokens. The paper reports this as an 86% token reduction for Single-Agent compared with MAS.
- Dev-Plan has the best reported lexical scores: ROUGE-L F1 0.2323 and BERTScore F1 0.8230, but it costs 79,196 tokens and 148 seconds per README on average.
- On the 20-repository structural evaluation, MAS has the highest manual precision at 0.982, with recall 0.696 and F1 0.814. Single-Agent has precision 0.776, recall 0.492, and F1 0.602.
- Dev-Plan has the best judged usefulness: mean LLM-judge score 8.60, 53.75% first-place win rate, and 1.25% fail rate. MAS scores 7.55 with 16.25% win rate and 2.50% fail rate. Single-Agent scores 7.25 with 10.00% win rate and 6.25% fail rate.
- Original README files score lower than Dev-Plan in the structural study: precision 0.724, recall 0.667, F1 0.694, mean judge score 7.36, and 17.50% fail rate.

## Link
- [https://arxiv.org/abs/2606.30524v1](https://arxiv.org/abs/2606.30524v1)
