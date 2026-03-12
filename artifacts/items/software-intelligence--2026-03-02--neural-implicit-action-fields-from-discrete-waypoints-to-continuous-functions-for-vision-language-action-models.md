---
source: arxiv
url: http://arxiv.org/abs/2603.01766v1
published_at: '2026-03-02T11:48:24'
authors:
- Haoyun Liu
- Jianzhuang Zhao
- Xinyuan Chang
- Tianle Shi
- Chuanzhang Meng
- Jiayuan Tan
- Feng Xiong
- Tong Lin
- Dongjie Huo
- Mu Xu
- SongLin Dong
- Zhiheng Ma
- Yihong Gong
- Sheng Zhong
topics:
- vision-language-action
- robot-manipulation
- implicit-neural-representation
- continuous-control
- siren
- impedance-control
relevance_score: 0.38
run_id: materialize-outputs
---

# Neural Implicit Action Fields: From Discrete Waypoints to Continuous Functions for Vision-Language-Action Models

## Summary
这篇论文提出 NIAF，把机器人动作从“预测一串离散路点”改成“预测一个连续时间函数”，以更贴合真实物理运动。核心价值是同时提升轨迹分辨率无关性、可微性和控制平滑性，从而让视觉-语言-动作模型更适合精细操控与阻抗控制。

## Problem
- 现有 VLA 常把动作表示为固定采样率下的离散路点或压缩控制点，但真实机器人运动本质上是连续的。
- 离散表示会带来量化误差、固定频率约束，以及速度/加速度/jerk 等高阶动态难以一致监督的问题，导致抖动和控制不稳定。
- 这很重要，因为精细接触、顺应控制、动态执行都依赖平滑且物理一致的连续轨迹，而不仅是位置点序列。

## Approach
- 将动作块表示为连续函数 \(\mathcal{A}(\tau)=\Phi(\tau;\theta)\)，模型不再直接输出 waypoint，而是回归定义整段轨迹的函数参数。
- 使用多模态大语言模型作为超网络/分层频谱调制器，根据图像、语言和状态上下文生成调制向量，去调制一个共享的 SIREN 运动先验。
- 采用 SIREN 隐式神经表示来保证轨迹具有解析可导性与理论上的无限平滑，从而可在任意控制频率下查询动作。
- 利用解析导数直接监督速度、加速度和 jerk，并把解析速度送入阻抗控制律，避免离散方法依赖数值微分带来的噪声。

## Results
- **CALVIN, ABCD→D**：NIAF 在 **0.77B、无机器人大规模预训练** 条件下达到 **Avg. Len 4.66**，优于 **BEAST 4.61**、**FLOWER 4.62**，也高于 **UniVLA 4.63 (9B, 有预训练)**。
- **CALVIN, ABCD→D**：连续完成 **1/2/3** 个任务成功率分别为 **0.997/0.978/0.946**，高于 **BEAST 0.981/0.962/0.930**；但 **5-task** 为 **0.839**，低于 **FLOWER 0.855** 和 **BEAST 0.848**。
- **CALVIN, ABC→D**：NIAF 达到 **Avg. Len 4.47**，优于 **FLOWER 4.44**、**BEAST 4.42**、**UniVLA 4.41**。其 **4-task/5-task** 成功率为 **0.848/0.764**，高于 **BEAST 0.827/0.744** 与 **FLOWER 0.823/0.755**。
- 论文声称在 **CALVIN 和 LIBERO** 上达到 SOTA，并且可扩展到从 **Florence-2 到 Qwen3-VL** 的不同骨干，但给定摘录中的 **LIBERO 表格被截断**，因此无法完整核对全部数值。
- 真实机器人实验声称 NIAF 可减少离散基线中的控制抖动、支持稳定阻抗控制，并改善精细动态任务表现；但摘录中 **未提供真实世界定量指标**，只有这些具体定性主张。"

## Link
- [http://arxiv.org/abs/2603.01766v1](http://arxiv.org/abs/2603.01766v1)
