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
language_code: zh-CN
---

# How to run Qwen 3.5 locally

## Summary
这不是一篇学术论文，而是一份关于 **Qwen3.5** 本地部署的实用指南，重点介绍不同参数规模模型如何在本地设备上通过量化与 llama.cpp / LM Studio 运行。其核心价值在于降低大模型本地推理门槛，并给出内存、上下文、推理模式与量化选择建议。

## Problem
- 解决的问题是：**如何让不同规模的 Qwen3.5 模型在本地硬件上可运行、可配置，并尽量保留性能**。
- 这很重要，因为超大模型通常受限于 **显存/内存、推理速度、量化误差、部署工具兼容性**，普通开发者难以直接本地使用。
- 文中还试图回答实际部署中的关键问题：**需要多少内存、如何切换 thinking / non-thinking、应选择哪种量化格式与运行后端**。

## Approach
- 核心方法很简单：**把原始大模型转换/提供为多种 GGUF 量化版本**，再用 **llama.cpp、llama-server 或 LM Studio** 在本地运行。
- 使用 **Unsloth Dynamic 2.0** 量化方案，在 4-bit 量化时把重要层提升到 8-bit 或 16-bit，以在更低内存占用下尽量保住精度。
- 对不同模型规模给出明确的 **硬件门槛与推荐配置**，例如 27B、35B、122B、397B 以及 0.8B/2B/4B/9B 小模型的内存需求与上下文设置。
- 通过 **thinking / non-thinking 模式切换** 和不同采样参数，适配通用任务、精确编码、推理任务等不同场景。
- 对超大 MoE 模型（如 397B-A17B），进一步结合 **量化 + MoE offloading**，使其能够在高内存本地机器甚至单张 24GB GPU 配合系统内存的环境中运行。

## Results
- 文中声称 **Qwen3.5 支持 256K context**，并可通过 **YaRN 扩展到 1M**；同时支持 **201 languages**。
- 对本地运行门槛的具体数字包括：**27B 可在约 18GB RAM/Mac 设备上用 Dynamic 4-bit 运行**，**35B-A3B 可在约 22GB 设备上运行**，**9B 近全精度需要约 12GB RAM/VRAM/统一内存**，**122B-A10B 约需 70GB RAM**。
- 对 397B-A17B，给出的部署数字包括：**完整 checkpoint 约 807GB 磁盘占用**；**3-bit 可装入 192GB RAM**，**4-bit(MXFP4) 可装入 256GB RAM**，其中 **UD-Q4_K_XL 磁盘占用约 214GB**；**8-bit 约需 512GB RAM/VRAM**。
- 397B-A17B 在推理性能上宣称：**单张 24GB GPU + 256GB 系统内存，通过 MoE offloading 可达 25+ tokens/s**。
- 第三方 750-prompt 混合基准（**LiveCodeBench v6, MMLU Pro, GPQA, Math500**）上，**原始权重 81.3%**；**UD-Q4_K_XL 为 80.5%（-0.8 点，+4.3% relative error increase）**；**UD-Q3_K_XL 为 80.7%（-0.6 点，+3.5% relative error increase）**，表明量化后与原始模型精度差距 **低于 1 个百分点**。
- 文中还宣称对 **Qwen3.5-35B** 做了 **150+ KL Divergence benchmarks**、总计 **9TB GGUFs** 的量化评测，并称 **UD-Q4_K_XL、IQ3_XXS 等在 99.9% KL Divergence 指标下处于 SOTA Pareto Frontier**；但这里未给出完整对比表格与统一学术实验设置。
- 若按学术“突破”标准来看，本文没有提出新的基础模型或训练算法；最强的具体贡献是：**展示了大规模 Qwen3.5 模型在本地以量化形式可运行，并给出较完整的部署/量化性能数字**。

## Link
- [https://unsloth.ai/docs/models/qwen3.5](https://unsloth.ai/docs/models/qwen3.5)
