---
source: arxiv
url: https://arxiv.org/abs/2607.18642v1
published_at: '2026-07-21T02:23:22'
authors:
- Yuxiang Ji
topics:
- code-dataset-generation
- contamination-resistance
- code-benchmarking
- synthetic-code
- program-transpilation
- refactoring-evaluation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Spaghetti Architect: A Contamination-Resistant, By-Construction-Labelled, Multi-Language Code Dataset Generator

## Summary
Spaghetti Architect generates fresh, oracle-validated code datasets whose semantics, language, intrinsic problem size, and incidental messiness are controlled independently. It supports contamination-aware evaluation and shows that computational accuracy can collapse with problem scale while refactoring equivalence remains high for capable models.

## Problem
- Mined code corpora do not provide known-optimal references, reliable semantic labels, controlled difficulty, or independent variation of problem size and code messiness.
- Public code samples may have appeared in model training data, making evaluation scores difficult to interpret as capability rather than memorization.
- Code evaluation also needs verified clean/messy pairs to test comprehension, refactoring, and robustness without confounding semantics with presentation.

## Approach
- An anti-optimization transpiler converts a validated, language-agnostic JSON intermediate representation into deliberately redundant programs in Python, JavaScript, Go, Java, and C++.
- A compile-run validator compares every emitted program with a reference oracle, making correctness a construction and validation property rather than an inferred label.
- Composable, strictly nested anti-pattern profiles vary incidental messiness while intrinsic knobs vary problem size, including operation count and scale, at fixed semantics.
- A public development split and freshly minted private held-out splits use secret seeds, literal changes, structural variants, and scale/depth variants to measure contamination resistance.
- The released artifact is MIT-licensed, dependency-free at its core, and includes a 100-instance public development reference split plus regenerable datasets.

## Results
- The public split crosses 50 base samples with five non-clean messiness profiles in five languages, producing 250 base-sample/profile cells with no missing cells; the messiness and intrinsic-size axes have Spearman correlation rho = 0.00 by construction.
- Across four open models, public development and freshly reminted Tier-A comprehension scores differ by at most 0.012, while refactoring semantic-equivalence scores differ by at most 0.011, supporting the freshness protocol.
- Refactoring equivalence forms a capability ladder from 0.73 to 0.99 and remains invariant to intrinsic scale for capable models, whereas arithmetic-aggregation exact-match accuracy falls to 0 for the strongest tested model as intrinsic scale increases.
- Removing generator annotations reduces refactoring semantic-equivalence scores by 0.173 for the weakest model versus 0.017 for the strongest; the weakest-to-strongest impact ratio is 6.5x to 9.9x in six of seven fits.
- The incidental messiness knob moves established complexity and readability metrics, but its effect on model accuracy is not established in the reported experiments; that question remains future work.
- Tier-B and Tier-C accuracy differences are confounded by operation count, family composition, and depth: standardizing Tier-A to Tier-B operation-count distributions shrinks the marginal gap by 60-90 percentage points, so the evidence supports freshness under reminting rather than a general novelty penalty.

## Link
- [https://arxiv.org/abs/2607.18642v1](https://arxiv.org/abs/2607.18642v1)
