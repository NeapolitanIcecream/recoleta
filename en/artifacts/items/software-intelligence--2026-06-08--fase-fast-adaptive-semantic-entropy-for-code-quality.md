---
source: arxiv
url: https://arxiv.org/abs/2606.09800v1
published_at: '2026-06-08T17:53:05'
authors:
- Shizhe Lin
- Ladan Tahvildari
topics:
- code-quality-estimation
- semantic-entropy
- code-generation
- multi-agent-systems
- uncertainty-quantification
- software-foundation-models
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# FASE: Fast Adaptive Semantic Entropy for Code Quality

## Summary
FASE estimates whether generated code is likely correct by measuring agreement among multiple code samples without ground-truth tests. It replaces LLM-based equivalence checks with embeddings, graph distances, and adaptive clustering, cutting runtime while improving correlation with Pass@1.

## Problem
- Multi-agent code generation can pass hallucinated or faulty code between agents, so a cheap quality signal is needed before errors spread.
- Standard semantic entropy groups outputs by functional equivalence, but LLM entailment checks are expensive and inconsistent across evaluator models.
- Structural entropy is faster, yet code with different syntax can still do the same job, and similar syntax can behave differently.

## Approach
- Generate 10 code samples per task, embed each sample with encoder-only models such as Qwen3-Embedding-8B, and compute cosine distances between all pairs.
- Build a minimum spanning tree over the pairwise distance graph to keep the closest relationships among samples and expose cluster boundaries.
- Set the clustering threshold from the mode of MST edge weights, scaled by the ratio between MST mean edge weight and full pairwise-distance mean.
- Use the resulting clusters as semantic equivalence classes, then compute entropy over those classes.

## Results
- On HumanEval, with 164 Python tasks, and BigCodeBench-hard, with 148 Python tasks, FASE with Qwen3-Embedding-8B reports a 25% average gain in Spearman correlation against Pass@1 compared with LLM-entailment semantic entropy.
- It reports a 19% increase in ROC-AUC against Pass@1 over the same LLM-entailment baseline.
- Runtime cost is about 0.3% of traditional semantic entropy methods because it removes LLM-driven pairwise equivalence checks.
- In intermediate Pass@1 tasks, MST edges between correct and failed code samples have distance ratios of about 3.4-3.6, compared with 1.7-1.8 in the full pairwise distance matrix.
- The evaluation uses four 7B coder models: Mistral-7B, CodeLlama-7B, DeepSeek-Coder-7B, and Qwen2.5-Coder-7B. Qwen2.5-Coder reaches Pass@1 = 1 on 101 HumanEval tasks and only 2 BigCodeBench-hard tasks in the reported setup.

## Link
- [https://arxiv.org/abs/2606.09800v1](https://arxiv.org/abs/2606.09800v1)
