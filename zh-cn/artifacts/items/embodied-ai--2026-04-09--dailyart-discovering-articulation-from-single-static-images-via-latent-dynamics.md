---
source: arxiv
url: http://arxiv.org/abs/2604.07758v1
published_at: '2026-04-09T03:24:07'
authors:
- Hang Zhang
- Qijian Tian
- Jingyu Gong
- Daoguo Dong
- Xuhong Wang
- Yuan Xie
- Xin Tan
topics:
- articulated-object-understanding
- single-image-reconstruction
- kinematic-joint-estimation
- novel-view-synthesis
- embodied-ai
relevance_score: 0.81
run_id: materialize-outputs
language_code: zh-CN
---

# DailyArt: Discovering Articulation from Single Static Images via Latent Dynamics

## Summary
## 摘要
DailyArt 先生成物体的张开版本，再根据闭合态和张开态之间的差异来估计单张静态图像中的关节。论文面向仅依赖图像的推断，在测试时不需要部件掩码、CAD 检索或人工关节提示。

## 问题
- 任务是从一张闭合状态图像中恢复一个具有关节的物体的关节类型、轴、支点和运动范围。
- 这对具身 AI 和世界模型很重要，因为机器人需要明确的运动学结构来预测和操控物体，而闭合图像常常遮住用来推断这种结构的运动线索。
- 以往方法在测试时通常需要额外输入，例如多状态观测、视频、掩码、部件图、检索候选项或物体模板。

## 方法
- DailyArt 把单图关节推断变成一个双状态推理问题，先在相同相机视角下合成同一物体的最大张开视图。
- 第一阶段使用冻结的 DINOv2 图像编码器和一个学习得到的 VAE 风格解码器。模型通过 AdaLN 注入标量状态变量 `t`，从闭合图像生成张开状态。
- 第二阶段使用 VGGT 将输入图像和合成的张开图像映射为稠密的 3D 点图，计算跨状态的 3D 运动种子，用置信度和位移启发式规则过滤后，再用集合预测 Transformer 一次性预测所有关节。
- 关节预测在训练时使用匈牙利匹配，输出关节类型、支点原点、轴方向和运动范围，关节槽上限为 `K=16`。
- 第三阶段把估计出的关节送回合成模型，使其可以在给定某个关节和目标运动值 `t'` 时生成部件级的新状态。

## 结果
- 摘要只说明 DailyArt 在关节估计和部件级新状态合成上表现良好，但没有给出基准表、数据集名称或最终定量分数。
- 该方法声称测试时只依赖图像，不需要物体专用模板、多视角输入、显式部件标注、掩码、图结构、提示词或预设部件数量。
- 模型在一次前向传播中预测完整关节集合，包括物体中心世界坐标系中的关节类型、支点原点、轴方向和运动边界。
- 第二阶段对 3D 点过滤使用 `0.85` 的置信度阈值，去掉位移种子中最短的 `15%` 和最长的 `20%`，并把关节槽上限设为 `16`。
- 训练时把运动范围归一化到 `[0,2]`，评估时把转动关节的数值从 `[-360°, 360°]` 映射过来。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.07758v1](http://arxiv.org/abs/2604.07758v1)
