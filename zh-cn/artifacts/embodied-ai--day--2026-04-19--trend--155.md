---
kind: trend
trend_doc_id: 155
granularity: day
period_start: '2026-04-19T00:00:00'
period_end: '2026-04-20T00:00:00'
topics:
- robotics
- vision-language navigation
- dexterous manipulation
- memory
- hardware design
run_id: materialize-outputs
aliases:
- recoleta-trend-155
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-navigation
- topic/dexterous-manipulation
- topic/memory
- topic/hardware-design
language_code: zh-CN
---

# 机器人研究更明确地处理记忆与机制

## Overview
这一天的论文不多，但信号很清楚：机器人论文开始更明确地处理内部状态和物理约束。Dual-Anchoring 通过在 Video-LLM 内监督进度和地标记忆，提升了长时程导航。MM-Hand 在硬件上也做了类似的事：它量化了远程肌腱布线带来的力和延迟代价，同时让机械手更轻、更模块化，也更适合加入传感器。

## Clusters

### 视觉-语言导航中的状态跟踪
Dual-Anchoring让长时程视觉-语言导航更明确地处理任务状态。核心思路很直接：让模型说明哪些指令子目标已经完成，并让它保留自己经过位置的地标级记忆。这种监督规模很大，包括 3.6M 条进度样本和 937K 条有落地对应的地标样本。论文在连续环境 VLN 基准上的提升很明显：R2R-CE 的成功率达到 65.6，RxR-CE 达到 61.7，相比 StreamVLN 分别提高约 +8.7 和 +8.8 个点。在这个时间段里，这让记忆与进度跟踪成为最清楚的算法结果。

#### Evidence
- [Dual-Anchoring: Addressing State Drift in Vision-Language Navigation](../Inbox/2026-04-19--dual-anchoring-addressing-state-drift-in-vision-language-navigation.md): 方法、数据集和基准提升的总结。

### 远程驱动的灵巧手设计
MM-Hand强调灵巧操作中的硬件实用性。它是一只 21-DOF 的开源机械手，采用远程肌腱驱动、模块化 3D 打印结构、快速肌腱连接器，并为手内更丰富的传感留出了空间。工程上的取舍被直接量化出来：1 m 软管可提供 25 N 指尖力，而 0.1 m 软管约为 33 N；控制器在约 0.2 s 延迟下，稳态关节误差仍低于 0.1°。论文还报告，在其跟踪测试中，摩擦的影响大于机械臂运动扰动。这让这项工作更像一篇有用的研究平台论文，而不只是概念演示。

#### Evidence
- [MM-Hand: A 21-DOF Multi-modal Modular Dexterous Robotic Hand with Remote Actuation](../Inbox/2026-04-19--mm-hand-a-21-dof-multi-modal-modular-dexterous-robotic-hand-with-remote-actuation.md): 机械手设计、传感栈和主要定量结果的总结。
