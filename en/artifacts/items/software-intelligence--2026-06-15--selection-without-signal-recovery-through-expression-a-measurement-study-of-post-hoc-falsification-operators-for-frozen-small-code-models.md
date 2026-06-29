---
source: arxiv
url: https://arxiv.org/abs/2606.16999v1
published_at: '2026-06-15T17:36:23'
authors:
- Mehmet Iscan
topics:
- code-generation
- code-intelligence
- post-hoc-selection
- software-evaluation
- frozen-code-models
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Selection Without Signal, Recovery Through Expression: A Measurement Study of Post-Hoc Falsification Operators for Frozen Small Code Models

## Summary
This paper finds that semantic post-hoc operators do not improve frozen small code models over Best-of-N under matched compute, while harness fixes recover missed correct code. Its main useful result is M1, an extraction and signature-alignment step that raises accuracy without extra generation.

## Problem
- Frozen local code models around 0.5B to 1.5B parameters often produce plausible code that passes visible tests but fails hidden tests, which limits use in offline and privacy-constrained coding tools.
- Many post-hoc methods try to select, verify, repair, or refute generated candidates without training, but it is unclear whether they add signal beyond sampling more candidates.
- The practical risk is wasting engineering effort on semantic reranking when the candidate pool lacks correct programs or when visible-passing candidates cannot be separated without hidden-test leakage.

## Approach
- The study freezes the model, samples a shared candidate pool, gives each operator only the prompt, public tests, and candidates, and compares the returned program against Best-of-N using hidden tests.
- Best-of-N returns the first candidate that passes public tests. Every tested operator gets matched generator compute, so gains cannot come from extra samples.
- It evaluates 26 semantic output-space operators covering selection, verification, repair, counterexample search, elimination, sound vetoes, portfolios, generation conditioning, and compute allocation.
- It separately tests M1, which recovers code that the standard extractor missed and aligns a single defined function name to the public-test signature.
- It also tests ACE, an adaptive consensus early-stop rule that saves sampling work when enough candidates agree.

## Results
- Across the tested model cells and benchmarks, none of the 26 semantic post-hoc operators improves held-out accuracy over Best-of-N at matched compute.
- A coverage wall appears on hard tasks: at k=16, 16/30 tasks still have no hidden-correct candidate in the sampled pool.
- Consensus-based selection has little room to help: on two sound-veto-capable trap benchmarks, the model emitted the triggering bug on 0/10 and 2/16 tasks, never as the consensus majority; about 83% of real bugs were invisible to the sound metamorphic relations.
- The paper proves a finite-sample floor for do-no-harm claims: with zero observed harm, certifying population harm rate <= 0.05 at delta = 0.10 needs n >= 45.
- M1 is the only deployed accuracy gain. On DeepSeek-Coder-1.3B, it raises HumanEval+ from 29 to 41 tasks, a +12 gain with p = 2.4e-4 and b10 = 0; on MBPP+, it raises 128 to 161 tasks, a +33 gain with p = 1.2e-10 and b10 = 0.
- ACE saves about 19% of samples at the zero-harm operating point; an aggressive setting saves about 64% but has measurable regressions with b10 = 2.

## Link
- [https://arxiv.org/abs/2606.16999v1](https://arxiv.org/abs/2606.16999v1)
