---
source: arxiv
url: https://arxiv.org/abs/2605.29059v1
published_at: '2026-05-27T20:08:47'
authors:
- Kaihua Qin
- Dawn Song
- Arthur Gervais
topics:
- smart-contract-decompilation
- code-intelligence
- llm-evaluation
- software-benchmark
- semantic-testing
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# SCDBench: A Benchmark for LLM-Based Smart Contract Decompilers

## Summary
SCDBench is a benchmark for testing whether LLMs can decompile Ethereum bytecode into Solidity that compiles and behaves like the original contract. The strongest evaluated model still reaches full semantic success on only 42 of 600 contracts.

## Problem
- Smart contract source code is often unavailable: the paper states that more than 99% of Ethereum contracts are unverified, while smart contracts secure over $160B in assets.
- LLM decompilers can produce Solidity that looks plausible and compiles, yet changes behavior, which makes readability-only evaluation unsafe for audit and security work.
- Prior decompiler evaluations use narrow datasets, private or unclear sampling, and inconsistent metrics, so results are hard to reproduce or compare.

## Approach
- SCDBench contains 600 real-world Solidity contracts sampled from 772,736 exact-bytecode-unique verified Ethereum contracts, split into 200 easy, 200 medium, and 200 hard examples.
- Each task provides EVM bytecode as input and ground-truth Solidity source as the reference output.
- The benchmark evaluates outputs in four cumulative stages: format completeness, compilability, ABI recovery, and semantic consistency.
- Semantic checking replays fixed test cases against the original contract and the decompiled contract, comparing return data, revert status, emitted logs, and touched storage slots.
- The authors also test one same-model repair step: if generated Solidity has the required format but fails compilation, the model receives the compiler error and gets one chance to fix it.

## Results
- The dataset includes 227,383 concrete semantic test cases covering 14,553 public functions, with 77.8% average code coverage.
- GPT-5.3-Codex has the best format completeness: 564/600 contracts, or 94.0%. Opus 4.7 reaches 435/600, GLM-5 reaches 520/600, and GLM-5 instruct reaches 540/600.
- GPT-5.3-Codex has the best unrepaired compilation rate at 421/600 contracts, or 70.2%. After one repair step, GPT-5.3-Codex rises to 542/600, or 90.3%.
- Repair improves every tested model: Opus 4.7 rises from 341/600 to 415/600 compilable contracts, GLM-5 rises from 221/600 to 403/600, and GLM-5 instruct rises from 144/600 to 386/600.
- GPT-5.3-Codex with repair reports the best ABI recovery F1: 0.896 total, with 0.942 on easy, 0.928 on medium, and 0.861 on hard contracts.
- Semantic correctness remains low: the best model fully decompiles only 42/600 contracts under the benchmark’s semantic replay checks.

## Link
- [https://arxiv.org/abs/2605.29059v1](https://arxiv.org/abs/2605.29059v1)
