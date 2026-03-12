---
source: hn
url: https://unsloth.ai/docs/models/qwen3.5
published_at: '2026-03-07T23:32:17'
authors:
- Curiositry
topics:
- local-llm
- model-quantization
- llama-cpp
- qwen
- tool-calling
- agentic-coding
relevance_score: 0.86
run_id: materialize-outputs
---

# How to run Qwen 3.5 locally

## Summary
这是一份面向工程实践的本地部署指南，介绍如何在 llama.cpp、LM Studio 和 llama-server 上运行 Qwen3.5 全系列模型，并结合 Unsloth 动态量化降低本地推理门槛。
它不是标准学术论文，更像产品/系统说明文档，重点在可运行性、量化配置、推理模式切换和资源需求。

## Problem
- 解决的问题是：**如何在本地设备上高效运行从 0.8B 到 397B 的 Qwen3.5 模型**，同时尽量降低内存占用并保留推理、编码、长上下文和工具调用能力。
- 这很重要，因为大模型通常对显存/内存要求极高；若能通过量化和后端适配在本地运行，就能支持离线使用、更低成本部署、私有数据处理和本地 agent/coding 工作流。
- 文中还隐含解决了一个工程问题：不同“thinking / non-thinking”模式、工具调用模板、量化格式和推理后端之间容易配置错误，影响真实可用性。

## Approach
- 核心方法是**使用 Unsloth Dynamic 2.0 动态量化 GGUF**，把 4-bit 等低比特量化与关键层升到 8/16-bit 结合，在尽量小的模型体积下维持性能。
- 运行机制很简单：先下载对应 Qwen3.5 变体的 GGUF 量化文件，再用 **llama.cpp / llama-server / LM Studio** 加载，并按任务切换“thinking”或“non-thinking”模式。
- 文档为不同尺寸模型给出本地硬件建议、上下文长度、采样参数和命令行设置；对于小模型，默认关闭 reasoning，需要显式开启 `enable_thinking=true`。
- 对超大模型 397B，方法上依赖**MoE offloading + 量化**，使其可以在单 24GB GPU 加大系统内存的环境中运行，而不是要求纯高端多卡集群。
- 还修复了**tool-calling chat template bug** 并更新 `imatrix` 数据与量化算法，以改善聊天、编码、长上下文和工具调用效果。

## Results
- 文中声称 Qwen3.5 支持 **256K context**，并可通过 **YaRN 扩展到 1M**；覆盖 **201 languages**。
- 本地资源门槛方面：**27B 可在约 18GB RAM/Mac** 上运行，**35B-A3B 可在约 22–24GB** 设备上运行，**9B 近全精度约需 12GB RAM/VRAM**，**122B-A10B 约需 70GB**。
- 对 **397B-A17B**：完整检查点约 **807GB**；**3-bit** 量化可放入 **192GB RAM**，**4-bit** 可放入 **256GB RAM**；其 **UD-Q4_K_XL** 约 **214GB** 磁盘占用，可直接在 **256GB M3 Ultra** 上加载；通过 **单张 24GB GPU + 256GB 系统内存** 的 MoE offloading，报告可达到 **25+ tokens/s**。
- 第三方 750-prompt 混合评测（**LiveCodeBench v6, MMLU Pro, GPQA, Math500**）中，**Qwen3.5-397B-A17B 原始权重 81.3%**；**UD-Q4_K_XL 80.5%**（**-0.8 点**，**+4.3% relative error increase**）；**UD-Q3_K_XL 80.7%**（**-0.6 点**，**+3.5% relative error increase**）。文中据此强调量化后与原始模型性能差距 **低于 1 个百分点**。
- 对 35B 系列，文中称更新后的量化在 **150+ KL Divergence benchmarks**、总计 **9TB GGUFs** 上表现为 **SOTA on Pareto Frontier**，并特别提到 **UD-Q4_K_XL、IQ3_XXS** 等结果，但未在摘录中给出更完整的逐项基准数值。
- 其他结果多为定性主张：改进后的量化算法、`imatrix` 数据和模板修复可提升 **chat、coding、long context、tool-calling** 场景表现；但除上述基准外，摘录未提供更多可核验的详细数字。

## Link
- [https://unsloth.ai/docs/models/qwen3.5](https://unsloth.ai/docs/models/qwen3.5)
