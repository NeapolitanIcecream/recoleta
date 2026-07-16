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

# 机器人研究更明确地讨论记忆与机制

## 概览
这一天的论文数量不多，但信号很清楚：机器人论文正在把内部状态和物理约束讲得更明白。Dual-Anchoring 通过在 Video-LLM 内部监督进度和地标记忆，提升了长时程导航。MM-Hand 在硬件上做了同样的事，量化远程腱路由带来的力和延迟代价，同时保持机械手更轻、更模块化，也更容易加传感器。

## 研究发现

### State tracking in vision-language navigation
Dual-Anchoring 让长时程视觉-语言导航的任务状态更明确。核心思路很简单：强制模型说明哪些指令子目标已经完成，并强制它保留对已到达地标的记忆。这个监督规模很大，有 360 万条进度样本和 93.7 万条带地标标注的样本。在连续环境 VLN 基准上，报告的提升很明显：R2R-CE 的成功率达到 65.6，RxR-CE 达到 61.7，比 StreamVLN 约高出 8.7 和 8.8 个百分点。在这个小周期里，这让记忆和进度跟踪成为最清楚的算法结果。

#### 资料来源
- [Dual-Anchoring: Addressing State Drift in Vision-Language Navigation](../Inbox/2026-04-19--dual-anchoring-addressing-state-drift-in-vision-language-navigation.md): Summary of the method, datasets, and benchmark gains.

### Remote-actuated dexterous hand design
MM-Hand 关注灵巧操作里的硬件可用性。它是一只 21 自由度的开源机械手，采用远程腱驱动、模块化 3D 打印结构、快速腱连接器，并为手内加入更丰富的传感留下空间。工程取舍是明确量化的：1 米套管的指尖力为 25 N，而 0.1 米套管约为 33 N；控制器仍能把稳态关节误差控制在 0.1° 以下，延迟约 0.2 秒。论文还报告，在跟踪测试里，摩擦的影响比机械臂运动扰动更大。这让这项工作更像一个研究平台论文，而不只是概念演示。

#### 资料来源
- [MM-Hand: A 21-DOF Multi-modal Modular Dexterous Robotic Hand with Remote Actuation](../Inbox/2026-04-19--mm-hand-a-21-dof-multi-modal-modular-dexterous-robotic-hand-with-remote-actuation.md): Summary of the hand design, sensing stack, and main quantitative results.
