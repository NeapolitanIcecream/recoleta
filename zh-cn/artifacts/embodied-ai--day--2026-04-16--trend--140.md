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

# 机器人论文把结构放进控制和数据采集

## Overview
这一天的机器人论文最强的一点，是研究者把任务结构放进了数据路径和决策路径。最清楚的例子是 $\pi_{0.7}$、WAV 和 ShapeGen。一条线给 VLA 控制加入更丰富的提示和潜在规划。另一条线构建更窄、几何感知的数据生成和采集系统，让策略一开始就看到正确的变化。

## Clusters

### Structured VLA control
通用机器人模型现在在提示和 rollout 中加入更多结构，而不只是更多数据。$\pi_{0.7}$ 让动作生成同时依赖任务文本、子任务文本、episode 元数据、控制模式，以及来自世界模型的可选子目标图像。论文把这种提示设计和长时程灵巧任务上的零样本行为联系起来，例如做浓缩咖啡、叠衣服和处理垃圾，还包括跨 embodiment 迁移。WAV 在规划侧延续了同一思路。它把未来预测器、价值模型和动作解码器结合起来，然后在潜在空间里搜索，而不是直接在原始动作上搜索。这里的证据更强的是机制，而不是精确幅度，因为摘录里没有给出这两篇论文的完整任务表。

#### Evidence
- [$π_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities](../Inbox/2026-04-16--p-0-7-a-steerable-generalist-robotic-foundation-model-with-emergent-capabilities.md): Prompt-conditioned VLA design, model scale, and claimed zero-shot dexterous generalization.
- [World-Value-Action Model: Implicit Planning for Vision-Language-Action Systems](../Inbox/2026-04-16--world-value-action-model-implicit-planning-for-vision-language-action-systems.md): World-value-action decomposition and latent-space planning claims for long-horizon VLA control.

### Data generation targets the gap directly
几篇论文通过围绕它们关心的失败模式生成更好的机器人数据来处理泛化问题。ShapeGen 用学到的 3D warp 在同一类别内替换物体，生成新的 real-to-real 演示。收益很明确：hang_mug 在未见实例上的成功率从 5% 升到 45%，hang_mug_hard 从 5% 升到 50%，serve_kettle 从 35% 升到 75%。DockAnywhere 也用同样思路处理 docking 误差下的移动操作。它复用演示里接触丰富的部分，只重新规划接近段，并在 3D 中编辑 RGB-D 观测。在 ManiSkill 的 5 个 docking 点设置下，它达到 78.9% 的总体成功率，而普通 DP3 是 17.8%，DP3+DemoGen 是 74.2%。共同模式是只做窄范围增强，同时保持任务几何不变。

#### Evidence
- [ShapeGen: Robotic Data Generation for Category-Level Manipulation](../Inbox/2026-04-16--shapegen-robotic-data-generation-for-category-level-manipulation.md): Real-to-real shape augmentation and task-level gains on unseen object instances.
- [DockAnywhere: Data-Efficient Visuomotor Policy Learning for Mobile Manipulation via Novel Demonstration Generation](../Inbox/2026-04-16--dockanywhere-data-efficient-visuomotor-policy-learning-for-mobile-manipulation-via-novel-demonstration-generation.md): Docking-pose augmentation method and benchmark results under viewpoint variation.

### Dexterous data collection gets more practical
这个窗口里的灵巧操作工作更重视数据如何采集，而不只是模型设计。DEX-Mouse 是一款便携式手持接口，用现成零件搭建，成本低于 150 美元。按前臂附着式设置使用时，它在报告的研究里达到 86.67% 的总体成功率和 10.05 秒的平均完成时间，优于两种手套基线。HRDexDB 在数据集规模上处理同样的瓶颈。它把人和机器人的抓取配对到同样的 100 个物体上，包含 1.4K 次试验、1280 万帧、23 个视频视角、物体位姿、触觉信号，以及四种 embodiment 下的成功标签。这给跨 embodiment 学习和抓取分析提供了更扎实的材料。

#### Evidence
- [DEX-Mouse: A Low-cost Portable and Universal Interface with Force Feedback for Data Collection of Dexterous Robotic Hands](../Inbox/2026-04-16--dex-mouse-a-low-cost-portable-and-universal-interface-with-force-feedback-for-data-collection-of-dexterous-robotic-hands.md): Low-cost dexterous data collection interface with attached-mode user study results.
- [HRDexDB: A Large-Scale Dataset of Dexterous Human and Robotic Hand Grasps](../Inbox/2026-04-16--hrdexdb-a-large-scale-dataset-of-dexterous-human-and-robotic-hand-grasps.md): Large paired human-robot grasp dataset with synchronized tactile and motion data.

### Abstract simulators get a grounded transfer recipe
这里的 sim2real 工作关注的是仿真器缺少真实状态的情况，而不只是物理参数没调好。ASTRA 把这看成一个依赖历史的 grounding 问题。它从抽象化的真实轨迹中学习循环潜在状态，再用转移、奖励和下一状态损失来修正仿真器。报告中的证据有选择性，但有用：在一个形态变化的 AntMaze 测试里，腿长变为 1.25 倍时，U-Maze 上的成功率达到 65%，而直接迁移是 21%。这很重要，因为很多实际仿真器本来就会保持粗粒度，论文给出了在这种设置下用有限真实数据训练的具体做法。

#### Evidence
- [Abstract Sim2Real through Approximate Information States](../Inbox/2026-04-16--abstract-sim2real-through-approximate-information-states.md): Formalization of abstract sim2real and reported morphology-shift result for ASTRA.
