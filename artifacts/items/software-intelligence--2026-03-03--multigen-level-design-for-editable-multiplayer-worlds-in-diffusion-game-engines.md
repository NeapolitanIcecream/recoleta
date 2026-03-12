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
- multiplayer-world-model
- level-design
- interactive-video-generation
relevance_score: 0.62
run_id: materialize-outputs
---

# MultiGen: Level-Design for Editable Multiplayer Worlds in Diffusion Game Engines

## Summary
MultiGen提出一种带显式外部记忆的扩散式游戏引擎，用于生成可编辑、可复现、且支持多人共享状态的第一人称游戏世界。核心贡献是在传统“只看最近几帧”的生成方式之外，加入可持续读写的地图与玩家状态记忆。

## Problem
- 现有扩散游戏引擎通常把状态隐含在有限帧上下文里，导致长时生成容易漂移、难以复现，也难让用户直接编辑世界结构。
- 这使得多人共享世界尤其困难：不同玩家缺少统一、可读写的公共状态，跨视角交互一致性难保证。
- 该问题重要，因为可控关卡设计和多人一致交互是生成式游戏引擎走向真实创作与互动娱乐的关键能力。

## Approach
- 方法把系统拆成三个模块：**Memory**保存外部世界状态（2D地图几何与玩家位姿）、**Observation**根据历史帧+记忆读出+动作生成下一帧、**Dynamics**根据动作与特征更新位姿。
- 外部记忆是核心机制：用户可直接编辑一个俯视2D minimap，模型在每一步都查询这张地图，而不是仅靠短期视觉历史“猜”世界结构。
- 为了把地图信息喂给视觉生成器，系统从当前位姿对地图做射线追踪，得到1D深度/视差信号，并将其作为额外条件输入扩散UNet。
- 动作通过嵌入和交叉注意力注入观察模型；位姿更新由一个轻量Transformer预测增量位姿，从而推进共享世界状态。
- 在多人模式下，每个玩家各自运行观察/动力学模块，但共同读写同一个外部记忆，因此一个玩家的动作可以影响另一个玩家看到的结果。

## Results
- 关卡设计评测基于 **Doom**，数据来自 **100** 个程序生成地图、超过 **1000万** 帧游戏数据。
- 与类似 **GameNGen** 的无外部记忆基线相比，整体画面相似性更好：**SSIM** 从 **0.457** 提升到 **0.469**，**LPIPS** 从 **0.442** 降到 **0.416**。
- 在早期步骤 **1–128**，**SSIM** 从 **0.476** 提升到 **0.484**，**LPIPS** 从 **0.389** 降到 **0.375**。
- 在更能体现长时稳定性的后期步骤 **128–196**，**SSIM** 从 **0.418** 提升到 **0.438**，**LPIPS** 从 **0.549** 降到 **0.496**，说明外部记忆更能抑制长程结构漂移。
- 论文还声称实现了实时多人生成、跨玩家视角一致、可发生击杀/重生等共享交互，但给定摘录中未提供多人部分的定量指标。

## Link
- [http://arxiv.org/abs/2603.06679v1](http://arxiv.org/abs/2603.06679v1)
