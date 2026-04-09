---
source: arxiv
url: http://arxiv.org/abs/2604.04198v1
published_at: '2026-04-05T17:43:16'
authors:
- Mengmeng Liu
- Diankun Zhang
- Jiuming Liu
- Jianfeng Cui
- Hongwei Xie
- Guang Chen
- Hangjun Ye
- Michael Ying Yang
- Francesco Nex
- Hao Cheng
topics:
- autonomous-driving
- world-model
- video-action-model
- zero-shot-generalization
- diffusion-transformer
relevance_score: 0.63
run_id: materialize-outputs
language_code: zh-CN
---

# DriveVA: Video Action Models are Zero-Shot Drivers

## Summary
## 摘要
DriveVA 是一个驾驶世界模型，它将未来视频和自车轨迹一起生成，并以预训练视频生成器为基础。论文称，这种联合视频-动作设定提升了闭环驾驶表现，并且在不进行目标域微调的情况下，能更好地迁移到不同数据集和领域。

## 问题
- 自动驾驶模型在未见过的道路、交通模式、传感器配置和域偏移下经常失效，这阻碍了真实部署。
- 以往的世界模型规划器通常把未来视觉和未来动作放在分离或联系较弱的模块中进行预测，因此规划轨迹可能偏离想象出的场景。
- 基于静态图文数据的视觉语言预训练提供了语义知识，但在随时间进行规划时，对运动和因果关系的先验较弱。

## 方法
- DriveVA 以近期相机历史、自车速度和语言指令为条件，在一个共享的生成过程中同时预测未来视频潜变量和动作 token 的短时 rollout。
- 模型使用预训练的 Wan2.2 视频 VAE 和文本编码器，再由一个单一的 DiT 解码器通过 conditional flow matching 联合生成未来视频潜变量和轨迹 token。
- 动作是表示未来自车位姿 `(x, y, yaw)` 的 3D token，与未来视频 token 一起训练，以保持轨迹与生成场景演化的一致。
- 一个视频续写策略会基于历史缓冲区递归地 rollout 短视频片段，目的是让更长时间范围的预测保持一致。
- 论文报告称，稠密视频监督是规划性能提升的主要来源：加入视频监督后，NAVSIMv1 PDMS 从 71.4 提升到 90.9，比只优化动作高出 19.5 分。

## 结果
- 在 NAVSIM v1 上，DriveVA 在闭环评估中达到 **90.9 PDMS**。在文中的表格里，这一结果高于 DiffusionDrive 的 **88.1**、ReCogDrive-IL 的 **86.5**、Epona 的 **86.2** 和 LAW 的 **84.6**。
- 在从 NAVSIM 训练到 **nuScenes** 的零样本跨数据集迁移中，相对于文中所述的当前最优世界模型规划器，DriveVA 将 **平均 L2 误差降低了 78.9%**，并将 **碰撞率降低了 83.3%**。
- 在从 NAVSIM 到 **Bench2Drive / CARLA v2** 的零样本 real-to-sim 迁移中，相比同类基线，它将 **平均 L2 误差降低了 52.5%**，并将 **碰撞率降低了 52.4%**。
- 该模型是生成式的，但论文称仅用 **2 个采样步数** 就已经得到接近最优的闭环表现。
- 论文最强的结论是，推动规划性能提升和零样本迁移增益的关键，是联合生成视频和动作，而不是单独预测动作。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04198v1](http://arxiv.org/abs/2604.04198v1)
