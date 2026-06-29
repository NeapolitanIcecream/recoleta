---
source: arxiv
url: https://arxiv.org/abs/2605.12624v2
published_at: '2026-05-12T18:09:42'
authors:
- Yuzhou Huang
- Benjin Zhu
- Hengtong Lu
- Victor Shea-Jay Huang
- Haiming Zhang
- Wei Chen
- Jifeng Dai
- Yan Xie
- Hongsheng Li
topics:
- autonomous-driving
- vision-language-action
- streaming-memory
- flow-matching
- trajectory-planning
- language-conditioned-control
relevance_score: 0.68
run_id: materialize-outputs
language_code: zh-CN
---

# MindVLA-U1: VLA Beats VA with Unified Streaming Architecture for Autonomous Driving

## Summary
## 概要
MindVLA-U1 是一个用于自动驾驶的流式视觉-语言-动作模型，在同一个共享的 VLM 主干里把语言输出保持为离散形式，把车辆轨迹保持为连续形式。它声称在 WOD-E2E 上的规划优于先前的 VA 和 VLA 系统，同时保持接近 VA 的延迟。

## 问题
- 驾驶 VLA 模型常常落后于 vision-to-action 规划器，因为语言 token、时间上下文和连续控制之间的接口不够强。
- 离散轨迹 token 会限制控制精度，而分开的动作头会削弱 VLM 推理和轨迹生成之间的耦合。
- 分块的视频-动作规划会增加时间成本，也可能让不同块之间出现不连续，这在长尾驾驶事件中很重要。

## 方法
- 该模型在一次前向过程中，通过一个 VLM 主干同时处理视觉、自车状态、语言、记忆和带噪动作 token。
- 语言使用自回归 token 预测；动作使用 flow matching 生成连续的 waypoints 轨迹。
- 一个 FIFO 流式记忆模块存储压缩后的历史帧特征，将它们对齐到当前自车位姿，并在每一帧后更新。
- 预测出的驾驶意图 token 通过 classifier-free guidance 约束动作扩散，把语言侧意图传入轨迹生成。
- 注意力掩码支持快、慢两种模式，包括仅动作推理和先语言后动作推理，都来自同一个 checkpoint。

## 结果
- 在 WOD-E2E 上，MindVLA-U1 声称用 2 个 diffusion steps 达到 8.20 RFS，高于经验丰富的人类司机的 8.13 GT RFS。
- 它报告在约 1B 参数规模下达到约 16 FPS，而 RAP 在匹配的约 1B 规模下约为 18 FPS。
- 论文声称在规划 ADE 上优于此前的 VA 和 VLA 方法，但摘要里没有给出 ADE 数值。
- WOD-E2E 包含 4,021 段约 20 秒的驾驶片段，其中 2,037 段用于训练，479 段用于验证，数据来自一套 8 摄像头的 360 度设备。
- MindLabel 增加了约 380 万个 VQA 对和约 25 万条 dreamed trajectories，覆盖约 1.88 万个 clips，但报告中的实验只使用了基础场景 VQA 和官方意图标签。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12624v2](https://arxiv.org/abs/2605.12624v2)
