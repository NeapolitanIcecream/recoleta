---
source: arxiv
url: http://arxiv.org/abs/2603.07949v2
published_at: '2026-03-09T04:30:57'
authors:
- Zihao Zheng
- Sicheng Tian
- Hangyu Cao
- Chenyue Li
- Jiayu Chen
- Maoliang Li
- Xinhao Sun
- Hailong Zou
- Guojie Luo
- Xiang Chen
topics:
- edge-cloud-inference
- vision-language-action
- embodied-ai
- robotics-systems
- dynamic-offloading
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# RAPID: Redundancy-Aware and Compatibility-Optimal Edge-Cloud Partitioned Inference for Diverse VLA Models

## Summary
RAPID 是一种面向视觉-语言-动作（VLA）模型的边云协同推理框架，用机器人运动学/动力学信号而不是视觉置信度来决定何时把推理卸载到云端。它试图同时解决视觉噪声下的分区不稳和 embodied 任务中动作阶段冗余被忽略的问题，从而提升实时性与兼容性。

## Problem
- VLA 模型参数大、推理慢，直接在边缘设备运行难以满足机器人控制的实时要求。
- 现有动态边云分区多依赖视觉特征或动作熵，容易被视觉噪声、遮挡和环境变化干扰，跨环境兼容性差。
- 现有方法忽略 embodied 任务中的逐步动作冗余：大量“平稳接近”动作并不重要，若频繁打断或卸载，会浪费算力并破坏动作连续性。

## Approach
- 用**关节瞬时加速度**表示“兼容性/异常运动变化”：当机器人高速运动中出现急停、转向、避障等非线性变化时，说明更可能需要云端重新规划。
- 用**关节力矩变化**表示“冗余度/关键交互”：平滑接近阶段力矩变化小、动作冗余高，接触/抓取/操作阶段力矩突变大、动作冗余低，更值得卸载到云端。
- 对这两类信号分别做滑动窗口归一化，得到异常分数；再依据当前关节速度动态分配权重：高速时更信任加速度，低速交互时更信任力矩。
- 通过双阈值触发器决定是否卸载，并配合异步多速率处理、动作抢占和冷却机制，避免频繁网络请求和动作中断。
- 核心思想可概括为：**机器人自己身体的运动/受力变化，比画面是否“看起来不确定”更适合决定边云分工。**

## Results
- 论文声称，相比 Edge-Only VLA 和 vision-based 基线（文中提到 ISAR/表中 SAFE），RAPID 可将**准确率最高提升 15.8%**，并实现**最高 1.73× 推理加速**，系统额外开销仅 **5\~7%**。
- 在仿真基准上，RAPID 的总延迟为 **222.9 ± 11.4 ms**，优于 vision-based SAFE 的 **377.7 ± 26.2 ms**，约快 **1.69×**；也优于 Edge-Only 的 **782.5 ± 28.5 ms**，约快 **3.51×**。
- 资源分配上，RAPID 将边侧负载降到 **2.4GB**，低于 SAFE 的 **4.7GB** 和 Edge-Only 的 **14.2GB**；对应边侧延迟 **139.4 ms**，显著低于 SAFE 的 **315.2 ms**。
- 视觉基线在噪声下明显退化：总延迟从标准环境的 **395.4 ms** 上升到视觉噪声下 **520.6 ms**，在干扰场景进一步升到 **685.3 ms**，支持作者“视觉驱动分区易受噪声影响”的论点。
- 动作冗余分析显示，冗余动作占比超过 **80%**：Pick & Place **82.5%**、Drawer Opening **86.4%**、Peg Insertion **81.2%**；这些冗余动作的平均注意力权重仅 **0.005–0.008**，而关键动作为 **0.058–0.076**。这为“边端处理冗余阶段、云端处理关键阶段”的设计提供了依据。

## Link
- [http://arxiv.org/abs/2603.07949v2](http://arxiv.org/abs/2603.07949v2)
