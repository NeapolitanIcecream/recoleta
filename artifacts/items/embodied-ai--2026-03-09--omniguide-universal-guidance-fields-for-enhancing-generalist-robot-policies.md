---
source: arxiv
url: http://arxiv.org/abs/2603.10052v1
published_at: '2026-03-09T17:18:13'
authors:
- Yunzhou Song
- Long Le
- Yong-Hyun Park
- Jie Wang
- Junyao Shi
- Lingjie Liu
- Jiatao Gu
- Eric Eaton
- Dinesh Jayaraman
- Kostas Daniilidis
topics:
- vision-language-action
- test-time-guidance
- generalist-robot-policy
- collision-avoidance
- semantic-grounding
- robot-manipulation
relevance_score: 0.96
run_id: materialize-outputs
---

# OmniGuide: Universal Guidance Fields for Enhancing Generalist Robot Policies

## Summary
OmniGuide提出一种统一的推理时引导框架，用3D空间中的“吸引/排斥能量场”去修正通用VLA机器人的动作采样。它的目标是在不重新训练、也不增加机器人数据的前提下，让现有通用策略在复杂、拥挤和高精度任务上更可靠、更安全。

## Problem
- 现有VLA通用机器人策略虽然覆盖任务广，但在**复杂空间理解、拥挤场景操作、精细操控、碰撞规避**上常常失效，属于“会很多但都不够精”。
- 常见补救办法依赖**额外高质量机器人数据和后训练/微调**，成本高且难扩展，还可能破坏原有泛化能力。
- 不同外部能力来源（3D几何、VLM语义推理、人类演示）很强，但缺少一种**统一方式**在测试时把它们转成可直接指导VLA动作生成的信号。

## Approach
- 核心机制很简单：把外部指导信息都写成**可微分的能量函数**，在3D空间里形成“朝目标吸引、离障碍排斥”的场，然后把这个梯度反传到VLA生成的动作上，改变采样方向。
- 方法适用于**diffusion/flow-matching**类生成式机器人策略；在每个去噪步骤，先估计当前“干净动作”，再通过可微运动学/动力学模型把动作转成末端执行器的笛卡尔轨迹。
- 然后在轨迹上计算任务能量：如**碰撞规避**用基于SDF的排斥能量，**语义指向**用VLM定位出的3D目标点构造高斯吸引能量，**人类示范**用手部轨迹和机器人轨迹做单调匹配后构造吸引能量。
- 最终更新等于“原VLA的自然动作先验 + 引导梯度”；还可在初始噪声阶段做候选采样筛选，从而兼顾自然性、约束满足和多模态性。
- 该框架可**组合多种异构引导源**，且作者强调无需重训、无需新增机器人数据、实时计算梯度即可在动态环境中工作。

## Results
- 摘要中报告：OmniGuide在仿真和真实环境中、跨多种引导源和两类SOTA通用策略（如 **π0.5、GR00T N1.6**）都带来显著提升。
- 量化结果（摘要明确给出）：**成功率从24.2%提升到92.4%**。
- 量化结果（摘要明确给出）：**避碰/安全率从7.0%提升到93.5%**。
- 作者声称这些提升是在**不需要重训练**、**不需要额外机器人数据**、且**没有显著执行延迟**的条件下获得的。
- 论文还声称：其统一框架能够**达到或超过**以往专门为某一种指导源设计的方法，但给定摘录里**未提供更细的任务级表格、数据集拆分或逐基线数值**。

## Link
- [http://arxiv.org/abs/2603.10052v1](http://arxiv.org/abs/2603.10052v1)
