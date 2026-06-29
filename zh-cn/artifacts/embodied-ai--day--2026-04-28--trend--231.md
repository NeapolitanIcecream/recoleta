---
kind: trend
trend_doc_id: 231
granularity: day
period_start: '2026-04-28T00:00:00'
period_end: '2026-04-29T00:00:00'
topics:
- robot learning
- photorealistic simulation
- 3D Gaussian Splatting
- dexterous manipulation
- contact-rich robotics
run_id: materialize-outputs
aliases:
- recoleta-trend-231
tags:
- recoleta/trend
- topic/robot-learning
- topic/photorealistic-simulation
- topic/3d-gaussian-splatting
- topic/dexterous-manipulation
- topic/contact-rich-robotics
language_code: zh-CN
---

# 机器人学习正在缩小视觉仿真与接触执行之间的差距

## Overview
当天的机器人信号是物理执行。GS-Playground 面向带接触物理的高吞吐照片级训练，HANDFUL 把手指当作多步灵巧任务中的稀缺资源。两篇论文都关注让学到的机器人策略在第一次接触之后仍然可用的条件。

## Clusters

### Photorealistic simulation for contact-rich policy training
GS-Playground 将并行物理引擎与批处理的 3D Gaussian Splatting（3DGS）连接起来。3DGS 是一种用于照片级真实场景重建的渲染方法。目标是在不损失强化学习所需模拟规模的前提下，让视觉输入尽量接近真实相机数据。

报告中的数字是主要信号。论文声称在 RTX 4090 级配置上以 640×480 达到约 10,000 FPS 的 3DGS 渲染，支持该分辨率下最多 2048 个渲染场景，并列出最多 4096 个 3DGS 环境。它的剪枝步骤移除了超过 90% 的高斯，同时将 PSNR 损失控制在 0.05 以下。模拟器还把高斯资产绑定到刚体上，因此渲染对象会在接触时随物理状态一起运动。

这对机器人学习很重要，因为接触密集的操作、导航和运动都需要大量试验和有用的图像。Real2Sim 流程补上了另一个实用环节：它把 RGB 采集转换为资产、网格、位姿、尺度和可碰撞的场景元素，减少了构建仿真场景时通常需要的手工工作。

#### Evidence
- [GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning](../Inbox/2026-04-28--gs-playground-a-high-throughput-photorealistic-simulator-for-vision-informed-robot-learning.md): Summary gives the simulator goal, 3DGS and physics design, Real2Sim pipeline, and headline throughput and pruning metrics.

### Finger allocation in sequential dexterous manipulation
HANDFUL 研究了机器人手常见的一种失败模式：稳定的第一次抓取会占用下一步动作需要的手指或接触区域。这个设置要求 LEAP Hand 先拿住一个物体，再在保留初始抓取的同时去推、按、拧、拉或抓另一个物体。

该方法把手指分配给第一次抓取，并保留其他手指可用。奖励函数鼓励主动手指发生接触，并惩罚非主动手指的接触力。随后，它从终止抓取状态训练第二阶段策略，并用课程学习保留每个后续任务中表现最好的抓取候选。

改进在消融实验中最清楚。HANDFUL 在仿真中报告的成功率为：Push Object 69.90%，Press Button 77.75%，Twist Knob 61.52%，Pull Drawer 78.94%，Pick Second 76.54%。去掉手指约束后，Pick Second 降到 0.00%，其他几个任务也下降。课程学习把第二阶段训练从 9000 万步降到 5400 万步，同时保持了相近的最终成功率。

#### Evidence
- [HANDFUL: Sequential Grasp-Conditioned Dexterous Manipulation with Resource Awareness](../Inbox/2026-04-28--handful-sequential-grasp-conditioned-dexterous-manipulation-with-resource-awareness.md): Summary gives the sequential task setup, resource-aware reward, curriculum, and simulation results.
