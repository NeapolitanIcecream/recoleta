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

# 机器人学习正在收紧视觉仿真与接触执行之间的连接

## Overview
当天的机器人学信号集中在物理执行上。GS-Playground 面向带接触物理的高吞吐量照片级真实训练，HANDFUL 则在多步骤灵巧任务中把手指视为稀缺资源。两篇论文都关注让学习到的机器人策略在首次接触后仍可用的条件。

## Clusters

### 用于接触密集策略训练的照片级真实仿真
GS-Playground 将并行物理引擎与批处理 3D Gaussian Splatting (3DGS) 连接起来。3DGS 是一种用于照片级真实场景重建的渲染方法。目标是在不牺牲强化学习所需仿真规模的情况下，让视觉输入接近真实相机数据。

论文报告的数字是关键信号。论文称，在 RTX 4090 级别配置上，640×480 分辨率下的 3DGS 渲染约为 10,000 FPS；在该分辨率下最多支持 2048 个渲染场景，并列出最多 4096 个 3DGS 环境。其剪枝步骤移除超过 90% 的 Gaussians，同时将 PSNR 损失控制在 0.05 以下。该仿真器还将 Gaussian 资产绑定到刚体上，因此渲染对象会在接触过程中随物理状态移动。

这对机器人学习有意义，因为接触密集的操作、导航和运动既需要大量试验，也需要有用的图像。Real2Sim 流水线补上了另一个实用环节：它把 RGB 采集转换为资产、网格、位姿、尺度和可用于碰撞的场景元素，减少通常构建仿真场景所需的人工工作。

#### Evidence
- [GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning](../Inbox/2026-04-28--gs-playground-a-high-throughput-photorealistic-simulator-for-vision-informed-robot-learning.md): 摘要给出了仿真器目标、3DGS 与物理设计、Real2Sim 流水线，以及核心吞吐量和剪枝指标。

### 序列灵巧操作中的手指分配
HANDFUL 研究机器人手中的一种常见失败模式：稳定的首次抓取可能占用下一步动作所需的手指或接触区域。该设置要求 LEAP Hand 握住一个物体，然后在保持初始抓取的同时，推动、按压、扭转、拉动或拾取另一个物体。

该方法为首次抓取分配手指，并保留其他手指可用。它的奖励鼓励主动手指接触，并惩罚非主动手指上的接触力。随后，它从终端抓取状态训练第二阶段策略，并用课程学习保留最适合每个后续任务的抓取候选。

收益在消融实验中最清楚。HANDFUL 报告称，在仿真中，Push Object 成功率为 69.90%，Press Button 为 77.75%，Twist Knob 为 61.52%，Pull Drawer 为 78.94%，Pick Second 为 76.54%。移除手指约束后，Pick Second 降至 0.00%，其他几个任务也下降。课程学习在保持相近最终成功率的同时，将第二阶段训练从 9000 万步减少到 5400 万步。

#### Evidence
- [HANDFUL: Sequential Grasp-Conditioned Dexterous Manipulation with Resource Awareness](../Inbox/2026-04-28--handful-sequential-grasp-conditioned-dexterous-manipulation-with-resource-awareness.md): 摘要给出了序列任务设置、资源感知奖励、课程学习和仿真结果。
