---
source: arxiv
url: http://arxiv.org/abs/2604.17016v1
published_at: '2026-04-18T14:55:11'
authors:
- Zhipeng Wang
- Boyang Yang
- Yidong Wan
- Liuye Guo
- You Lv
- Tao Zheng
- Zhuowei Wang
- Tieke He
topics:
- automatic-program-repair
- cross-lingual-transfer
- code-llms
- low-resource-languages
- software-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# HELO-APR: Enhancing Low-Resource Program Repair through Cross-Lingual Knowledge Transfer

## Summary
HELO-APR improves automatic program repair for low-resource languages by transferring repair knowledge from a high-resource language through verified cross-lingual data and staged fine-tuning. The paper targets Ruby and Rust repair using C++ as the source language and reports large gains over strong baselines.

## Problem
- LLM-based program repair works much better for high-resource languages such as C++ than for low-resource languages such as Ruby and Rust because verified buggy-fixed training pairs are scarce.
- Direct transfer from a high-resource language causes syntax interference: a model trained only on C++ can emit C++-style patches for Ruby, which do not compile.
- Naive synthetic data pipelines can create low-quality bugs or miss whether a defect can even exist in the target language.

## Approach
- HELO-APR has two parts: build verified low-resource buggy-fixed pairs from high-resource pairs, then train with a three-stage curriculum.
- During data construction, it filters out non-transferable defects, translates fixed C++ code into the target language while preserving the code structure needed to recreate the bug, and verifies the translated code with generated tests that must reach at least 90% line and branch coverage.
- It then injects target-language bugs guided by the original defect type, root cause, and patch, and picks candidates that best match the original bug behavior on bug-triggering inputs while avoiding extra regressions.
- During training, the model first learns repair on C++, then learns cross-lingual alignment using parallel C++/target-language buggy-fixed pairs, then adapts to direct repair in the target language. The backbone model is frozen and only repair adapters are tuned.

## Results
- On xCodeEval, HELO-APR raises Pass@1 on DeepSeek-Coder-6.7B from 31.32% to 48.65%, a relative gain of 55.33% over the zero-shot baseline.
- On xCodeEval, HELO-APR raises Pass@1 on CodeLlama-7B from 1.67% to 11.97%, more than 7 times the zero-shot baseline.
- For syntactic validity, the average target compilation rate on CodeLlama improves from 49.77% to 91.98%.
- On Defects4Ruby, HELO-APR improves BLEU-4 from 61.20 to 66.79 and ROUGE-1 from 76.76 to 83.59 on CodeLlama-7B.
- The paper also reports ablation studies for both dataset construction and curriculum stages, with the stated claim that each core component is necessary, but the excerpt does not provide the ablation numbers.
- Training data uses 10,000 C++ buggy-fixed pairs from xCodeEval to synthesize target-language repair data for Ruby and Rust.

## Link
- [http://arxiv.org/abs/2604.17016v1](http://arxiv.org/abs/2604.17016v1)
