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
DriveVA 是一个驾驶世界模型，它基于预训练视频生成器，同时生成未来视频和自车轨迹。论文声称，这种视频与动作联合建模提高了闭环驾驶表现，也让模型在不同数据集和领域之间的迁移更好，而且不需要在目标域微调。

## 问题
- 自动驾驶模型在未见过的道路、交通模式、传感器配置和领域偏移下经常失效，这会阻碍实际部署。
- 以往的世界模型规划器通常把未来视觉和未来动作分开预测，或者只用弱连接的模块，所以规划出的轨迹容易和想象中的场景脱节。
- 视觉语言预训练主要来自静态图文数据，能提供语义知识，但在按时间进行规划时，运动和因果先验更弱。

## 方法
- DriveVA 以最近的相机历史、自车速度和语言指令为条件，然后在一个共享的生成过程中同时预测一小段未来的视频潜变量和动作 token。
- 该模型使用预训练的 Wan2.2 视频 VAE 和文本编码器，然后由一个单一的 DiT 解码器通过条件流匹配联合生成未来视频潜变量和轨迹 token。
- 动作用三维 token 表示未来自车位姿 `(x, y, yaw)`，并与未来视频 token 一起训练，这样轨迹就能和生成出的场景演化保持一致。
- 视频续接策略会从历史缓冲区递归地滚动生成短片段，用来保持更长时间范围内预测的一致性。
- 论文报告说，稠密视频监督是规划提升的主要来源：加入视频监督后，NAVSIMv1 的 PDMS 从 71.4 提高到 90.9，比只优化动作高出 19.5 分。

## 结果
- 在 NAVSIM v1 上，DriveVA 的闭环评估达到 **90.9 PDMS**。在表格中，这一结果高于 DiffusionDrive 的 **88.1**、ReCogDrive-IL 的 **86.5**、Epona 的 **86.2** 和 LAW 的 **84.6**。
- 在从 NAVSIM 训练集到 **nuScenes** 的零样本跨数据集迁移中，DriveVA 相比论文所述的当前最优世界模型规划器，将 **平均 L2 误差降低 78.9%**，将 **碰撞率降低 83.3%**。
- 在从 NAVSIM 到 **Bench2Drive / CARLA v2** 的零样本真机到仿真迁移中，它相对同类基线将 **平均 L2 误差降低 52.5%**，将 **碰撞率降低 52.4%**。
- 该模型是生成式模型，但论文指出，**2 步采样** 已经能带来接近最优的闭环表现。
- 论文最强的结论是，推动规划提升和零样本迁移收益的是视频与动作的联合生成，而不是只做动作预测。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04198v1](http://arxiv.org/abs/2604.04198v1)
