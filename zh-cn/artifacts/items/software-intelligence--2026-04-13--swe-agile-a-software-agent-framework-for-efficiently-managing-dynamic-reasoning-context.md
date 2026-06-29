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
SWE-AGILE 是一个面向多步代码修复的软件代理框架。它保留最近的详细推理，把较早的推理压缩成简短摘要，并训练模型在这种变化的上下文里工作。在 SWE-Bench-Verified 上，它报告了 7B-8B 开放模型的新最佳结果，使用 Qwen3-8B 达到 24.1% 的成功率。

## 问题
- 多轮软件工程代理需要很长的推理链来检查代码、使用工具并处理边界情况，但保留所有历史推理会让上下文快速膨胀。
- 长上下文会通过“中间遗忘”效应、更高的内存成本，以及更慢的训练和推理，降低代理质量。
- 如果完全丢掉旧推理，代理就必须在每次工具调用后重新推导同样的分析，这会浪费 token，并削弱跨步骤的连续性。

## 方法
- 代理在每一步输出三部分：详细推理、简短推理摘要和下一步动作。
- 它使用动态上下文：完整的观测和动作保留在历史中，最近的推理在滑动窗口里原样保留，更早的推理则用每步摘要替代。
- 训练使用轨迹快照，让每一步都在与推理时相同的可见性限制下学习，而不是在训练时暴露完整的历史思维链。
- 一个 hindsight backfill 流程会重写成功轨迹，把详细推理和摘要补进去，使用真实的未来动作加上原始的浅层思路来合成更好的监督信号。
- 带可验证奖励的强化学习加入了轨迹级压缩奖励，因此模型只有在既解决任务又保持保留上下文尽量短时才会得到奖励。

## 结果
- 在 **SWE-Bench-Verified** 上，**SWE-AGILE (SFT+RL)** 配合 **Qwen3-8B** 达到 **24.1%** 成功率。
- 在同一基准上，**Qwen3-8B 基础模型**得到 **15.83%**，而 **SWE-AGILE (SFT)** 得到 **21.45%**，相对基础模型提升 **35.5%**。
- 论文表示，**24.1%** 在其对比表中为 **7B-8B** 级别设立了新标准，超过 **R2EGym 7B (19.0%)**、**SWE-smith 7B (15.2%)** 和 **SWE-Gym 7B (10.6%)**；它也高于 **SkyRL-Agent-v0 14B (21.6%)**。
- 该方法只使用了 **2.2k** 条训练轨迹，作者称这只是 **SWE-Dev** 使用的 **19.3k** 条轨迹的 **11%**，但 SWE-AGILE 仍以 **24.1%** 的分数略高于 **SWE-Dev 7B (23.4%)**。
- 在 **Qwen3-14B** 上仅使用 SFT 时，SWE-AGILE 在 **SWE-Bench-Verified** 上报告 **30.06%**，高于 **R2EGym 14B (26.8%)**、**SkyRL-Agent-v0 14B (21.6%)** 和 **SWE-Gym 14B (16.4%)**。
- 在 **SWE-Bench Lite** 上，**SWE-AGILE-8B** 报告 **14.77%**，对比 **SWE-smith-7B 的 11.7%** 和 **R2E-Gym 的 11.0%**。摘要里只包含动态上下文分析的部分消融结果，因此这里看不到这些研究的完整定量拆分。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11716v1](http://arxiv.org/abs/2604.11716v1)
