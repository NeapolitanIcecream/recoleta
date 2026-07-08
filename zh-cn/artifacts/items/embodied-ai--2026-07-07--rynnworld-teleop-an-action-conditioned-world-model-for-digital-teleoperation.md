---
source: arxiv
url: https://arxiv.org/abs/2607.06558v1
published_at: '2026-07-07T17:58:11'
authors:
- Haoyu Zhao
- Xingyue Zhao
- Hangyu Li
- Biao Gong
- Kehan Li
- Siteng Huang
- Xin Li
- Deli Zhao
- Zhongyu Li
topics:
- action-conditioned-world-model
- digital-teleoperation
- robot-data-scaling
- sim2real
- dexterous-manipulation
- imitation-learning
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation

## Summary
## 概要
RynnWorld-Teleop 声称，机器人示教可以通过实时、动作条件化的视频世界模型来采集，无需使用实体机器人。它把操作员手部姿态转换为生成的机器人第一视角视频，并生成对齐的机器人动作，用于模仿学习。

## 问题
- 机器人学习需要大量、多样的轨迹数据，但实体遥操作会把每次示教绑定到机器人硬件、工作空间布置、物体可用性和人工复位。
- 现有的人到机器人视频转换能生成看起来像机器人的视频，但无法恢复机器人动作，因此不能产生完整的状态-动作训练数据。
- 现有的动作条件化第一视角世界模型仍以人为中心，因此无法弥合机器人策略训练中的视觉差距和动作差距。

## 方法
- 操作员提供手部姿态流。RynnWorld-Teleop 以该姿态流和一张参考图像为条件，生成以机器人为中心的第一视角视频。
- 手部姿态被渲染为 21 关节、带深度信息的骨架视频，其中关节颜色和大小编码相机空间深度，然后由 VAE 将其映射到视频潜在空间。
- Wan2.2-TI2V-5B 视频 Diffusion Transformer 增加了独立的姿态 patch-embedding 分支，并使用分布对齐和可学习门控来控制姿态。
- 训练先使用人类第一视角视频进行预训练，然后在成对的人类-机器人遥操作数据上进行机器人域适配。
- 因果学生模型从双向教师模型蒸馏而来，使用流式自回归生成、KV 缓存、4 步采样，以及用于长 rollout 的分块重新锚定。

## 结果
- 蒸馏后的模型可在一块 NVIDIA H100 GPU 上以 40+ FPS 进行交互式生成。
- 训练数据包括 VITRA 的 30.7M 帧和 1.23M 个切片、EgoDex 的 74.0M 帧和 0.91M 个切片，以及作者的机器人数据的 0.43M 帧和 5.3K 个切片。
- 机器人域数据包含 4 项任务的 1,800 个真实世界示教 episode：500 个 Dual Picking、500 个 Block Pushing、500 个 Bimanual Lifting，以及 300 个 Lid Placement。
- 生成的策略数据集将 RGB 帧与 54 维机器人动作配对，覆盖双 7-DoF 机械臂和双 20-DoF 灵巧手。
- 论文声称，仅用生成数据训练的策略可在灵巧双臂任务中实现 zero-shot Sim2Real transfer，并且向真实数据集加入生成数据会提高成功率。摘录未提供实际成功率数值或基线表。
- 该数据流水线以 16 FPS 合成骨架条件化视频，并在长时域生成中使用 81 帧分块进行重新锚定。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.06558v1](https://arxiv.org/abs/2607.06558v1)
