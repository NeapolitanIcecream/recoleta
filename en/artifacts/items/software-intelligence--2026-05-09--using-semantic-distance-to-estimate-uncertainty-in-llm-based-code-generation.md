---
source: arxiv
url: https://arxiv.org/abs/2605.09023v1
published_at: '2026-05-09T16:02:54'
authors:
- Weilin He
- Arindam Sharma
- Cristina David
topics:
- code-generation
- uncertainty-estimation
- semantic-distance
- fuzz-testing
- code-intelligence
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Using Semantic Distance to Estimate Uncertainty in LLM-Based Code Generation

## Summary
The paper proposes SDE and DSDE, two execution-based uncertainty scores for LLM code generation that estimate whether the first generated program is likely wrong. They compare sampled programs by graded behavioral distance on shared fuzzed inputs, rather than treating every disagreement as equal.

## Problem
- LLM code generators produce plausible code with no correctness guarantee, which matters when generated code is used without complete external validation.
- Existing sample-based uncertainty methods often count behavioral disagreement as binary, so a one-case mismatch can get the same treatment as failure on every input.
- Developers need a reference-free signal that ranks generated code by likely correctness before running full validation or showing the code to a user.

## Approach
- The method samples K candidate programs for the same task and runs them on N shared fuzzed inputs.
- Programs with identical execution signatures are grouped into semantic clusters. Each signature records normal outputs and abnormal terminations by error type.
- The method assigns a graded distance between clusters by averaging per-input outcome differences. Normal output mismatches cost 1; abnormal cases use fixed weights a, b, and c.
- SDE averages weighted distances over all cluster pairs, using cluster probabilities. DSDE compares alternative clusters against the cluster containing the top-ranked program.
- The pipeline needs only generated code and executable inputs. It uses no model internals, embeddings, or LLM-as-judge calls.

## Results
- On LiveCodeBench with closed-source models, DSDE reaches AUROC 0.844 for GPT-3.5-Turbo, 0.844 for GPT-4o-mini, 0.808 for Gemini-2.5-Flash-Lite, and 0.825 for Claude Opus 4.5 in pass@1 failure prediction.
- On LiveCodeBench, DSDE beats the reported baselines on every listed model and metric. Example: for GPT-4o-mini, DSDE AUROC is 0.844, compared with DiffTrust 0.534, HonestCoder 0.646, and Semantic Entropy 0.607.
- DSDE correlates with partial correctness on LiveCodeBench. For GPT-4o-mini, Pearson r is -0.624 and Spearman rho is -0.624 against partial_pass@1.
- Generalization results include MBPP AUROC 0.752, LiveCodeBench AUROC 0.844, BigCodeBench AUROC 0.668, HumanEval-X Python AUROC 0.757, Java AUROC 0.745, and C++ AUROC 0.804 for DSDE under the reported GPT-4o-mini setting.
- The method is cheaper than the baselines in the runtime table: about 5.7 seconds per LiveCodeBench task at K=10 and N=10, compared with about 11 seconds for HonestCoder, 13 seconds for Semantic Entropy, and 27 seconds for DiffTrust.
- A smaller K=3, N=3 setting still reaches DSDE AUROC 0.783 on LiveCodeBench with GPT-4o-mini, about 93% of the AUROC at K=10, N=10.

## Link
- [https://arxiv.org/abs/2605.09023v1](https://arxiv.org/abs/2605.09023v1)
