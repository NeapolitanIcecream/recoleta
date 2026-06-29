---
source: arxiv
url: https://arxiv.org/abs/2605.06192v1
published_at: '2026-05-07T13:06:19'
authors:
- Zhaoyang Yang
- Yurun Jin
- Lizhe Qi
- Cong Huang
- Kai Chen
topics:
- robot-world-model
- video-diffusion
- action-conditioned-video
- kinematic-projection
- robot-data-scaling
- sim2real
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# EA-WM: Event-Aware Generative World Model with Structured Kinematic-to-Visual Action Fields

## Summary
## 摘要
EA-WM 通过把机器人动作转成与相机对齐的视觉场，并用事件监督的融合机制结合视频特征，改进了机器人视频世界建模。论文声称，在 WorldArena 上，它生成的轨迹与动作更一致，尤其是在机器人运动、接触和三维一致性方面。

## 问题
- 机器人视频世界模型通常用低维的关节或末端执行器向量来条件生成，这些向量提供的相机空间几何信息不足，难以准确渲染机器人的运动。
- 轨迹几何不准、机器人与物体接触建模弱，会降低生成视频在规划、合成机器人数据和 VLA 策略评估中的价值。
- 现有 world-action 模型更关注用视频改进动作预测，而不是用动作改进未来视频合成。

## 方法
- EA-WM 将机器人关节状态、夹爪状态、末端执行器位姿和相机参数转换为结构化运动到视觉动作场，简称 KVAF。
- KVAF 通过正向运动学和相机投影构建，再以带深度信息的机械臂骨架、关节标记点、夹爪几何、末端执行器热力图和位姿坐标轴的形式渲染到目标相机视图中。
- 模型使用 Wan2.2 video VAE 编码 RGB 视频和 KVAF，然后在扩散 Transformer 骨干中分别用视频分支和 KVAF 分支处理。
- 稀疏的双向融合层通过跨注意力在两个分支之间交换信息。
- 事件差分潜变量监督把帧差视频编码为事件目标，再用这些目标训练事件门控，控制视频特征和 KVAF 特征在哪里交互。

## 结果
- 在 WorldArena 上，EA-WM 的 P3CScore 为 76.60；对比之下，列出的最强基线 CogVideoX 为 71.08，Wan2.2 为 60.83。
- EA-WM 的 Interaction Quality 为 0.682，CogVideoX 为 0.594；Trajectory Accuracy 为 0.430，CogVideoX 为 0.353。
- 它的 Depth Accuracy 为 0.959，CogVideoX 为 0.910；Perspectivity 为 0.838，高于该指标上列出的最佳基线 0.796。
- 它的 Instruction Following 为 0.792，CogVideoX 为 0.727；Semantic Alignment 为 0.895，略低于 CogVideoX 的 0.898。
- 在消融实验中，完整 EA-WM 的 P3CScore 为 76.60；去掉 KVAF 后为 70.97，去掉事件感知融合后为 74.80。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06192v1](https://arxiv.org/abs/2605.06192v1)
