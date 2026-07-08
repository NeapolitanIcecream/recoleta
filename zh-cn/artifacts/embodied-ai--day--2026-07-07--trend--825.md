---
kind: trend
trend_doc_id: 825
granularity: day
period_start: '2026-07-07T00:00:00'
period_end: '2026-07-08T00:00:00'
topics:
- "\u673A\u5668\u4EBA\u5B66"
- "\u89C6\u89C9-\u8BED\u8A00-\u52A8\u4F5C\u6A21\u578B"
- "\u4E16\u754C\u6A21\u578B"
- "3D \u64CD\u4F5C"
- "\u6A21\u4EFF\u5B66\u4E60"
- "\u7075\u5DE7\u64CD\u4F5C"
- "\u673A\u5668\u4EBA\u89C4\u5212"
run_id: materialize-outputs
aliases:
- recoleta-trend-825
tags:
- recoleta/trend
- "topic/\u673A\u5668\u4EBA\u5B66"
- "topic/\u89C6\u89C9-\u8BED\u8A00-\u52A8\u4F5C\u6A21\u578B"
- "topic/\u4E16\u754C\u6A21\u578B"
- "topic/3d-\u64CD\u4F5C"
- "topic/\u6A21\u4EFF\u5B66\u4E60"
- "topic/\u7075\u5DE7\u64CD\u4F5C"
- "topic/\u673A\u5668\u4EBA\u89C4\u5212"
language_code: zh-CN
---

# 机器人策略工作正在集中于几何、生成演示和控制延迟

## Overview
当天的机器人论文把物理细节放进策略流水线。视觉-语言-动作（VLA）模型加入 3D 结构、可复用演示、缓存动作块和显式交接检查。RynnWorld-4D、RynnWorld-Teleop 和 Lift3D-VLA 的重点最清楚：让机器人控制更快、更有空间依据，同时减少对原始物理数据采集的依赖。

## Clusters

### 用于操作和遥操作的 4D 世界模型
RynnWorld-4D 将未来预测同时建模为 RGB、深度和光流。深度把像素提升为 3D 点，光流在时间上连接这些点，让策略获得关于接触和运动的场景流视角。所报告的数据规模在这一时期较大：Rynn4DDataset 1.0 超过 2.544 亿帧。策略路径在 RTX 5090 上每次规划仍需 1,106 ms，其中世界模型占 990 ms，因此延迟仍是核心约束。

RynnWorld-Teleop 将动作条件视频模型用作数据引擎。操作员手部姿态驱动以机器人为中心的第一视角视频，生成的数据集把帧与双臂和灵巧手的 54 维机器人动作配对。蒸馏模型报告在单张 H100 上达到 40+ FPS，使交互式生成具备可行性。论文声称使用生成数据实现零样本 sim-to-real 迁移，但可用摘录没有包含成功率表。

#### Evidence
- [RynnWorld-4D: 4D Embodied World Models for Robotic Manipulation](../Inbox/2026-07-07--rynnworld-4d-4d-embodied-world-models-for-robotic-manipulation.md): 概述 RGB-深度-光流预测、Rynn4DDataset 规模和策略延迟。
- [RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation](../Inbox/2026-07-07--rynnworld-teleop-an-action-conditioned-world-model-for-digital-teleoperation.md): 描述动作条件数字遥操作、40+ FPS 生成和 54 维动作标签。

### VLA 策略中的 3D 几何
Lift3D-VLA 在复用预训练 2D 视觉编码器的同时，把点云推理加入 VLA 策略。它把 3D 点投影到六个虚拟平面上，将 1024 个点标记化为 256 个 token，并训练编码器重建当前几何和预测下一帧几何。动作解码器还把动作块预测分散到 LLaMA2-7B 的各层中。

报告中的提升很具体：MetaWorld 平均成功率提高 10.8 个百分点，RLBench 提高 11.1 个百分点，并比摘录中最强的真实世界基线高 4 个百分点。这一组结果的意义在于，当天最强的操作声明绑定在可达性、遮挡、接触和未来几何上，而不只依赖语言条件图像特征。

#### Evidence
- [Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation](../Inbox/2026-07-07--lift3d-vla-lifting-vla-models-to-3d-geometry-and-dynamics-aware-manipulation.md): 给出点云方法、训练设置和基准差值。

### 高效的 VLA 训练和推理
ActionCache 通过复用过去的动作块来降低基于流的 VLA 模型推理成本。紧凑键检索缓存动作，系统随后直接执行该动作，或用一到两个流步骤细化它。在使用 π0.5 的 VLABench 上，完整模型以 18.8 ms 的动作头延迟达到 38.8% 成功率；不做细化的 ActionCache 以 1.6 ms 达到 32.9%。经过一步细化后，它以 3.6 ms 达到 32.4%，而直接一步生成降至 6.8%。

SIEVE 处理训练侧问题。它在夹爪或手部状态变化处切分演示，聚类可复用的视觉-运动原语，并在原语序列桶内选择中心轨迹。在使用 Qwen3-VL-4B-GR00T 的 Bridge-V2 上，50% 演示和 25K 步训练达到 56.3% 平均成功率，高于使用 50K 步的全数据训练结果 51.8%。证据给出一条实用结论：选择和复用可以提高机器人策略质量，而不必扩大每个数据集和每次前向计算。

#### Evidence
- [Training-Free Acceleration for Vision-Language-Action Models with Action Caching and Refinement](../Inbox/2026-07-07--training-free-acceleration-for-vision-language-action-models-with-action-caching-and-refinement.md): 报告 ActionCache 机制、延迟和成功率比较。
- [SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models](../Inbox/2026-07-07--sieve-structure-aware-data-selection-for-imitation-learning-with-vla-models.md): 报告 SIEVE 选择方法和 Bridge-V2 成功率结果。

### 部署失败暴露薄弱的技能边界
BEHAVIOR-1K 交接研究显示，高单技能分数不能保证长时程机器人成功。多个孤立技能得分较高，包括 pick_up_from 的 96.5% 和 place_on 的 100.0%，但端到端任务谓词成功被描述为接近零。在 30 次 rollout 中，平均进度为 19.5%。一条 10 次 rollout 的轨迹记录了 130 次失败的技能尝试，包括抓取控制、放置、目标定位和导航就绪失败。

LAMP 为真实硬件给出一条互补路径：用学习到的 2-D 潜在运动先验约束灵巧手探索。它从小规模演示集开始，在四个真实机器人任务上达到 56.25% 的平均模仿学习成功率，并在在线强化学习后达到 98.75% 的平均最终成功率。消融结果很明确：移除低维瓶颈后，最终成功率降至 55.0%；原始行为克隆在强化学习后平均为 3.75%。

#### Evidence
- [Diagnosing Semantic Handoff Failures in Agent-Orchestrated Vision-Language-Action Skill Composition](../Inbox/2026-07-07--diagnosing-semantic-handoff-failures-in-agent-orchestrated-vision-language-action-skill-composition.md): 详述语义交接失败、孤立技能分数、rollout 进度和失败类别。
- [LAMP: Latent Motion Prior-Guided Real-World Learning for Dexterous Hand Manipulation](../Inbox/2026-07-07--lamp-latent-motion-prior-guided-real-world-learning-for-dexterous-hand-manipulation.md): 报告 LAMP 的潜在运动先验、真实机器人任务结果和消融。
