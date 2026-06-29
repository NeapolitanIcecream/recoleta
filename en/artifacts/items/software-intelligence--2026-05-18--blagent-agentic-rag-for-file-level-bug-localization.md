---
source: arxiv
url: https://arxiv.org/abs/2605.17965v1
published_at: '2026-05-18T07:20:13'
authors:
- Md Afif Al Mamun
- Gias Uddin
topics:
- bug-localization
- agentic-rag
- code-intelligence
- automated-program-repair
- software-agents
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# BLAgent: Agentic RAG for File-Level Bug Localization

## Summary
BLAgent is an agentic RAG pipeline for file-level bug localization in code repositories. It ranks likely faulty files from a bug report, then improves downstream automated repair by giving the repair system better file context.

## Problem
- File-level bug localization is a bottleneck for debugging, triage, root-cause analysis, and automated program repair because later steps fail when the wrong files are selected.
- SWE-bench repositories average over 11,000 functions and 168,000 statements, so direct statement-level search is too expensive for LLM-based repair systems.
- Prior RAG methods often use static retrieval over weak code chunks, while graph-based agent methods can be costly or require extra model training.

## Approach
- BLAgent indexes source files with AST-aware chunks, so chunks align with functions, classes, or other syntactic units instead of arbitrary text spans.
- It prepends each chunk with the relative file path, which helps match bug reports that mention modules, tracebacks, or package-qualified names.
- It rewrites each bug report into two retrieval queries: a structural query for identifiers and modules, and a behavioral query for observed versus expected behavior.
- It retrieves candidate files from both queries, keeps up to 15 candidates, and ranks files by the best matching chunk in each file.
- It reranks candidates in two phases: a ReAct agent scores file skeletons, then a one-shot LLM compares pruned file contexts for the top 5 files using the most relevant retrieved chunks.

## Results
- On SWE-bench Lite, BLAgent reaches 86.7% Top-1 accuracy and 0.900 MRR with a closed-source model.
- With an open-source model, it reaches 78.6% Top-1 accuracy and 0.851 MRR on SWE-bench Lite.
- The paper claims BLAgent beats LocAgent while using the same model at over 18× lower API cost.
- When integrated into Agentless, an open-source APR system, BLAgent improves issue resolution by over 20%.
- The paper reports that removing file-level localization from a multi-granularity localization pipeline caused a 94% drop in Top-5 accuracy and a 96% drop in statement-level MAP, which motivates the file-level focus.

## Link
- [https://arxiv.org/abs/2605.17965v1](https://arxiv.org/abs/2605.17965v1)
