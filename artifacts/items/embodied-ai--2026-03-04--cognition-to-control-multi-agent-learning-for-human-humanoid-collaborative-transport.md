---
source: arxiv
url: http://arxiv.org/abs/2603.03768v1
published_at: '2026-03-04T06:24:55'
authors:
- Hao Zhang
- Ding Zhao
- H. Eric Tseng
topics:
- human-robot-collaboration
- multi-agent-reinforcement-learning
- humanoid-control
- vision-language-models
- whole-body-control
relevance_score: 0.68
run_id: materialize-outputs
---

# Cognition to Control - Multi-Agent Learning for Human-Humanoid Collaborative Transport

## Summary
该论文提出 C2C（cognition-to-control）分层框架，用于人类与类人机器人协作搬运，把高层语义推理、战术协同决策和高频全身控制明确分离。核心目标是在接触丰富、长时程的人机协作任务中，同时实现可解释的认知规划与稳定可靠的物理执行。

## Problem
- 解决的问题是：如何把高层任务意图（如“绕过障碍把物体运到目标处”）稳定地转成与人类伙伴同步的全身接触控制，尤其是在长时程、接触约束、安全约束都存在的人机协作搬运中。
- 这很重要，因为传统脚本式 leader-follower、意图推断或单智能体 RL 往往在人的行为变化时变脆弱，容易出现振荡、失稳、掉落或无法泛化到复杂环境。
- 现有 VLA/VLM 系统通常偏低频、偏反应式，难以直接承担毫秒级连续控制；而纯控制方法又难以利用开放词汇语义和长期规划信息。

## Approach
- 论文提出三层结构：**VLM grounding 层**先从多视角感知中生成共享的 2D 锚点/路径；**MARL skill 层**根据这些锚点做分布式战术协同；**WBC 层**再把战术命令变成满足动力学、接触稳定和可行性的高频关节控制。
- 核心机制可简单理解为：VLM 只负责回答“往哪里走”，MARL 负责回答“人与机器人现在如何配合地走/搬/转”，WBC 负责回答“具体怎么稳定地动身体和手臂”。
- 协作被建模为 **Markov potential game**，使用共享团队奖励来对齐多智能体目标，避免显式 leader-follower 角色分配或单独的人类意图预测，让 leader-follower 行为从训练中自然涌现。
- MARL 动作采用**残差控制**：策略不是从零输出整个动作，而是在一个名义搬运控制器之上输出小的战术修正（如底盘速度、质心高度、躯干姿态、手腕偏移），从而更易学习并适应伙伴动态。
- 训练上采用 **CTDE**（集中训练、分散执行）和 joint-action critic，以减轻伙伴策略变化带来的非平稳性；实验平台包含 Isaac Lab 仿真与 Unitree G1 + 人类的现实部署。

## Results
- 在 9 个协作场景上，MARL + C2C 架构整体优于脚本基线。表 III 显示机器人脚本基线平均成功率（architecture synergy index）为 **56.5%**，而 **HAPPO 80.6%**、**HATRPO 83.0%**、**PCGrad 83.2%**；相对脚本基线总体增益为 **+45.6%**。
- 分场景看，成功率最高达到 **88.6% ± 3.5**（S21 Narrow gate, PCGrad），而对应脚本基线为 **59.2% ± 9.0**；例如 S31 Facing mode 中，脚本为 **52.8% ± 8.1**，HATRPO 达到 **84.4% ± 1.6**，架构增益 **+55.9%**。
- 其他代表性提升包括：S11 Alignment 从 **65.4% ± 7.2** 提升到 **87.9% ± 4.5**（HATRPO）；S22 S-shaped path 从 **57.5% ± 8.8** 提升到 **82.1% ± 5.0**（HATRPO）；S33 Pivoting 从 **49.6% ± 8.3** 提升到 **78.6% ± 4.5**（PCGrad）。
- 消融结果显示完整三层结构是必要的：**No cognition** 和 **No skill** 都直接失败，而 **Full hierarchy** 在给出的消融表中达到 **78.6%** 成功率，平均完成时间 **81.2 s**。
- 论文还声称在真实世界 Unitree G1 + 人类协作实验中，相比单智能体基线具有更高成功率、更好完成时间和更低物体倾斜率，但当前摘录未给出图 4(c) 的具体数值。

## Link
- [http://arxiv.org/abs/2603.03768v1](http://arxiv.org/abs/2603.03768v1)
