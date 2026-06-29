---
source: arxiv
url: https://arxiv.org/abs/2605.29822v1
published_at: '2026-05-28T12:04:51'
authors:
- Tambon Florian
- Papadakis Mike
topics:
- code-correctness
- llm-code-validation
- test-generation
- specification-reasoning
- code-intelligence
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Inferring Code Correctness from Specification

## Summary
TRAILS estimates whether one generated program matches a natural-language specification by testing program behavior, then asking an LLM to judge the resulting input-output pairs against the spec. It targets the oracle problem for LLM-generated code, where users often lack trusted tests.

## Problem
- LLM-generated code can look plausible while violating the specification; this matters because developers and non-expert users may accept wrong code without a trusted oracle.
- Dynamic consensus methods need multiple candidate programs and many executions, which raises cost. Static code reasoning can miss runtime bugs and can vary across model runs.
- The paper studies single-candidate correctness inference using only the specification and the candidate code, with no trusted tests, examples, or user feedback.

## Approach
- TRAILS first asks an LLM to extract behavior categories and preconditions from the specification.
- For each category, it generates candidate inputs, runs them on the code, repairs invalid inputs within a fixed budget, discards invalid partitions, and removes duplicate inputs by code coverage.
- It executes the remaining inputs on the candidate code to collect concrete outputs.
- It gives an LLM the specification plus one input-output pair at a time, without showing the code, and asks for a binary correctness judgment.
- It aggregates the per-input judgments into a score and compares that score with a threshold, reported for τ = 0.6, 0.7, and 0.8.

## Results
- The evaluation uses LiveCodeBench v4 Lite with 119 tasks and CoCoClaNeL with 161 tasks after filtering. It tests Qwen3Coder-30B, Devstral-Small-24B, and Olmo3.1-32B-Instruct against HoarePrompt and Zero-Shot COT, averaged over 3 reruns.
- On LiveCodeBench, best MCC scores are Qwen 0.661 vs Zero-Shot COT 0.612 and HoarePrompt 0.605, Devstral 0.550 vs 0.463 and 0.357, and Olmo 0.606 vs 0.464 and 0.355. The relative MCC gains over Zero-Shot COT reach 8.01%, 18.79%, and 30.60% for those model cases.
- On CoCoClaNeL, best MCC scores are Qwen 0.259 vs Zero-Shot COT 0.186 and HoarePrompt 0.223, Devstral 0.261 vs 0.212 and 0.223, and Olmo 0.431 vs 0.332 and 0.269. The relative MCC gains over Zero-Shot COT reach 39.24%, 23.11%, and 29.82%.
- P4 also improves in the strongest cases: LiveCodeBench Qwen reaches 0.825 vs Zero-Shot COT 0.804, LiveCodeBench Olmo reaches 0.803 vs 0.723, CoCoClaNeL Qwen reaches 0.617 vs 0.512, and CoCoClaNeL Olmo reaches 0.711 vs 0.591.
- TRAILS costs more tokens: 18.6k to 37.5k tokens per task in Table 1, compared with 11.3k to 20.6k for HoarePrompt and 1.1k to 2.5k for Zero-Shot COT. The paper attributes the extra cost mainly to input repair, especially with crashing incorrect code and standard-input formatting in CoCoClaNeL.
- The abstract claims better stability across seeded runs and more unique code samples assigned correct labels than the baselines. The provided excerpt does not include the numeric stability or unique-label counts.

## Link
- [https://arxiv.org/abs/2605.29822v1](https://arxiv.org/abs/2605.29822v1)
