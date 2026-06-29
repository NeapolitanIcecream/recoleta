---
kind: trend
trend_doc_id: 499
granularity: day
period_start: '2026-06-01T00:00:00'
period_end: '2026-06-02T00:00:00'
topics:
- robotics
- VLA
- world models
- manipulation
- semantic grounding
- 3D geometry
- policy evaluation
- reinforcement learning
run_id: materialize-outputs
aliases:
- recoleta-trend-499
tags:
- recoleta/trend
- topic/robotics
- topic/vla
- topic/world-models
- topic/manipulation
- topic/semantic-grounding
- topic/3d-geometry
- topic/policy-evaluation
- topic/reinforcement-learning
language_code: zh-CN
---

# 机器人策略论文集中在预测、几何和更难的 VLA 评估

## Overview
这一时期的机器人工作主要围绕 Vision-Language-Action（VLA）策略展开。最强的模式是对控制的现实压力：AHEAD 预测移动物体的未来视觉 token，Dex-BEV 加入三维对齐，RoboSemanticBench 则显示，抓取能力可能掩盖语义选择薄弱的问题。

## Clusters

### Predictive world models for moving scenes and data growth
几篇论文把预测当作机器人策略中缺失的控制层。AHEAD 在冻结的 7B OpenVLA 模型外包上一层 490 万参数的潜在世界模型，用来预测与任务相关的未来视觉 token。它的提升在物体运动带来时序问题时最明显：在 20 个动态仿真场景中，成功率为 79% 到 97%；在实体 xArm 7 上的抛接任务中为 19/30，而列出的所有基线都是 0/30。

RoboDream 解决的是另一个瓶颈：示范数据供给。它先把视频扩散锚定到只包含机器人运动的渲染结果，再补入物体和场景。混合真实数据和生成数据后，四个操作任务上的平均真实世界成功率达到 62.5%，而 Real-50 基线为 36.3%。在报告的设置里，扩大混合数据后成功率达到 72.5% 到 73.75%。

#### Evidence
- [Intercepting the Future: Latent-Space Predictive World Model for Dynamic VLA Manipulation](../Inbox/2026-06-01--intercepting-the-future-latent-space-predictive-world-model-for-dynamic-vla-manipulation.md): AHEAD method and dynamic manipulation results.
- [RoboDream: Compositional World Models for Scalable Robot Data Synthesis](../Inbox/2026-06-01--robodream-compositional-world-models-for-scalable-robot-data-synthesis.md): RoboDream data synthesis method and real-world policy results.

### 3D action alignment becomes a concrete performance lever
Dexterity-BEV 和 Lie Diffuser Actor 都把位姿几何显式放进了策略接口。Dexterity-BEV 把像素映射到共享的三维鸟瞰图（BEV）坐标系里，并在这个坐标系中表达视觉输入、本体感觉和动作。它在修改后的 LIBERO 相机和位姿测试中报告了 89.9% 的平均成功率，而 X-VLA 和 2D 消融都低于 10%。

Lie Diffuser Actor 通过在切空间里加噪声、再用指数映射把样本映回去，让扩散式位姿生成保持在 SE(3) 这个刚体位姿群上。在 CALVIN ABCD→D 上，它把平均任务长度提高到 3.584，3D Diffuser Actor 为 3.288；在跨架构测试中，它把 OpenVLA-OFT 在 LIBERO Long 上的成功率从 92.20% 提高到 94.13%。

#### Evidence
- [Dexterity-BEV: Aligning 3D World and Actions for Generalizable Robot Policies Learning](../Inbox/2026-06-01--dexterity-bev-aligning-3d-world-and-actions-for-generalizable-robot-policies-learning.md): Dex-BEV 3D alignment method and LIBERO/RoboTwin results.
- [The Lie We Tell: Correcting the Euclidean Fallacy in Vision Language Action Policies via Score Matching on Tangent Space](../Inbox/2026-06-01--the-lie-we-tell-correcting-the-euclidean-fallacy-in-vision-language-action-policies-via-score-matching-on-tangent-space.md): Lie Diffuser Actor SE(3) diffusion method and benchmark results.

### Evaluation work finds failures hidden by ordinary success rates
RoboSemanticBench 把抓取能力和语义目标选择分开评估。它把数学、常识和事实问题转成抓取放置任务。在每个模型、每个套件 500 个仿真回合的评估中，pi0.5 的平均任务成功率最好，为 21.8%，但它的归一化语义落地分数只有 5.2%。几个被评估的模型分数为负，这意味着它们在成功抓取后的目标选择低于随机选择归一化基线。

FATE-VLA 用自适应测试生成寻找容易失败的操作场景。在 GR00T-N1.6 上，最佳变体把发现的失败率提高到 65.3%，随机测试为 35.6%。在 EO-1 上，失败发现率达到 60.0%，随机测试为 36.7%。这些结果把评估目标说得更具体：在物体、位姿和指令条件下找出成簇的失败。

#### Evidence
- [RoboSemanticBench: Diagnosing Semantic Grounding in Action Prediction for VLA Models](../Inbox/2026-06-01--robosemanticbench-diagnosing-semantic-grounding-in-action-prediction-for-vla-models.md): RoboSemanticBench benchmark design and semantic grounding scores.
- [FATE-VLA:Failue-aware test generation for vision-language-action models](../Inbox/2026-06-01--fate-vla-failue-aware-test-generation-for-vision-language-action-models.md): FATE-VLA adaptive failure discovery method and results.

### Policy improvement uses guided rollouts and learned rewards
两篇论文都在处理怎样让策略改进少浪费。EG-GRPO 用在线 rollout，再加上每个 GRPO 组里的一条基于规则的专家轨迹，训练一个空中 VLA 策略。以 OpenVLA-OFT 为起点，它把监督微调下的总成功率从 26.1% 提高到 55.6%，意图对齐分数从 4.50 提高到 7.24。它的并行 rollout 系统把每步 rollout 时间缩短了 43.5%。

CSIL++ 用从示范中学到的 coherent reward 改进 pi-0.5 在稀疏仿真操作任务上的表现。集成版在六个任务中的五个上至少达到 90% 成功率，其中 Threading 为 0.92，pi-0.5 基线为 0.14。现有摘录里的证据只来自仿真，但这些提升说明，少写手工奖励也能改进大型行为模型。

#### Evidence
- [Towards Precise Intent-Aligned VLA Aerial Navigation via Expert-Guided GRPO](../Inbox/2026-06-01--towards-precise-intent-aligned-vla-aerial-navigation-via-expert-guided-grpo.md): EG-GRPO training setup and aerial navigation results.
- [Coherent Off-Policy Improvement of Large Behavior Models with Learned Rewards](../Inbox/2026-06-01--coherent-off-policy-improvement-of-large-behavior-models-with-learned-rewards.md): CSIL++ learned reward method and simulated manipulation results.
