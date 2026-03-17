---
source: arxiv
url: http://arxiv.org/abs/2603.09542v1
published_at: '2026-03-10T11:51:54'
authors:
- Ziyue Zhu
- Shangyang Wu
- Shuai Zhao
- Zhiqiu Zhao
- Shengjie Li
- Yi Wang
- Fang Li
- Haoran Luo
topics:
- vision-language-action
- neuro-symbolic-ai
- robot-manipulation
- online-reinforcement-learning
- data-efficient-learning
relevance_score: 0.95
run_id: materialize-outputs
---

# NS-VLA: Towards Neuro-Symbolic Vision-Language-Action Models

## Summary
NS-VLA 是一个将神经网络感知、符号化操作原语和在线强化学习结合起来的视觉-语言-动作模型，用于机器人操作。它的目标是在更少示教数据下获得更强的泛化、鲁棒性和探索能力。

## Problem
- 现有端到端 VLA 往往直接从图像和指令回归动作，缺少对可复用操作原语的显式结构建模，因此长时序与组合泛化较弱。
- 许多方法依赖大模型、复杂架构和大量示教数据，但真实机器人中为每个任务收集海量演示并不现实。
- 纯监督模仿通常只能复现示教轨迹，难以在环境中主动探索，从而限制了性能上限与鲁棒性。

## Approach
- 先用冻结的预训练 VLM 编码图像和语言，再生成一个由离散 primitive 组成的任务计划；随后用一个符号分类器预测当前正在执行哪一个 primitive。
- 通过“计划约束 + 单调指针”机制，只允许 primitive 按计划顺序停留或前进一步，简单理解就是让模型按步骤稳定执行，减少来回抖动和错误切换。
- 用符号求解器把当前 primitive 变成动作：先基于该 primitive 只挑选最相关的视觉 token（Top-K 稀疏化），再结合本体状态由 Transformer 一次输出一段动作 chunk，而不是每步都重新密集预测。
- 在线强化学习阶段只更新轻量模块，不改动主干 VLM；奖励同时包含任务成功、primitive 段切换里程碑和段内进度 shaping，并用 KL 约束贴近行为克隆策略以稳定训练。

## Results
- **LIBERO 1-shot（每任务仅 1 条示教）**：NS-VLA 在 2B 参数下取得 **69.1%** 平均成功率，优于 VLA-Adapter **65.3%**、EVOLVE-VLA **61.3%**、UniVLA **55.1%**、OpenVLA-OFT **48.9%**、OpenVLA **35.7%**。
- 在同一 1-shot LIBERO 上，NS-VLA 各子集成绩为：**Spatial 85.7% / Object 75.3% / Goal 70.7% / Long 45.2%**；相比 7B OpenVLA 的 **47.4 / 46.0 / 44.3 / 4.9** 和 3B π0 的 **48.6 / 47.2 / 33.2 / 20.4** 明显更高。
- **LIBERO-Plus 泛化测试（在 full LIBERO 训练后测试扰动环境）**：NS-VLA 平均成功率 **79.4%**，超过 OpenVLA-OFT **69.6%**、RIPT-VLA **68.4%**、π0-Fast **61.6%**、VLA-Adapter **58.9%**、OpenVLA **15.6%**。
- 在 LIBERO-Plus 上，NS-VLA 的四类任务为 **88.1 / 79.0 / 70.2 / 80.3**，其平均性能下降仅 **19.2** 个点；对比 OpenVLA-OFT **27.5**、RIPT-VLA **25.2**、π0-Fast **23.9**，说明扰动下更稳健。
- **Ablation（LIBERO 平均 SR）**：完整 NS-VLA 为 **98.6%**；去掉计划约束降到 **79.7%**，去掉视觉提取器 **90.1%**，去掉动作生成器 **85.2%**，去掉 RL **91.6%**；说明计划约束和 RL 都是关键组件。
- 论文还声称在 CALVIN 上验证了性能、在扰动场景下更鲁棒、并具有更大的探索空间，但给定摘录中未提供 CALVIN 的具体数值。

## Link
- [http://arxiv.org/abs/2603.09542v1](http://arxiv.org/abs/2603.09542v1)
