---
source: arxiv
url: https://arxiv.org/abs/2604.25903v1
published_at: '2026-04-28T17:48:16'
authors:
- Ajmain Inqiad Alam
- Palash Roy
- Chanchal K. Roy
- Banani Roy
- Kevin A. Schneider
topics:
- llm-compression
- code-intelligence
- green-ai
- model-distillation
- software-engineering
- quantization
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Carbon-Taxed Transformers: A Green Compression Pipeline for Overgrown Language Models

## Summary
Carbon-Taxed Transformers is a compression pipeline for code-focused language models that cuts inference memory, latency, and CO2 cost while keeping most task performance. It targets clone detection, code summarization, and code generation across encoder-only, encoder-decoder, and decoder-only Transformers.

## Problem
- Large language models used in software engineering are costly to run, slow to deploy, memory-heavy, and energy-intensive during inference.
- The paper treats inference efficiency and CO2 emissions as design constraints because deployed inference can dominate total ML compute and energy use.
- Prior compression work often applies one method to one model or task, leaving less evidence for ordered multi-step compression across software engineering workloads.

## Approach
- CTT first uses neural architecture search to find a smaller student architecture under hard latency and memory limits.
- It then applies structured pruning to layers, attention heads, hidden size, and feedforward size, keeping reductions only when validation loss stays acceptable.
- It quantizes the pruned model before training so the student learns under low-precision numerical constraints.
- It trains the quantized student with knowledge distillation, matching teacher outputs instead of relying only on hard labels.
- The tested tasks cover three Transformer types: UniXCoder-style encoder-only clone detection, encoder-decoder code summarization, and decoder-only code generation.

## Results
- CTT reports up to 49× memory reduction across evaluated software engineering models.
- Inference latency drops by 8-10× for clone detection, up to 3× for summarization, and 4-7× for generation.
- Reported inference CO2 emissions fall by up to 81%.
- Performance retention is reported at about 98% accuracy for clone detection, about 89% for summarization, and up to 91% on textual generation metrics.
- For code generation pass@1, the compressed models retain up to 68% performance.
- Two ablation studies claim that both the NAS→pruning→quantization→distillation order and the individual compression components are needed for the reported gains.

## Link
- [https://arxiv.org/abs/2604.25903v1](https://arxiv.org/abs/2604.25903v1)
