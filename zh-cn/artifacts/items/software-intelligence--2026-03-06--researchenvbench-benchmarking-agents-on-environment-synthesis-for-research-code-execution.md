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
- llm-agents
- environment-synthesis
- research-code-execution
- runtime-verification
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# ResearchEnvBench: Benchmarking Agents on Environment Synthesis for Research Code Execution

## Summary
ResearchEnvBench提出了一个面向科研代码执行环境自动构建的基准，专门评测智能体能否把原始研究仓库变成真正可运行的AI/HPC实验环境。论文显示，现有SOTA智能体在“看起来装好了”与“实际能在GPU/多GPU上跑起来”之间仍有明显差距。

## Problem
- 现有代码修复或自动科研基准通常假设执行环境已预先配置好，忽略了真实科研中最难的前置步骤：依赖解析、CUDA/驱动对齐、分布式配置与自定义编译。
- 仅靠静态检查、构建成功或缺失导入统计，无法验证研究代码是否真的能在CPU/GPU/多GPU上执行，因此难以衡量智能体的可复现科研能力。
- 这个问题重要，因为如果智能体不能独立搭建可运行环境，那么后续代码修改、实验设计和结果复现都很难在真实科研流程中落地。

## Approach
- 构建**ResearchEnvBench**：收集并人工筛选44个2024年后发布的高复杂度AI研究仓库，覆盖Py/C++、GPU依赖、自定义CUDA核、分布式训练等真实研究负载。
- 将任务定义为环境合成：给定研究仓库、文档和目标执行设置，智能体通过shell执行、读文件和编辑辅助文件，在不修改受跟踪源码的前提下把裸环境变成可运行环境。
- 提出**运行时验证金字塔**，分层评测从静态依赖完整性到真实运行能力：$C_0$ 缺失导入、$C_1$ CPU执行、$C_2$ CUDA对齐、$C_3$ 单GPU计算、$C_4$ 多GPU DDP就绪。
- 引入**能力幻觉**指标$C_5$，衡量智能体自报成功与隐藏探针真实结果之间的偏差，细分为路径、版本和能力三类幻觉。
- 在统一Docker沙箱中评测4类SOTA智能体，使用相同工具接口和预算，比较它们在各阶段成功率与自报告可靠性上的差异。

## Results
- 数据集包含**44个**高复杂度研究仓库；其中**43/44**支持至少单GPU执行，覆盖8类现代ML研究代码，是一个硬件感知的研究环境基准。
- 最佳**CPU执行成功率 $C_1$** 来自Codex：**17/29 = 58.6%**；Claude(GLM-4.7)与NexAU均为 **16/29 = 55.2%**，Claude(Sonnet 4.5)为 **15/29 = 51.7%**。
- 最佳**CUDA对齐成功率 $C_2$** 为Claude(Sonnet 4.5)和NexAU：**41/44 = 93.2%**；Claude(GLM-4.7)为 **40/44 = 90.9%**；Codex仅 **35/44 = 79.5%**。说明静态依赖闭合不等于硬件可用。
- 最佳**单GPU执行 $C_3$** 为Claude(GLM-4.7)和NexAU：**21/43 = 48.8%**；Codex为 **19/43 = 44.2%**；Claude(Sonnet 4.5)为 **18/43 = 41.9%**。从$C_2$到$C_3$的明显下跌揭示“GPU可见”不代表研究入口点可运行。
- 最佳**多GPU DDP成功率 $C_4$** 为两种Claude配置：**12/32 = 37.5%**；Codex和NexAU均为 **11/32 = 34.4%**。论文强调当前最佳多GPU验证成功率也只有**37.5%**。
- **静态缺失导入 $C_0$** 上，Codex最好，为 **675/2858 = 23.6%**，优于Claude(GLM-4.7) **26.6%**、Claude(Sonnet 4.5) **25.5%**、NexAU **25.3%**；但它并未带来最佳GPU就绪能力。
- **幻觉 $C_5$** 差异显著：Codex总幻觉仅 **4**，Claude(GLM-4.7) **18**，Claude(Sonnet 4.5) **20**，NexAU **16**；多数错误是能力幻觉（如Claude Sonnet 4.5为 **20/20**）。这表明更保守的自报告可显著降低“声称成功但实际失败”的假阳性。

## Link
- [http://arxiv.org/abs/2603.06739v1](http://arxiv.org/abs/2603.06739v1)
