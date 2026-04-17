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
DailyArt 从一张静态图像估计可动关节，方法是先生成物体的打开版本，再根据闭合状态与打开状态之间的差异读取关节结构。论文面向纯图像推断，测试时不需要部件掩码、CAD 检索，也不需要人工提供关节提示。

## 问题
- 任务是从一张闭合状态图像中恢复可动物体的关节类型、轴、枢轴点和运动范围。
- 这对具身 AI 和世界模型很重要，因为机器人需要明确的运动学结构来预测和操作物体，而闭合图像常常会遮住推断这些结构所需的运动线索。
- 以往工作通常需要测试时额外输入，例如多个状态、视频、掩码、部件图、检索候选或物体模板。

## 方法
- DailyArt 将单图像可动结构推断改写成一个双状态推理问题：在相同相机视角下，先合成同一物体的最大打开视图。
- 第一阶段使用冻结的 DINOv2 图像编码器和一个学习得到的 VAE 风格解码器。模型通过 AdaLN 注入标量状态变量 `t`，从闭合图像生成打开状态。
- 第二阶段用 VGGT 将输入图像和合成的打开图像都转换为稠密 3D 点图，计算跨状态的 3D 运动种子，用置信度和位移启发式规则筛选，然后用集合预测 transformer 一次性预测所有关节。
- 关节预测在训练时使用 Hungarian matching，输出关节类型、枢轴原点、轴方向和运动范围，最多使用 `K=16` 个关节槽位。
- 第三阶段将估计得到的关节再输入合成模型，使其能够在指定关节和目标运动值 `t'` 的条件下生成部件级新状态。

## 结果
- 摘要称 DailyArt 在可动关节估计上表现很强，并支持基于关节条件的部件级新状态合成，但节选内容没有给出基准表、数据集名称或最终量化分数。
- 该方法声称测试时可用纯图像推断，不需要物体特定模板、多视图输入、显式部件标注、掩码、图结构、提示词或预先声明的部件数量。
- 模型在一次前向传播中预测完整关节集合，包括关节类型、枢轴原点、轴方向，以及以物体中心世界坐标表示的运动限制。
- 第二阶段对 3D 点筛选使用 `0.85` 的置信度阈值，去掉位移种子中最短的 `15%` 和最长的 `20%`，并将关节槽位上限设为 `16`。
- 训练时将运动范围归一化到 `[0,2]`，评估时将旋转关节的数值从 `[-360°, 360°]` 映射过来。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.07758v1](http://arxiv.org/abs/2604.07758v1)
