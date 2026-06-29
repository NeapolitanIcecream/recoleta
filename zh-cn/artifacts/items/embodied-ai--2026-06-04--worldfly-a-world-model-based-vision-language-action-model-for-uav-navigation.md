---
source: arxiv
url: https://arxiv.org/abs/2606.06147v1
published_at: '2026-06-04T13:23:05'
authors:
- Shengtao Zheng
- Kai Li
- Weichen Zhang
- Yu Meng
- Chen Gao
- Xinlei Chen
- Yong Li
- Xiao-Ping Zhang
topics:
- uav-navigation
- vision-language-action
- world-model
- flow-matching
- simulated-benchmark
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# WorldFly: A World-Model-Based Vision-Language-Action Model for UAV Navigation

## Summary
## 概要
WorldFly 是一个用于无人机的视觉-语言-动作模型，会同时预测未来的摄像头视图和导航动作。在新的 Urban Canyon Traversal 基准上，它的成功率、路径效率和终点距离误差都优于 OpenFly 和 Pi-0-UAV。

## 问题
- 现有的无人机 VLA 策略通常把过去的第一视角图像和语言直接映射到动作；当建筑遮挡路线或急转弯导致视角大幅变化时，这种方法会失效。
- 这很重要，因为低空城市无人机需要沿着语言指令穿过路口和狭窄街道，包括训练中没有见过的布局。
- 论文还补上了一个基准空缺，构建了 Urban Canyon Traversal，包含长路线、大转弯和未见路口测试。

## 方法
- WorldFly 在语言指令和最近的第一视角观测条件下，联合建模未来动作片段和未来视频帧的分布。
- 一个世界模型分支预测未来视频潜变量，动作分支预测一个 8 维连续动作片段，并映射到 10 个离散的 OpenFly 导航原语。
- 两个分支使用相同的噪声时间步做 flow matching，因此未来视觉状态和动作在对齐的去噪条件下训练。
- 双分支耦合块在视频分支和动作分支之间使用交叉注意力，让计划中的动作条件化想象帧，也让想象帧条件化动作预测。
- 指令由 T5 编码，视频帧在进入 transformer 处理前先用 LTX-Video VAE 压缩。

## 结果
- Urban Canyon Traversal 包含 4,000 多条训练轨迹，构建于 AirSim 城市场景地图；另外还有 TEST-EASY，包含来自已见路口的 100 条轨迹，以及 TEST-HARD，包含来自 14 个新路口的 100 条轨迹。
- 在 TEST-EASY 上，WorldFly 的成功率为 87%，SPL 为 73.25%，导航误差为 7.92 米；OpenFly 分别为 72%、58.55% 和 14.69 米。
- 在 TEST-HARD 上，WorldFly 的成功率为 31%，SPL 为 27.86%，导航误差为 31.08 米；OpenFly 分别为 16%、14.92% 和 35.32 米。
- 与 TEST-HARD 上的 Pi-0-UAV 相比，WorldFly 将成功率从 10% 提升到 31%，将 SPL 从 9.43% 提升到 27.86%。
- 不使用双分支耦合的消融版本在 TEST-EASY 上得到 76% 成功率和 61.59% SPL，在 TEST-HARD 上得到 21% 成功率和 18.14% SPL；完整的 WorldFly 分别得到 87% 和 73.25%，以及 31% 和 27.86%。
- 论文报告，使用 50 步 flow-matching 去噪调度时，仅动作推理在一块 NVIDIA A100 上每步约需 7.81 秒。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.06147v1](https://arxiv.org/abs/2606.06147v1)
