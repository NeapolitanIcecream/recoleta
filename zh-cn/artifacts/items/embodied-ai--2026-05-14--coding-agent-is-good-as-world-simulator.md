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
论文声称，编码智能体可以通过编写和修复可执行的 PyChrono 仿真代码来构建基于物理的世界模型。它的主要价值是用可检查仿真器状态替代仅视频的 rollout；这些状态可以暴露刚体、关节、接触、传感器和求解器诊断信息。

## 问题
- 视频世界模型可以生成看起来合理的画面，但会丢失物理状态，导致长 rollout 中出现接触不稳定、形状扭曲和运动不一致。
- 手工构建物理仿真需要仿真器知识、资产选择、碰撞设置、代码编写、参数调节和视觉检查。
- 这会影响具身智能体、机器人任务、车辆和流固耦合场景，因为控制和评估依赖可执行动力学，而不只依赖外观。

## 方法
- 系统把文本提示词和可选参考图像转换为结构化仿真计划，其中包含物体、空间关系、物理角色、实现步骤和相机设置。
- 编码智能体使用技能库、资产库、确定性工具和特定版本的 API 索引来编写 PyChrono 代码。
- 生成的程序在 Project Chrono 中运行，并产生日志、轨迹、渲染帧和视频。
- 视觉审查智能体检查渲染视频中的物体、布局、运动、接触，以及与计划不一致的地方。
- 仿真评审器结合日志、轨迹数据和视觉审查结果，然后把具体错误报告发回去，在多轮迭代中修补同一个程序。

## 结果
- 在报告的三个任务 Outdoor vehicle、FSI vehicle 和 Robot in office 上，无论输入是纯文本还是文本加图像，计划生成的 Pass@1、Pass@3 和 Pass@5 都达到 100%。
- 代表性成功运行耗时分别为：Outdoor vehicle 24 分钟，FSI vehicle 30 分钟，Robot in office 28 分钟。
- token 使用量很高：Outdoor vehicle 总计 1.68e+06 个 token，FSI vehicle 为 3.24e+06，Robot in office 为 6.34e+06。
- 在 WorldModelBench 场景级总分中，该系统在 Vehicle FSI 上比 Wan2.2-TI2V-5B 高 +1.70 分，6.80±1.03 对 5.10±0.99，p=0.0012。
- Outdoor vehicle 提高 +0.30 分，5.80±1.14 对 5.50±1.08，p=0.5203；Robot in office 提高 +0.80 分，6.90±0.57 对 6.10±1.10，p=0.0528。
- 按指标汇总后，指令得分提高 +2.40 分，5.90±0.57 对 3.50±0.85，p=0.000059；物理定律得分提高 +0.40，p=0.5086；常识得分持平，2.30 对 2.30，p=1.0000。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14398v1](https://arxiv.org/abs/2605.14398v1)
