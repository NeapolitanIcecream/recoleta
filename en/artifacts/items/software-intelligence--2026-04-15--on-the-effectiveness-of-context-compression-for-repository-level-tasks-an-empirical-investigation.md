---
source: arxiv
url: http://arxiv.org/abs/2604.13725v1
published_at: '2026-04-15T11:00:17'
authors:
- Jia Feng
- Zhanyue Qin
- Cuiyun Gao
- Ruiqi Wang
- Chaozheng Wang
- Yingwei Ma
- Xiaoyuan Xie
topics:
- repository-level-code
- context-compression
- code-intelligence
- long-context-llms
- code-generation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# On the Effectiveness of Context Compression for Repository-Level Tasks: An Empirical Investigation

## Summary
This paper studies whether compressing long repository context helps or hurts repository-level code tasks. It finds that compression can cut cost and, with learned latent-vector methods, can beat full-context inference on some code benchmarks.

## Problem
- Repository-level code completion and generation need long multi-file context, which raises latency and memory cost as input length grows.
- Long prompts also hide useful evidence inside irrelevant repository text and can exceed the model context window, forcing truncation.
- Prior context compression work focused on natural language. Its value for code, where cross-file dependencies and syntax matter more, was unclear.

## Approach
- The paper runs a unified empirical comparison of **8 compression methods** across **3 paradigms**: text-to-text (shorter token sequences), text-to-vector (learned latent memory tokens), and text-to-image (render code as images for a VLM).
- It evaluates two repository-level tasks on **ComplexCodeEval**: code completion and code generation, using **100 Python + 100 Java** held-out samples.
- Models come from the **Qwen2.5** family: **Qwen2.5-Coder 3B/7B** for text-based methods and **Qwen2.5-VL 3B/7B** for visual compression.
- For text-to-vector, the context is split into segments and compressed into a small set of learned memory tokens, with variants that either keep segments separate or pass memory across segments.
- The study measures both task quality and deployment cost, comparing compressed inference against **full-context** and **no-context** baselines over multiple compression ratios.

## Results
- Main claim: at **4x compression**, **text-to-vector** methods can outperform full-context inference by up to **28.3% BLEU** on Python completion. In the table, **QC-7B T2V-SS** reaches **41.34 BLEU** on Python completion versus **32.21** for full context, a gain of about **28.3%**.
- On **QC-7B**, text-to-vector also improves other completion scores over full context in several settings: Python completion **EM 42-44 vs 33**, Java completion **BLEU up to 35.12 vs 32.60**, and Java completion **ES up to 60.29 vs 55.90**.
- On code generation, text-to-vector often beats full context on Python with **QC-3B** and **QC-7B**. Examples: **QC-7B T2V-QS** gets **13.58 BLEU** vs **10.49** full context on Python generation; **QC-3B T2V-QC** gets **12.43 BLEU** vs **10.27**.
- **Text-to-image** stays close to full context on completion at moderate compression but drops on generation. Example: **QV-7B** Python completion is **24.11 BLEU** at **4x** vs **24.91** full context, while Python generation falls to **4.52** vs **9.19**.
- **Text-to-text** is useful at mild compression but usually underperforms full context and degrades faster on generation. Example: **QC-7B T2T-LL2** Python completion is **30.32 BLEU** vs **32.21** full context; Python generation is **7.54** vs **10.49**.
- Efficiency claims: all three paradigms lower inference cost versus full-context decoding. The paper reports up to **50% end-to-end latency reduction** at high compression ratios, **33% latency reduction** for text-to-image at its best **4x** setting, and **over 35%** total latency reduction for text-to-text at moderate ratios.

## Link
- [http://arxiv.org/abs/2604.13725v1](http://arxiv.org/abs/2604.13725v1)
