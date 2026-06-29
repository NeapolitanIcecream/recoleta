---
source: arxiv
url: https://arxiv.org/abs/2606.27344v1
published_at: '2026-06-25T17:50:07'
authors:
- Yuemin Mao
- Uksang Yoo
- Jean Oh
- Jonathan Francis
- Jeffrey Ichnowski
topics:
- dexterous-manipulation
- vibrotactile-sensing
- sim2real
- tactile-policy-learning
- contact-rich-manipulation
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# VibeAct: Vibration to Actions for Contact-Rich Reactive Robot Dexterity

## Summary
## 概要
VibeAct 使用压电式指尖麦克风，为在仿真中训练的灵巧机器人策略加入接触开始、是否滑移和滑移幅值反馈。它的主要结论是，这种小型触觉信号可以改善富接触手部控制，而且不需要仿真原始振动音频。

## 问题
- 灵巧手需要快速的接触和滑移反馈，因为关键事件发生在局部、持续时间短，并且常被摄像头遮挡。
- 原始振动声学信号很难仿真，因为它们受手指材料、安装方式、物体纹理、电子器件和电机噪声影响。
- 直接用真实触觉数据训练灵巧操作策略，需要大量真实世界数据，或者需要进行不安全的在线探索。

## 方法
- 机器人使用 8 个压电式麦克风，每个指尖 2 个，采样率为 48 kHz。
- 真实遥操作数据会在经过校准的 MuJoCo 数字克隆体中重放，用来标注一个 12 维触觉向量：每根手指的接触开始、二值滑移和滑移幅值。
- 触觉估计器使用每根手指独立的网络，将 200 ms 的 log-mel 麦克风窗口映射到该向量。
- PPO 策略在 MuJoCo 中训练，输入包括本体感知、固定摄像头点云和同一个 12 维触觉向量；部署时，由估计器提供触觉输入。

## 结果
- 触觉估计器，完整 VibeAct：在留出的移动物体划分上，接触开始 F1 为 0.597 ± 0.101，是否滑移 F1 为 0.913 ± 0.054，滑移幅值 MAE 为 4.736 ± 0.658 mm/s。
- 与仅预训练相比，完整 VibeAct 将接触开始 F1 从 0.384 提高到 0.597，将是否滑移 F1 从 0.781 提高到 0.913，并将滑移幅值 MAE 从 6.417 降低到 4.736 mm/s。
- 在仿真中，5 个任务、3 个种子下每个任务 100 次试验，完整 VibeAct 在所有任务上都超过本体感知加点云基线：Box Climb 50.0% vs 46.7%，Nut Rotation 44.0% vs 28.5%，Peg in Hole 30.0% vs 6.5%，Cube Rotation 57.0% vs 6.0%，Can Climb 76.0% vs 60.0%。
- 仿真中提升最大的是 Cube Rotation +51.0 个百分点和 Peg in Hole +23.5 个百分点，这两个任务都需要持续的触觉修正。
- 在硬件上，VibeAct 相比 Prop+PC 提高了成功次数：Box Climb 12/20 vs 4/20，Can Climb 19/20 vs 11/20，Nut Rotation 8/20 vs 1/20。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.27344v1](https://arxiv.org/abs/2606.27344v1)
