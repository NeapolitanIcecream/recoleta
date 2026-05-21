---
source: arxiv
url: https://arxiv.org/abs/2605.17522v1
published_at: '2026-05-17T16:11:22'
authors:
- Sixu Lin
- Junliang Chen
- Huaiyuan Xu
- Zhuohao Li
- Guangming Wang
- Yixiong Jing
- Sheng Xu
- Runyi Zhao
- Brian Sheil
- Lap-Pui Chau
- Guiliang Liu
topics:
- robot-world-model
- flow-guided-manipulation
- vision-language-action
- 3d-motion-planning
- real-time-robot-control
- sim2real
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# RoboFlow4D: A Lightweight Flow World Model Toward Real-Time Flow-Guided Robotic Manipulation

## Summary
## 摘要
RoboFlow4D 从 RGB 图像和文本预测多帧 3D 夹爪流，并用这些流在闭环中引导机器人策略。它用一个轻量级扩散 Transformer 模型替代由多个模型组成的 3D 流流水线，目标是实现实时操作。

## 问题
- 2D 流规划器在图像空间中运行，因此会缺少无碰撞操作所需的深度和几何信息。
- 近期的 3D 流规划器通常串联视频生成、深度估计、定位和点跟踪模型，这会增加延迟和内存成本。
- 真实机器人需要低延迟规划，并能在任务执行过程中根据新观测更新。

## 方法
- RoboFlow4D 的输入包括近期 RGB 帧、可选的 2D 查询点集合，以及一条语言指令。
- DINOv2 和 SigLIP 对视觉和文本进行编码；3D Perceiver 通过与 VGGT 特征对齐来学习具备 3D 感知能力的特征。
- 名为 FlowDiT 的扩散 Transformer 对未来 3D 轨迹去噪，并输出形状为 `关键点 × 帧 × 3D 位置` 的多帧流。
- 动作策略同时接收常规状态输入和编码后的流计划，因此可以跟踪预测运动。
- 控制以慢快循环运行：RoboFlow4D 以较低频率规划原子任务轨迹，策略以较高频率执行动作块。

## 结果
- 在 LIBERO 上配合 Diffusion Policy 使用时，平均成功率从 78.9% 升至 85.1%，提升 +6.2 个百分点；各套件提升为 Spatial +8.2、Object +1.7、Goal +6.8、Long +8.0。
- 在 LIBERO 上配合 DiT 策略使用时，平均成功率从 83.7% 升至 87.7%，提升 +4.0 个百分点；各套件提升为 Spatial +6.0、Object +0.7、Goal +3.0、Long +6.4。
- 论文报告在 ManiSkill3 上平均提升 +11.0 个百分点，并显示在可见的 PushCube、PickCube 和 StackCube 表格行中，DP 的平均值从 12.3% 提高到 22.0%。
- 根据论文摘录，真实世界任务提升了 5 到 20 个百分点。
- 作者声称规划延迟低于 1 秒，相比模块化流流水线加速 120×，并且模型规模比其他流模型小 24% 以上。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17522v1](https://arxiv.org/abs/2605.17522v1)
