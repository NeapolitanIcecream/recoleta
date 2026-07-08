---
source: arxiv
url: https://arxiv.org/abs/2607.06559v1
published_at: '2026-07-07T17:58:15'
authors:
- Haoyu Zhao
- Xingyue Zhao
- Siteng Huang
- Xin Li
- Deli Zhao
- Zhongyu Li
topics:
- embodied-world-model
- vision-language-action
- robot-manipulation
- 4d-scene-flow
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# RynnWorld-4D: 4D Embodied World Models for Robotic Manipulation

## Summary
## 概述
RynnWorld-4D 从一张 RGB-D 图像和一条文本指令预测未来的 RGB、深度和光流视频，然后使用模型隐藏的 4D 特征来选择机器人动作。论文面向一类操作任务：2D 视频预测会丢失精确机器人控制所需的深度和运动线索。

## 问题
- 机器人需要预测物体在接触过程中如何在 3D 中运动；仅使用 RGB 的视频模型可能漏掉深度、6-DoF 位姿和逐点运动。
- 现有 NeRF、3D Gaussian 和动态 SfM 方法通常需要多视角、针对特定场景的优化，或无法从单张图像生成未来状态。
- 这一差距会影响操作策略，因为策略必须输出底层动作，而深度或运动误差可能导致灵巧双臂任务失败。

## 方法
- 模型使用 RGB-DF：同步的 RGB 帧、深度图和光流。深度把像素提升为 3D 点，光流把这些点沿时间连接起来，形成 3D 场景流。
- RynnWorld-4D 将 Wan 视频扩散骨干扩展为三个分支，分别处理 RGB、深度和光流。
- Joint Cross-Modal Attention 被插入到 30 层中的每 3 个 transformer 块之后，总计 10 个联合模块，使每个模态都能在同一帧关注另外两个模态。
- 训练使用 Rynn4DDataset 1.0。该数据集由第一人称人类视频和机器人操作视频构建，并配有 Qwen3-VL 字幕、Depth Anything 3 深度伪标签和 DPFlow 光流伪标签。
- RynnWorld-4D-Policy 冻结世界模型，在一次前向传播中读取中间 RGB/深度/光流潜变量，用 Flow Former 对其压缩，并用 flow-matching 策略预测动作块。

## 结果
- Rynn4DDataset 1.0 包含来自 Epic-Kitchens、EgoVid、RoboMIND、RDT-1B、Galaxea、RoboCoin 和 AgiBot 的超过 2.544 亿帧。
- 模型同时预测 RGB、深度和光流；论文称，这些输出可以用针孔相机几何反投影为 3D 场景流。
- 策略推理路径报告，在配备 FP8 和 FlashAttention 3 的 NVIDIA RTX 5090 上总延迟为 1,106 ms：RynnWorld-4D 为 990 ms，深度估计为 85 ms，VAE 和潜变量准备为 18 ms，Flow Former 为 4 ms，动作头为 8 ms。
- 在每次传递 K=10 个动作块时，论文报告的规划频率约为 0.9 Hz，有效控制频率约为 9 Hz。
- 摘录声称该方法在真实世界灵巧双臂操作任务上达到 state-of-the-art 性能，尤其擅长空间精度和时间协调任务，但所示文本没有给出成功率或基准表。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.06559v1](https://arxiv.org/abs/2607.06559v1)
