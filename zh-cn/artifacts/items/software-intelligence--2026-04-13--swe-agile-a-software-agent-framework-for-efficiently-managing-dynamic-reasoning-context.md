---
source: arxiv
url: http://arxiv.org/abs/2604.11716v1
published_at: '2026-04-13T16:52:34'
authors:
- Shuquan Lian
- Juncheng Liu
- Yazhe Chen
- Yuhong Chen
- Hui Li
topics:
- software-agents
- code-intelligence
- swe-bench
- context-management
- reasoning-compression
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# SWE-AGILE: A Software Agent Framework for Efficiently Managing Dynamic Reasoning Context

## Summary
## 摘要
SWE-AGILE 是一个用于多步代码修复的软件代理框架。它保留最近的详细推理，把更早的推理压缩成简短摘要，并训练模型在这种持续变化的上下文中工作。在 SWE-Bench-Verified 上，它报告了 7B-8B 开源模型中的最佳结果，Qwen3-8B 的成功率达到 24.1%。

## 问题
- 多轮软件工程代理需要较长的推理链来检查代码、使用工具和处理边界情况，但保留全部历史推理会让上下文迅速膨胀。
- 大上下文会因 lost-in-the-middle 效应、更高的内存成本以及更慢的训练和推理而降低代理质量。
- 如果把旧推理完全丢弃，代理就必须在每次工具调用后重新推导同样的分析，这会浪费 token，并削弱步骤之间的连续性。

## 方法
- 代理在每一步输出三部分：详细推理、简短的推理摘要和下一步动作。
- 它使用动态上下文：完整的观察和动作保留在历史中，最近的推理以原文形式保留在滑动窗口内，更早的推理则替换为逐步生成的摘要。
- 训练使用轨迹快照，使每一步都在与推理时相同的可见性限制下学习，而不是在训练时暴露完整的历史思维链。
- 一个 hindsight backfill 流水线会用详细推理和摘要重写成功轨迹，利用真实的后续动作和原始的浅层思考，合成更好的监督信号。
- 带可验证奖励的 RL 增加了轨迹级压缩奖励，因此模型只有在既解决任务又把保留上下文控制得较短时才会得到奖励。

## 结果
- 在 **SWE-Bench-Verified** 上，**SWE-AGILE (SFT+RL)** 配合 **Qwen3-8B** 达到 **24.1%** 的成功率。
- 在同一基准上，**Qwen3-8B base model** 为 **15.83%**，**SWE-AGILE (SFT)** 为 **21.45%**，相对基座模型提升 **35.5%**。
- 论文称，**24.1%** 在其对比表中为 **7B-8B** 这一档设下了新标准，超过 **R2EGym 7B (19.0%)**、**SWE-smith 7B (15.2%)** 和 **SWE-Gym 7B (10.6%)**；也高于 **SkyRL-Agent-v0 14B (21.6%)**。
- 该方法使用了 **2.2k training trajectories**。作者称这相当于 **SWE-Dev** 所用 **19.3k** 轨迹的 **11%**，而 SWE-AGILE 仍以 **24.1%** 的分数略高于 **SWE-Dev 7B (23.4%)**。
- 在 **Qwen3-14B** 且仅用 SFT 的设置下，SWE-AGILE 在 **SWE-Bench-Verified** 上报告 **30.06%**，高于 **R2EGym 14B (26.8%)**、**SkyRL-Agent-v0 14B (21.6%)** 和 **SWE-Gym 14B (16.4%)**。
- 在 **SWE-Bench Lite** 上，**SWE-AGILE-8B** 报告 **14.77%**，对比 **SWE-smith-7B 的 11.7%** 和 **R2E-Gym 的 11.0%**。摘录里只包含动态上下文分析的部分消融结果，因此这些研究的完整定量拆分在这里无法获得。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11716v1](http://arxiv.org/abs/2604.11716v1)
