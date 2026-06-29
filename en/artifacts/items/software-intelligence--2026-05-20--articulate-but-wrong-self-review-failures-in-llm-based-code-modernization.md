---
source: arxiv
url: https://arxiv.org/abs/2605.21537v1
published_at: '2026-05-20T05:00:31'
authors:
- Gokul Chandra Purnachandra Reddy
- Aditya Lolla
- Harsha Sanku
topics:
- llm-code-modernization
- self-review
- behavioral-equivalence
- code-intelligence
- software-testing
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# Articulate but Wrong: Self-Review Failures in LLM-Based Code Modernization

## Summary
The paper finds that LLMs often change Python 2 behavior during Python 3 modernization, and same-model self-review misses many of those failures. Its main practical claim is that production modernization pipelines need external behavioral checks instead of plain self-approval.

## Problem
- LLM agents can produce code that runs and looks plausible while changing the legacy program's observable behavior.
- This matters because compile checks and basic tests may pass after migration, leaving downstream callers with different values or types.
- The paper tests whether the model that wrote the migrated code can catch its own behavior-changing output.

## Approach
- The authors build a 60-snippet Python 2 corpus: 20 semantic traps, 20 syntactic traps, and 20 benign controls that need no real modernization.
- They run 1,980 modernization calls across 11 production LLMs, 7 model families, and 3 prompt phrasings at temperature 0.
- A type-strict behavioral oracle compares each candidate against the Python 2 contract, including value and return type, so int-to-float drift is counted.
- After generation, the same model reviews the legacy snippet and its candidate output and answers whether behavior was preserved.

## Results
- Semantic traps drift in 39.7% of attempts versus 7.0% on benign controls and 12.7% on syntactic traps, across 660 calls per category.
- Numeric-semantics traps are the main failure class, with 57% drift; lazy-evaluation traps drift at 21%, while type-model and literal-syntax traps stay near baseline.
- Models agree on which snippets are hard: mean pairwise Pearson r=0.52 across 55 model pairs, with a core of numeric snippets failing for at least 8 of 11 models under every prompt.
- Same-model self-review endorses 83 of 262 semantic drift cases, or 31.7%; for numeric drift, it misses 75 of 207 cases, or 36%.
- Per-model self-miss rates range from 0% on five models to 100% on one model, and semantic drift rates range from 5.6% to 46.7% in the abstract and up to 65.0% in the per-model table.
- Method choices change measured rates: permissive equality lowers semantic drift from 39.7% to about 26.7%, while a fence-only parser raises benign-control drift from 7.0% to about 23%.

## Link
- [https://arxiv.org/abs/2605.21537v1](https://arxiv.org/abs/2605.21537v1)
