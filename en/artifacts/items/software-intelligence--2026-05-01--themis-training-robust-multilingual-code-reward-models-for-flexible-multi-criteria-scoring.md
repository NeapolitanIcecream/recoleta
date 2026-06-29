---
source: arxiv
url: https://arxiv.org/abs/2605.00754v3
published_at: '2026-05-01T16:07:34'
authors:
- Indraneil Paul
- "Goran Glava\u0161"
- Iryna Gurevych
topics:
- code-reward-models
- code-intelligence
- preference-learning
- multilingual-code
- software-post-training
- code-quality
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Themis: Training Robust Multilingual Code Reward Models for Flexible Multi-Criteria Scoring

## Summary
Themis trains code reward models that score generated code on correctness, runtime, memory, maintainability, and security in eight programming languages. The paper targets code post-training settings where execution tests are unavailable or too narrow.

## Problem
- Code post-training often uses test-case execution, which only works for executable, self-contained code and mostly rewards functional correctness.
- Real code quality also depends on runtime, memory use, maintainability, and security, so a single execution signal misses common developer needs.
- Existing code reward evaluations focus mainly on Python and valid-buggy solution pairs, so they do not test multilingual, multi-criteria scoring well.

## Approach
- The authors build Themis-CodeRewardBench with about 8.9k pairwise code preferences, 8 languages, and 5 criteria: functional correctness, execution efficiency, memory efficiency, readability and maintainability, and security hardness.
- They profile more than 50 code, math, and general reward models on this benchmark to find gaps in current code scoring.
- They create Themis-CodePreference with more than 350k code preference pairs and Themis-GeneralPreference with more than 110k general-domain preferences.
- They train Themis-RM models from 600M to 32B parameters using pairwise preference learning, with textual criteria that let users score any subset of the 5 code-quality dimensions.

## Results
- The excerpt gives no exact accuracy, win-rate, or ranking metric values for Themis-RM.
- The benchmark contribution is concrete: about 8.9k preferences, 8 languages, 5 scoring dimensions, and data drawn from correctness, efficiency, memory, maintainability, and security sources.
- The training data claim is concrete: more than 350k open-source code preference pairs plus more than 110k general preference pairs.
- The model suite spans 600M to 32B parameters and is claimed to show positive scaling trends.
- The paper claims cross-lingual transfer from diverse preferences and better reliability when training on multiple criteria, but the excerpt does not provide the numeric gains.

## Link
- [https://arxiv.org/abs/2605.00754v3](https://arxiv.org/abs/2605.00754v3)
