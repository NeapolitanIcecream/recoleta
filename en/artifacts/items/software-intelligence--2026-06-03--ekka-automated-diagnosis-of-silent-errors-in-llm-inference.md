---
source: arxiv
url: https://arxiv.org/abs/2606.04594v1
published_at: '2026-06-03T08:32:13'
authors:
- Yile Gu
- Zhen Zhang
- Shaowei Zhu
- Xinwei Fu
- Jun Wu
- Yida Wang
- Baris Kasikci
topics:
- llm-inference
- silent-errors
- debugging
- code-intelligence
- llm-agents
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Ekka: Automated Diagnosis of Silent Errors in LLM Inference

## Summary
Ekka diagnoses silent accuracy and output errors in LLM serving systems by comparing a buggy engine with a correct reference implementation at intermediate model states. It turns manual tensor inspection into an automated agent workflow that ranks the likely faulty component.

## Problem
- Silent errors in systems such as vLLM and SGLang can return plausible text while accuracy drops or outputs become wrong, with no runtime error or warning.
- The paper cites a vLLM Gemma 3 issue where Hellaswag accuracy dropped by nearly 30%, and developers spent months tracing it to sliding-window attention misuse.
- Root causes can sit in model code, kernel backends, numerical precision, or serving logic, so output-only checks give little help in finding the failing component.

## Approach
- Ekka runs the buggy target system and a reference implementation, such as HuggingFace Transformers, on the same model, prompts, and settings.
- It collects intermediate activations and call sequences while reproducing the bug.
- It builds model trees for both implementations, then maps semantically matching components even when one side fuses modules, such as QKV projection.
- It generates code to align activations across shape, data type, and memory-layout differences.
- It computes an error ratio that filters small numerical differences, then applies change-point analysis to find where the target and reference first diverge sharply.

## Results
- On a benchmark of real silent errors, Ekka reports 80% pass@1 diagnosis accuracy and 88% pass@5 diagnosis accuracy.
- The benchmark study collected 90 silent errors: 48 from vLLM and 42 from SGLang; 70 closed issues were used for analysis.
- In the 70 closed issues, accuracy regression was the largest symptom class at 43.8%.
- Root-cause shares were 30.6% framework implementation, 25.5% model implementation, 24.5% kernel backend, and 19.4% numerical precision.
- Ekka diagnosed 17 issues from vLLM and SGLang, with a reported 24% to 34% accuracy gain over state-of-the-art systems and about $30 average cost per case.
- It also diagnosed 4 new silent errors in vLLM and SGLang, and the developers confirmed all 4.

## Link
- [https://arxiv.org/abs/2606.04594v1](https://arxiv.org/abs/2606.04594v1)
