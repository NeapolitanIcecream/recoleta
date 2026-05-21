---
source: arxiv
url: https://arxiv.org/abs/2605.03943v1
published_at: '2026-05-05T16:31:14'
authors:
- Pietro Cassieri
- Giuseppe Scanniello
- Seung Yeob Shin
- Fabrizio Pastore
- Domenico Bianculli
topics:
- code-intelligence
- llm-linting
- quantum-software
- static-analysis
- rag
- chain-of-thought
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Beyond Rules: LLM-Powered Linting for Quantum Programs

## Summary
The paper proposes LintQ-LLM+CoT and LintQ-LLM+RAG, LLM-based linters for quantum programs written in Qiskit. On 55 Qiskit files, both beat the rule-based LintQ baseline by F1 score.

## Problem
- Quantum programs have bugs tied to measurement, gates, register allocation, and Qiskit API constraints; generic Python linters and classical static analysis miss many of them.
- Rule-based quantum linters such as LintQ need hand-written CodeQL rules, which are costly to maintain as Qiskit APIs change.
- Better linting matters because false alarms waste developer time and missed quantum-specific bugs can make circuits invalid or misleading.

## Approach
- LintQ-LLM+CoT asks an LLM to check one quantum problem type at a time, using a system prompt and two automated user prompts.
- The first prompt gives the bug definition and asks the model to plan a detection strategy, summarize the code, apply the checks, and return JSON warnings with snippets and line numbers.
- The second prompt supplies the line-numbered Qiskit source file for analysis.
- LintQ-LLM+RAG adds one retrieved example from a FAISS vector index for the specific problem type, built from 157 manually verified true-positive Qiskit files embedded with OpenAI text-embedding-3-large.
- The evaluation compares LintQ, LintQ-LLM+CoT, and LintQ-LLM+RAG against manual ground truth on 55 files: 43 real files and 12 fault-injected files.

## Results
- On the 55-file corpus, LintQ-LLM+CoT reached F1 = 0.70, compared with LintQ's F1 = 0.41.
- LintQ-LLM+RAG reached F1 = 0.68, also above the LintQ baseline.
- LintQ-LLM+CoT had the highest recall at 0.96 and missed 3 true problems in the corpus.
- LintQ-LLM+RAG had the highest precision at 0.56, which the authors report as a reduction in false positives compared with CoT alone.
- The RAG knowledge base contains 157 files after removing 8 examples over the 8192-token limit; it is built from 165 manually verified true-positive warnings from the earlier LintQ dataset.
- The evaluation corpus contains 77 LintQ warnings before manual validation, spread across 10 quantum problem categories plus 5 clean files.

## Link
- [https://arxiv.org/abs/2605.03943v1](https://arxiv.org/abs/2605.03943v1)
