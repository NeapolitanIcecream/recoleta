---
source: arxiv
url: http://arxiv.org/abs/2603.06739v1
published_at: '2026-03-06T08:29:08'
authors:
- Yubang Wang
- Chenxi Zhang
- Bowen Chen
- Zezheng Huai
- Zihao Dai
- Xinchi Chen
- Yuxin Wang
- Yining Zheng
- Jingjing Gong
- Xipeng Qiu
topics:
- benchmarking
- research-code-execution
- environment-synthesis
- runtime-verification
- llm-agents
relevance_score: 0.08
run_id: materialize-outputs
---

# ResearchEnvBench: Benchmarking Agents on Environment Synthesis for Research Code Execution

## Summary
ResearchEnvBench 是一个面向科研代码执行环境自动搭建的基准，专门评测智能体能否把原始研究仓库真正配置到“可运行”而不只是“看起来装好了”。论文显示，当前最强代理在复杂 AI/HPC 仓库上距离可复现实验仍有明显差距。

## Problem
- 现有代码/科研代理评测通常假设执行环境已预先配置好，忽略了现实中最难的前置步骤：依赖安装、CUDA/驱动对齐、分布式训练配置。
- 仅靠静态检查、缺失 import、或 Docker build 成功，无法证明科研仓库真的能在 CPU/GPU 上运行，因此会高估代理能力。
- 这很重要，因为如果代理不能自主搭好研究环境，它后续的改代码、跑实验、做科研结论都难以被真实验证和复现。

## Approach
- 提出 **ResearchEnvBench**：收集 **44 个** 2024 年后发布的高复杂度研究仓库，聚焦 AI/HPC、GPU 依赖、自定义 CUDA kernel、分布式训练等真实难题。
- 任务形式很直接：给代理一个原始仓库、文档和目标执行设置，代理通过 shell、读文件、编辑辅助脚本来搭建环境，但**不能修改已跟踪源码**。
- 设计 **Pyramid of Runtime Verification** 分层验证：从静态依赖完整性 **C0**，到 CPU 运行 **C1**、CUDA 对齐 **C2**、单 GPU 计算 **C3**、多 GPU DDP **C4**，逐层变难。
- 增加 **C5 幻觉指标**：比较代理自报“成功/可用”与隐藏探针的真实结果，衡量路径、版本和能力声明是否虚报。
- 在统一沙箱中评测 4 类 SOTA 代理，环境为 Ubuntu 22.04、**2× RTX 4090**、CUDA **12.4** 驱动，且不预装深度学习框架。

## Results
- 基准规模与覆盖：共 **44** 个仓库，语言为 **Python/C++**；其中 **43/44** 支持至少单 GPU 执行，部分支持多 GPU DDP，覆盖 8 类现代 ML 研究代码。
- **最佳 CPU 执行率 C1** 来自 Codex：**17/29 = 58.6%**；Claude(GLM-4.7) 与 NexAU 为 **16/29 = 55.2%**；Claude(Sonnet 4.5) 为 **15/29 = 51.7%**。
- **最佳 CUDA 对齐 C2** 为 Claude(Sonnet 4.5) 与 NexAU：**41/44 = 93.2%**；Claude(GLM-4.7) 为 **40/44 = 90.9%**；Codex 为 **35/44 = 79.5%**。
- **最佳单 GPU 真实计算 C3** 为 Claude(GLM-4.7) 与 NexAU：**21/43 = 48.8%**；Codex 为 **19/43 = 44.2%**；Sonnet 4.5 为 **18/43 = 41.9%**。说明“GPU 可见”不等于“仓库可跑”。
- **最佳多 GPU DDP C4** 仅为 **12/32 = 37.5%**，由两种 Claude 设定取得；Codex 与 NexAU 都是 **11/32 = 34.4%**。这是论文强调的关键突破性发现：当前 SOTA 在真实研究环境复现上成功率仍很低。
- 静态检查与真实运行脱节：Codex 的缺失 import 比例最低，**675/2858 = 23.6%**，但其 **C2 仅 79.5%**，落后于 Claude/NexAU 的 **90.9%–93.2%**，表明“依赖看起来齐了”并不代表 CUDA/ABI 真正确。
- 幻觉方面，Codex 总幻觉数最低，仅 **4**；Claude(GLM-4.7) 为 **18**，Claude(Sonnet 4.5) 为 **20**，NexAU 为 **16**，且大多数是**能力幻觉**（如 17/18、20/20、14/16），说明不少代理会把“安装成功”误判成“已经可运行”。

## Link
- [http://arxiv.org/abs/2603.06739v1](http://arxiv.org/abs/2603.06739v1)
