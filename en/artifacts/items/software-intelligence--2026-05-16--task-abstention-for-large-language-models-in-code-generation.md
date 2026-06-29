---
source: arxiv
url: https://arxiv.org/abs/2605.17029v1
published_at: '2026-05-16T14:58:11'
authors:
- Yanke Zhou
- Yuhao Tan
- Senrong Xu
- Zenan Li
- Yuan Yao
- Taolue Chen
- Xiaoxing Ma
topics:
- code-generation
- task-abstention
- code-llms
- hallucination-detection
- execution-based-evaluation
- risk-calibration
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Task Abstention for Large Language Models in Code Generation

## Summary
CodeRefuser decides when a code LLM should refuse a code-generation prompt because the prompt is likely to lead to wrong code. It clusters generated programs by their execution outputs and calibrates a refusal rule with Learn Then Test.

## Problem
- Code LLMs can produce plausible code that fails functional tests, which makes automated code generation risky in developer tools.
- The paper targets task-level abstention: deciding that a prompt is too likely to fail before returning code, even after multiple samples.
- The abstention criterion uses H@k, the probability that all k sampled solutions are incorrect; the default setting is k=3 with risk tolerance α=0.2.

## Approach
- During calibration, CodeRefuser samples code for prompts with oracle tests, runs the code, estimates H@k, and chooses thresholds that keep admission risk below α with confidence 1-δ.
- At test time, it asks the LLM to generate both code samples and test cases, then runs the samples on the generated tests.
- It clusters code samples that produce the same outputs on the tests, so syntax differences do not split equivalent solutions.
- It uses two scoring modes: Cluster Ratio (CR), which requires a large enough execution-consistent cluster, and Semantic Entropy (SE), which refuses when cluster diversity is too high.
- Sample-Test Dual Filtering (STDF) removes generated tests with high error rates or high output diversity, reducing noise from invalid tests.

## Results
- On HumanEval and MBPP with DeepSeek-Coder-33B, Qwen2.5-Coder-32B, CodeLlama-7B, and WizardCoder-33B, the paper reports a 26.5 percentage point average precision gain over the best existing competitor.
- On HumanEval, CR+STDF reaches precision/F1 of 72.00/69.92 for DeepSeek-Coder, 73.33/53.85 for Qwen2.5-Coder, 91.67/91.70 for CodeLlama, and 61.40/66.14 for WizardCoder.
- On MBPP, SE+STDF reaches 72.65/72.88 for DeepSeek-Coder, while CR+STDF reaches 48.94/47.44 for Qwen2.5-Coder, 79.40/79.69 for CodeLlama, and 69.23/63.07 for WizardCoder.
- With calibration on MBPP and testing on HumanEval, CR+STDF still reaches 91.51 precision and 91.23 F1 for CodeLlama, showing cross-dataset transfer in the reported setup.
- Static baselines with 256 samples do not catch up to CodeRefuser with 64 samples: on HumanEval, CodeRefuser gets 72.00/69.92 for DeepSeek-Coder versus PPL at 37.02/54.36 and CLM at 36.41/53.39.

## Link
- [https://arxiv.org/abs/2605.17029v1](https://arxiv.org/abs/2605.17029v1)
