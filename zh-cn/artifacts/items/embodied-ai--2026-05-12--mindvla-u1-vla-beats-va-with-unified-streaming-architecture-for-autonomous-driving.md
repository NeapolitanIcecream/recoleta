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
## 摘要
MindVLA-U1 是用于自动驾驶的流式视觉-语言-动作模型，在一个共享 VLM 骨干网络中保留离散语言输出和连续车辆轨迹。论文称，它在 WOD-E2E 上的规划效果优于此前的 VA 和 VLA 系统，同时保持接近 VA 的延迟。

## 问题
- 自动驾驶 VLA 模型的表现常常落后于视觉到动作规划器，因为语言 token、时间上下文和连续控制之间的接口较弱。
- 离散轨迹 token 会限制控制精度，独立的动作头会削弱 VLM 推理与轨迹生成之间的耦合。
- 分块的视频-动作规划会增加时间建模成本，并可能在块之间产生不连续，这会影响长尾驾驶事件。

## 方法
- 模型在一次前向传播中，通过一个 VLM 骨干网络处理视觉、自车状态、语言、记忆和带噪动作 token。
- 语言使用自回归 token 预测；动作使用流匹配生成连续航点轨迹。
- FIFO 流式记忆存储压缩后的历史帧特征，将其对齐到当前自车姿态，并在每帧后更新。
- 预测出的驾驶意图 token 通过 classifier-free guidance 条件化动作扩散，让语言以可测量的路径进入轨迹生成。
- 注意力掩码支持快慢两种模式，包括仅动作推理和先语言后动作推理，且来自同一个 checkpoint。

## 结果
- 在 WOD-E2E 上，MindVLA-U1 使用 2 个扩散步骤，声称达到 8.20 RFS，高于有经验人类驾驶员的 8.13 GT RFS。
- 论文报告，在约 1B 参数规模下速度约为 16 FPS；相比之下，RAP 在匹配的约 1B 规模下约为 18 FPS。
- 论文称，其规划 ADE 相比此前 VA 和 VLA 方法达到 state-of-the-art，但摘录未给出 ADE 数值。
- WOD-E2E 包含 4,021 个约 20 秒的驾驶片段，其中有 2,037 个训练序列和 479 个验证序列，数据来自 8 摄像头 360 度设备。
- MindLabel 增加了约 3.8M 个 VQA 对和约 250K 条生成轨迹，覆盖约 18.8K 个片段；不过报告的实验只使用基础场景 VQA 和官方意图标签。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12624v2](https://arxiv.org/abs/2605.12624v2)
