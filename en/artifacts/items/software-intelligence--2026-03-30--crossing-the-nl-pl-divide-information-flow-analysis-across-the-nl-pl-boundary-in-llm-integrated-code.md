---
source: arxiv
url: http://arxiv.org/abs/2603.28345v1
published_at: '2026-03-30T12:14:24'
authors:
- Zihao Xu
- Xiao Cheng
- Ruijie Meng
- Yuekang Li
topics:
- llm-program-analysis
- taint-analysis
- program-slicing
- code-security
- nl-pl-boundary
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Crossing the NL/PL Divide: Information Flow Analysis Across the NL/PL Boundary in LLM-Integrated Code

## Summary
This paper studies a new blind spot in program analysis: data that crosses from code into an LLM prompt and comes back as text, JSON, SQL, or code. It introduces a taxonomy for describing how much of an input placeholder survives that boundary and shows that the taxonomy helps taint analysis and backward slicing.

## Problem
- Existing program analyses rely on summaries of how a call transforms inputs into outputs, but LLM calls do not expose such summaries because the prompt-to-output step is opaque and context-dependent.
- This breaks taint analysis, slicing, dependency tracking, and change-impact analysis at the natural-language/programming-language boundary, which matters for security and for basic developer tooling.
- In LLM-integrated apps, attacker-controlled input can pass through prompts and reappear in executable outputs such as SQL, shell commands, or code, creating injection and other security risks.

## Approach
- The paper defines the NL/PL boundary as the point where runtime program values are inserted into prompts and later influence LLM outputs consumed by code.
- It builds a 24-label taxonomy over two dimensions: information preservation level (L0 blocked to L4 lexical preservation) and output modality or form, including natural language, structured data, and executable artifacts.
- The taxonomy is grounded in quantitative information flow theory and applied per placeholder per callsite, so the same variable can get different labels in different prompt contexts.
- To build and test the taxonomy, the authors reconstruct real LLM callsites from Python code, infer placeholder values, generate model outputs, and label 9,083 placeholder-output pairs from 4,154 files.
- For taint propagation, they use a two-stage pipeline: taxonomy-based filtering predicts when a placeholder should propagate across the LLM boundary, then an LLM verifier checks the remaining cases.

## Results
- The labeled dataset covers 9,083 placeholder-output pairs from 4,154 real-world Python files.
- Human annotators reached Cohen's kappa = 0.79 on a 200-pair sample, and GPT-generated labels matched human consensus with kappa = 0.82.
- Coverage is near complete: 1 of 9,083 pairs was unclassifiable, about 0.01%.
- On taint propagation prediction, the two-stage pipeline reached F1 = 0.923 on 353 expert-annotated pairs from 62 sink-containing files.
- The paper reports cross-language validation on 6 real OpenClaw prompt-injection cases in TypeScript, but the excerpt does not provide a numeric score for that setting.
- For backward slicing, taxonomy-informed filtering reduced slice size by a mean of 15% in files with non-propagating placeholders, and four blocked labels accounted for nearly all non-propagating cases.

## Link
- [http://arxiv.org/abs/2603.28345v1](http://arxiv.org/abs/2603.28345v1)
