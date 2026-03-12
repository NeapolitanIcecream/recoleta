---
source: arxiv
url: http://arxiv.org/abs/2603.04356v1
published_at: '2026-03-04T18:20:03'
authors:
- Soroush Nasiriany
- Sepehr Nasiriany
- Abhiram Maddukuri
- Yuke Zhu
topics:
- robot-benchmark
- simulation-framework
- generalist-robot-policy
- robot-foundation-model
- lifelong-learning
- mobile-manipulation
relevance_score: 0.97
run_id: materialize-outputs
---

# RoboCasa365: A Large-Scale Simulation Framework for Training and Benchmarking Generalist Robots

## Summary
RoboCasa365 是一个面向通用机器人训练与评测的大规模家庭移动操作仿真基准，重点解决“缺少可复现、系统化、大规模 benchmark”的问题。它把任务、场景与演示数据同时扩展到较大规模，并用此分析多任务训练、机器人基础模型训练和终身学习中的关键影响因素。

## Problem
- 现有机器人学习很难可靠衡量“离通用家庭机器人还有多远”，因为缺少**可复现、系统化、足够大规模**的评测基准。
- 真实世界数据收集和评测成本高、噪声大，难以系统研究**任务多样性、环境变化、数据规模**对泛化的影响。
- 现有仿真框架通常任务少、场景窄、数据规模有限，难以支撑**generalist robot policy / robot foundation model** 的训练与公平比较。

## Approach
- 构建 RoboCasa365：基于 RoboCasa 扩展为 **365 个日常任务**、**2,500 个厨房场景**、**2,000+ 小时**机器人交互数据的仿真框架。
- 任务层面包含 **65 个原子任务**和 **300 个组合任务**；组合任务通过 LLM 先生成高层活动和任务蓝图，再人工实现到模拟器中。
- 场景层面使用 **50 个真实住宅厨房布局 × 50 种风格 = 2,500 个预训练场景**，并与 **10 个目标场景**分离，用于更严格的泛化评测。
- 数据层面提供 **30k 预训练人工演示**、**25k 目标任务人工演示**，并用 MimicGen 在 **60 个原子任务**上从每任务 **100 条种子演示扩展到 10k 条**，形成 **1615 小时**合成数据。
- 基准评测覆盖三类设置：**大规模多任务训练、基础模型预训练+微调、终身学习**，并比较 Diffusion Policy、pi_0、pi_0.5、GR00T N1.5 等方法。

## Results
- **基准规模声明**：365 个任务、2,500 个厨房场景、**612 小时人工演示 + 1615 小时合成演示**；论文称其是首个同时满足“数百任务、数千场景、大规模高质量数据、系统 benchmark”的仿真框架之一。
- **多任务训练（300 个预训练任务，50 个目标任务评测）**：GR00T N1.5 平均成功率 **20.0%**，优于 pi_0.5 **16.9%**、pi_0 **15.0%**、Diffusion Policy **6.1%**。按任务类型，GR00T 在 Atomic / Composite-Seen / Composite-Unseen 上分别为 **43.0 / 9.6 / 4.4**，显示长时序组合任务和未见任务明显更难。
- **基础模型训练收益**：在 50 个目标任务上，GR00T 的“仅目标数据训练”平均成功率从 **21.0% / 34.3% / 43.7%**（10%/30%/100%目标数据）提升到“预训练+目标微调”的 **35.9% / 42.2% / 51.1%**。论文明确声称预训练带来约 **3× 数据效率提升**。
- **未见组合任务收益最明显**：Composite-Unseen 上，100% 目标数据时“仅目标训练”为 **33.3%**，而“预训练+微调”为 **42.1%**；10% 数据时分别为 **11.2% vs 22.7%**。
- **原子任务零/低样本迁移较强，组合任务弱**：仅预训练时 Atomic 达 **41.9%**，但 Composite-Seen / Unseen 仅 **0.0% / 0.2%**，说明预训练知识对短时技能更易迁移，对长时序规划仍不足。
- **终身学习存在明显灾难性遗忘**：四阶段训练中，Atomic 成功率从 Phase 1 的 **41.5%** 降到 Phase 4 的 **10.6%**；2-3 stage 任务从 **24.5%** 降到 **1.7%**，表明随着学习更长时序新任务，旧任务性能持续下降。

## Link
- [http://arxiv.org/abs/2603.04356v1](http://arxiv.org/abs/2603.04356v1)
