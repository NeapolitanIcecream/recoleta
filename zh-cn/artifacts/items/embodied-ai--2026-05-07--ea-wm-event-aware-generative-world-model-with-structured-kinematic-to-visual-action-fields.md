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
EA-WM 通过把机器人动作转换为与相机对齐的视觉场，并使用带事件监督的融合来结合视频特征，改进机器人视频世界建模。论文称，该方法在 WorldArena 上生成的 rollout 更符合动作，尤其改善了机器人运动、接触和 3D 一致性。

## 问题
- 机器人视频世界模型常用低维关节向量或末端执行器向量作为生成条件，这些向量缺少足够的相机空间几何信息，难以准确渲染机器人运动。
- rollout 几何质量差、机器人与物体接触建模弱，会降低生成视频在规划、合成机器人数据和 VLA 策略评估中的价值。
- 现有 world-action 模型更关注用视频改进行动预测，对用动作改进未来视频合成关注较少。

## 方法
- EA-WM 将机器人关节状态、夹爪状态、末端执行器位姿和相机参数转换为 Structured Kinematic-to-Visual Action Fields，即 KVAFs。
- KVAFs 通过正向运动学和相机投影构建，然后在目标相机视角中渲染为带深度信息的机械臂骨架、关节标志点、夹爪几何、末端执行器热图和位姿坐标轴。
- 该模型使用 Wan2.2 video VAE 对 RGB 视频和 KVAFs 进行编码，然后在 diffusion-transformer 主干中分别通过视频分支和 KVAF 分支处理它们。
- 稀疏双向融合层通过交叉注意力在两个分支之间交换信息。
- Event-Difference Latent Supervision 将帧差视频编码为事件目标，再用这些目标训练事件门控，控制视频特征和 KVAF 特征在哪些位置交互。

## 结果
- 在 WorldArena 上，EA-WM 报告的 P3CScore 为 76.60；相比之下，列出的最强基线 CogVideoX 为 71.08，Wan2.2 为 60.83。
- EA-WM 将 Interaction Quality 提高到 0.682，而 CogVideoX 为 0.594；Trajectory Accuracy 提高到 0.430，而 CogVideoX 为 0.353。
- 它报告的 Depth Accuracy 为 0.959，而 CogVideoX 为 0.910；Perspectivity 为 0.838，而该指标上列出的最佳基线为 0.796。
- 它报告的 Instruction Following 为 0.792，而 CogVideoX 为 0.727；Semantic Alignment 为 0.895，略低于 CogVideoX 的列出最佳值 0.898。
- 在消融实验中，完整 EA-WM 的 P3CScore 为 76.60；去掉 KVAFs 后为 70.97，去掉 event-aware fusion 后为 74.80。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06192v1](https://arxiv.org/abs/2605.06192v1)
