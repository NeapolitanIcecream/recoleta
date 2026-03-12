---
source: arxiv
url: http://arxiv.org/abs/2603.06679v1
published_at: '2026-03-03T18:58:17'
authors:
- Ryan Po
- David Junhao Zhang
- Amir Hertz
- Gordon Wetzstein
- Neal Wadhwa
- Nataniel Ruiz
topics:
- diffusion-game-engine
- external-memory
- multiplayer-worlds
- level-design
- video-world-model
relevance_score: 0.2
run_id: materialize-outputs
---

# MultiGen: Level-Design for Editable Multiplayer Worlds in Diffusion Game Engines

## Summary
MultiGen 提出一种带**显式外部记忆**的扩散式游戏引擎，用于生成可编辑、可复现且支持多人共享状态的交互世界。其核心贡献是把“世界状态”从短时视频上下文中剥离出来，使关卡设计和多人一致性交互都更自然。

## Problem
- 现有扩散游戏引擎多是**下一帧预测器**，世界状态隐含在有限历史帧里，导致长时生成容易漂移、难以复现。
- 用户很难**直接编辑环境结构**；想事先指定关卡布局时，模型往往无法在长 rollout 中稳定遵守。
- 多人场景中，不同玩家通常没有真正**共享的底层世界状态**，因此跨视角一致性和相互作用难以维持，这对可交互仿真和游戏体验都很重要。

## Approach
- 引入独立于上下文窗口的**外部记忆**，持续保存静态地图和玩家位姿，而不是只依赖最近几帧图像作为状态。
- 将系统拆成三个模块：**Memory**（保存地图几何与玩家 pose）、**Observation**（基于历史帧+记忆读出+动作生成下一帧）、**Dynamics**（根据动作和特征更新下一时刻 pose）。
- 用用户可编辑的**俯视 2D minimap** 作为环境蓝图；模型在每一步从地图和当前位姿中做 ray-tracing，得到 1D 深度/视差条件信号，再送入扩散 UNet。
- 动作通过 learned embedding 注入观察模型；动力学模块用一个轻量 transformer 预测位姿增量，从而推进共享状态。
- 多人时，每个玩家各自运行 Observation/Dynamics，但**共同读写同一个外部记忆**，因此能生成彼此一致、可相互影响的第一人称视角。

## Results
- 关卡设计数据集：作者在 **100 个程序生成 Doom 地图**上采集了**超过 1000 万帧**游戏数据，用于训练跨布局泛化。
- 与类似 **GameNGen** 的无外部记忆基线相比，作者在 level-conditioned rollout 上报告更好的结构一致性：**SSIM(all) 0.469 vs 0.457**，**LPIPS(all) 0.416 vs 0.442**。
- 在早期区间 **1–128 步**，方法达到 **SSIM 0.484 vs 0.476**，**LPIPS 0.375 vs 0.389**，说明短期质量也有提升。
- 在后期区间 **128–196 步**，提升更明显：**SSIM 0.438 vs 0.418**，**LPIPS 0.496 vs 0.549**，支持其“外部记忆减轻长时漂移”的主张。
- 对多人生成，摘录中主要提供**定性结果**：两名玩家可在共享世界中相遇、击杀、重生，并在双方视角中保持一致；文段未给出明确的多人定量指标。

## Link
- [http://arxiv.org/abs/2603.06679v1](http://arxiv.org/abs/2603.06679v1)
