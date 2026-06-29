---
source: arxiv
url: https://arxiv.org/abs/2605.14398v1
published_at: '2026-05-14T05:33:41'
authors:
- Hongyu Wang
- Jingquan Wang
- Bocheng Zou
- Radu Serban
- Dan Negrut
topics:
- world-model
- physics-simulation
- agentic-code-generation
- embodied-simulation
- robot-simulation
- video-world-models
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Coding Agent Is Good As World Simulator

## Summary
## 摘要
论文声称，编码代理可以通过编写和修复可执行的 PyChrono 仿真代码来构建基于物理的世界模型。它的主要价值，是用能暴露物体、关节、接触、传感器和求解器诊断信息的模拟器状态，替代仅依赖视频的滚动生成。

## 问题
- 视频世界模型可以生成看起来合理的帧，但会丢失物理状态，导致长序列滚动时接触不稳定、形状失真和运动不一致。
- 手工搭建物理仿真需要熟悉模拟器、选择资产、设置碰撞、编写代码、调参和目视检查。
- 这会影响具身智能体、机器人任务、车辆以及流固相互作用，因为控制和评估依赖可执行动力学，而不只是外观。

## 方法
- 系统把文本提示，加上可选的参考图像，转换成结构化仿真计划，包含物体、空间关系、物理角色、实现步骤和相机设置。
- 编码代理使用技能库、资产库、确定性工具和按版本整理的 API 索引编写 PyChrono 代码。
- 生成的程序在 Project Chrono 中运行，并输出日志、轨迹、渲染帧和视频。
- 视觉审查代理检查渲染视频中的物体、布局、运动、接触，以及与计划不一致的地方。
- 仿真判定器结合日志、轨迹数据和视觉审查结果，再把具体错误报告发回去，反复修补同一段程序。

## 结果
- 在报告的三个任务上，计划生成的 Pass@1、Pass@3 和 Pass@5 都达到 100%：Outdoor vehicle、FSI vehicle 和 Robot in office，在仅文本输入和文本加图像输入下都一样。
- 代表性的成功运行分别花了 24 分钟、30 分钟和 28 分钟，对应 Outdoor vehicle、FSI vehicle 和 Robot in office。
- 令牌使用量很高：Outdoor vehicle 共 1.68e+06 个 token，FSI vehicle 为 3.24e+06，Robot in office 为 6.34e+06。
- 在 WorldModelBench 的场景级总分上，系统在 Vehicle FSI 上比 Wan2.2-TI2V-5B 高 1.70 分，6.80±1.03 对 5.10±0.99，p=0.0012。
- Outdoor vehicle 提高 0.30 分，5.80±1.14 对 5.50±1.08，p=0.5203；Robot in office 提高 0.80 分，6.90±0.57 对 6.10±1.10，p=0.0528。
- 按指标汇总后，指令得分提高 2.40 分，5.90±0.57 对 3.50±0.85，p=0.000059；物理定律得分提高 0.40，p=0.5086；常识得分持平，2.30 对 2.30，p=1.0000。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14398v1](https://arxiv.org/abs/2605.14398v1)
