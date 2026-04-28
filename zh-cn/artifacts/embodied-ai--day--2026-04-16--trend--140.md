---
kind: trend
trend_doc_id: 140
granularity: day
period_start: '2026-04-16T00:00:00'
period_end: '2026-04-17T00:00:00'
topics:
- robotics
- vision-language-action
- data generation
- dexterous manipulation
- sim2real
run_id: materialize-outputs
aliases:
- recoleta-trend-140
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/data-generation
- topic/dexterous-manipulation
- topic/sim2real
language_code: zh-CN
---

# 机器人论文把结构引入控制与数据采集

## Overview
这一天的机器人论文最强的一点很明确：研究者正在把任务结构放进数据路径和决策路径里。最清楚的例子是 $\pi_{0.7}$、WAV 和 ShapeGen。一条路线把更丰富的提示和潜空间规划加入 VLA 控制。另一条路线构建更窄、更关注几何的数据生成与采集系统，让策略从一开始就看到正确的变化。

## Clusters

### 结构化 VLA 控制
通用机器人模型现在不只是增加数据量，也在提示和执行过程中加入更多结构。$\pi_{0.7}$ 将动作生成建立在任务文本、子任务文本、轨迹元数据、控制模式，以及来自世界模型的可选子目标图像之上。论文将这种提示设计与长程灵巧任务上的零样本行为联系起来，包括制作咖啡、折叠衣物和处理垃圾，以及跨本体迁移。WAV 在规划侧推进了同一方向。它把未来预测器、价值模型和动作解码器结合起来，然后在潜空间中搜索，而不是直接搜索原始动作。这里的证据对机制的说明强于对具体优势幅度的说明，因为摘录没有给出两篇论文的完整任务表。

#### Evidence
- [$π_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities](../Inbox/2026-04-16--p-0-7-a-steerable-generalist-robotic-foundation-model-with-emergent-capabilities.md): 基于提示条件的 VLA 设计、模型规模，以及声称的零样本灵巧泛化。
- [World-Value-Action Model: Implicit Planning for Vision-Language-Action Systems](../Inbox/2026-04-16--world-value-action-model-implicit-planning-for-vision-language-action-systems.md): 用于长时程 VLA 控制的 world-value-action 分解与潜空间规划主张。

### 数据生成直接对准缺口
有几篇论文通过围绕它们关心的失败模式生成更好的机器人数据来解决泛化问题。ShapeGen 用学习到的 3D 形变在同一类别内替换物体，生成新的 real-to-real 示范。提升很具体：在未见过的实例上，hang_mug 从 5% 提高到 45%，hang_mug_hard 从 5% 提高到 50%，serve_kettle 从 35% 提高到 75%。DockAnywhere 在存在对接误差的移动操作中采用了类似做法。它复用示范中接触密集的部分，只对接近阶段重新规划，并在 3D 中编辑 RGB-D 观测。在 ManiSkill 的五个对接点设置下，它的总体成功率达到 78.9%，而普通 DP3 为 17.8%，DP3+DemoGen 为 74.2%。共同模式是做范围较窄的增强，同时保持任务几何不变。

#### Evidence
- [ShapeGen: Robotic Data Generation for Category-Level Manipulation](../Inbox/2026-04-16--shapegen-robotic-data-generation-for-category-level-manipulation.md): real-to-real 形状增强，以及在未见物体实例上的任务级提升。
- [DockAnywhere: Data-Efficient Visuomotor Policy Learning for Mobile Manipulation via Novel Demonstration Generation](../Inbox/2026-04-16--dockanywhere-data-efficient-visuomotor-policy-learning-for-mobile-manipulation-via-novel-demonstration-generation.md): 对接位姿增强方法，以及视角变化下的基准结果。

### 灵巧数据采集变得更实用
这一时间窗口内的灵巧操作工作更重视数据是如何采集的，而不只是模型设计。DEX-Mouse 是一种便携式手持接口，用现成部件搭建，成本低于 150 美元。在前臂附着式设置中，它取得了 86.67% 的总体成功率和 10.05 秒的平均完成时间，在论文报告的研究中超过了两个手套基线。HRDexDB 在数据集规模上处理了同一个瓶颈。它在同样的 100 个物体上配对人类和机器人的抓取数据，覆盖 1.4K 次试验、12.8M 帧、23 路视频视角、物体位姿、触觉信号，以及四种本体上的成功标签。这为跨本体学习和抓取分析提供了更扎实的数据基础。

#### Evidence
- [DEX-Mouse: A Low-cost Portable and Universal Interface with Force Feedback for Data Collection of Dexterous Robotic Hands](../Inbox/2026-04-16--dex-mouse-a-low-cost-portable-and-universal-interface-with-force-feedback-for-data-collection-of-dexterous-robotic-hands.md): 低成本灵巧数据采集接口，以及附着模式用户研究结果。
- [HRDexDB: A Large-Scale Dataset of Dexterous Human and Robotic Hand Grasps](../Inbox/2026-04-16--hrdexdb-a-large-scale-dataset-of-dexterous-human-and-robotic-hand-grasps.md): 大规模配对人机抓取数据集，包含同步触觉和运动数据。

### 抽象模拟器有了可落地的迁移方法
这里的 sim2real 工作关注的是模拟器缺少真实状态的情况，而不只是物理参数没有调准。ASTRA 将其视为一个依赖历史的落地问题。它从抽象化的真实轨迹中学习循环潜状态，再用转移、奖励和下一状态损失来修正模拟器。报告出的证据有选择性，但有用：在腿长变为 1.25× 的形态变化 AntMaze 测试中，U-Maze 上的成功率达到 65%，而直接迁移为 21%。这一点很重要，因为很多实际模拟器本来就有意保持粗粒度，而这篇论文给出了一个在真实数据有限时如何在这种设定下训练的具体方法。

#### Evidence
- [Abstract Sim2Real through Approximate Information States](../Inbox/2026-04-16--abstract-sim2real-through-approximate-information-states.md): 对抽象 sim2real 的形式化，以及 ASTRA 在形态变化上的结果。
