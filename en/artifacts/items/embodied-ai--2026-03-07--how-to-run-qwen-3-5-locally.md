---
source: hn
url: https://unsloth.ai/docs/models/qwen3.5
published_at: '2026-03-07T23:32:17'
authors:
- Curiositry
topics:
- llm-deployment
- local-inference
- quantization
- gguf
- llama-cpp
relevance_score: 0.05
run_id: materialize-outputs
language_code: en
---

# How to run Qwen 3.5 locally

## Summary
This is not an academic paper, but a practical guide for local deployment of **Qwen3.5**, focusing on how models of different parameter scales can run on local devices through quantization and llama.cpp / LM Studio. Its core value is lowering the barrier to local inference for large models, while providing recommendations on memory, context, reasoning modes, and quantization choices.

## Problem
- The problem it addresses is: **how to make Qwen3.5 models of different sizes runnable and configurable on local hardware, while preserving as much performance as possible**.
- This matters because very large models are typically constrained by **VRAM/memory, inference speed, quantization error, and deployment tool compatibility**, making them difficult for ordinary developers to use locally.
- The article also tries to answer key practical deployment questions: **how much memory is needed, how to switch between thinking / non-thinking, and which quantization format and runtime backend to choose**.

## Approach
- The core method is straightforward: **convert or provide the original large models in multiple GGUF quantized versions**, then run them locally with **llama.cpp, llama-server, or LM Studio**.
- It uses the **Unsloth Dynamic 2.0** quantization scheme, which upcasts important layers to 8-bit or 16-bit during 4-bit quantization in order to preserve accuracy as much as possible under lower memory usage.
- It provides clear **hardware thresholds and recommended configurations** for different model sizes, such as the memory requirements and context settings for 27B, 35B, 122B, 397B, and the smaller 0.8B/2B/4B/9B models.
- Through **thinking / non-thinking mode switching** and different sampling parameters, it adapts to scenarios such as general tasks, precise coding, and reasoning tasks.
- For ultra-large MoE models (such as 397B-A17B), it further combines **quantization + MoE offloading**, enabling them to run on high-memory local machines or even in setups with a single 24GB GPU plus system memory.

## Results
- The article claims that **Qwen3.5 supports 256K context** and can be extended to **1M via YaRN**; it also supports **201 languages**.
- Specific figures for local deployment thresholds include: **27B can run with Dynamic 4-bit on a device with about 18GB RAM/Mac memory**, **35B-A3B can run on a device with about 22GB**, **9B at near-full precision requires about 12GB RAM/VRAM/unified memory**, and **122B-A10B requires about 70GB RAM**.
- For 397B-A17B, the deployment figures given include: **the full checkpoint occupies about 807GB of disk space**; **3-bit can fit into 192GB RAM**, **4-bit (MXFP4) can fit into 256GB RAM**, of which **UD-Q4_K_XL uses about 214GB of disk space**; **8-bit requires about 512GB RAM/VRAM**.
- For inference performance, 397B-A17B is claimed to achieve: **25+ tokens/s via MoE offloading with a single 24GB GPU + 256GB system memory**.
- On a third-party 750-prompt mixed benchmark (**LiveCodeBench v6, MMLU Pro, GPQA, Math500**), **the original weights score 81.3%**; **UD-Q4_K_XL scores 80.5% (-0.8 points, +4.3% relative error increase)**; **UD-Q3_K_XL scores 80.7% (-0.6 points, +3.5% relative error increase)**, indicating that the accuracy gap after quantization is **less than 1 percentage point**.
- The article also claims it conducted **150+ KL Divergence benchmarks** on **Qwen3.5-35B**, totaling quantization evaluations across **9TB GGUFs**, and states that **UD-Q4_K_XL, IQ3_XXS, and others lie on the SOTA Pareto Frontier under the 99.9% KL Divergence metric**; however, it does not provide a complete comparison table or a unified academic experimental setup.
- By academic “breakthrough” standards, this article does not propose a new foundation model or training algorithm; its strongest concrete contribution is: **demonstrating that large-scale Qwen3.5 models can run locally in quantized form, and providing relatively complete deployment and quantization performance figures**.

## Link
- [https://unsloth.ai/docs/models/qwen3.5](https://unsloth.ai/docs/models/qwen3.5)
