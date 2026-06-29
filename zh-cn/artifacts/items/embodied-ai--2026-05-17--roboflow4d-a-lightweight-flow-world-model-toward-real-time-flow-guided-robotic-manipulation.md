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
RoboFlow4D 从 RGB 图像和文本预测多帧 3D 夹爪流，然后用这些流在闭环中指导机器人策略。它通过一个轻量级扩散 Transformer 模型取代多模型 3D 流管线，目标是实现实时操作。

## 问题
- 2D 流规划器在图像空间中工作，会遗漏无碰撞操作所需的深度和几何信息。
- 近期的 3D 流规划器常把视频生成、深度、定位和点跟踪模型串联起来，这会增加延迟和内存开销。
- 真实机器人需要低延迟规划，并且任务过程中能根据新观测及时更新。

## 方法
- RoboFlow4D 以最近的 RGB 帧、一个可选的 2D 查询点集合和一条语言指令作为输入。
- DINOv2 和 SigLIP 分别编码视觉和文本；3D Perceiver 通过与 VGGT 特征对齐来学习具备 3D 感知的特征。
- 一个名为 FlowDiT 的扩散 Transformer 对未来 3D 轨迹进行去噪，输出形状为 `keypoints × frames × 3D position` 的多帧流。
- 动作策略同时接收普通状态输入和编码后的流规划，因此可以跟踪预测的运动。
- 控制以慢快循环运行：RoboFlow4D 规划较低频率的原子任务轨迹，而策略执行较高频率的动作块。

## 结果
- 在 LIBERO 上使用 Diffusion Policy 时，平均成功率从 78.9% 提高到 85.1%，提升 6.2 个百分点；各子集提升分别为 Spatial +8.2、Object +1.7、Goal +6.8、Long +8.0。
- 在 LIBERO 上使用 DiT 策略时，平均成功率从 83.7% 提高到 87.7%，提升 4.0 个百分点；各子集提升分别为 Spatial +6.0、Object +0.7、Goal +3.0、Long +6.4。
- 论文报告在 ManiSkill3 上平均提升 11.0 个百分点，并展示了在可见的 PushCube、PickCube 和 StackCube 表格行上，DP 的平均成功率从 12.3% 提高到 22.0%。
- 根据论文摘要，真实世界任务提升了 5 到 20 个百分点。
- 作者声称规划延迟低于 1 秒，比模块化流管线快 120 倍，模型规模比其他流模型小 24% 以上。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17522v1](https://arxiv.org/abs/2605.17522v1)
