---
source: arxiv
url: https://arxiv.org/abs/2605.08215v1
published_at: '2026-05-06T11:21:25'
authors:
- Sangwu Park
- Wonjoong Kim
- Yeonjun In
- Sein Kim
- Hongseok Kang
- Chanyoung Park
topics:
- vision-language-action
- test-time-training
- visual-foresight
- out-of-distribution
- robot-manipulation
- libero-plus
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Test-Time Training for Visual Foresight Vision-Language-Action Models

## Summary
## 总结
T³VF 为 Visual Foresight VLA 模型加入测试时训练，使它们在部署时视觉条件发生变化时也能适应。它把预测的未来图像和之后观察到的图像之间的差异当作监督信号，再用动作方差过滤更新。

## 问题
- Visual Foresight VLA 模型先预测未来的视觉状态，再基于这个预测生成动作，所以分布外视觉变化会同时损害图像预测和动作生成。
- 这篇论文针对 LIBERO-Plus 中的扰动，包括机器人状态、语言、噪声、布局、背景、相机和光照变化。
- 这很重要，因为即使基础模型在分布内的 LIBERO 任务上表现良好，VF-VLA 在部署时遇到变化后也可能掉点。

## 方法
- 在步骤 `t`，模型预测未来观测 `ô_{t+n}` 并执行一个动作。经过 `n` 步后，环境给出实际观测 `o_{t+n}`。
- T³VF 将 `(ô_{t+n}, o_{t+n})` 视为自监督训练对，并用训练时相同的图像损失来更新图像预测路径。
- 这次更新只改动可学习查询 token `q`；VLM 主干、图像头和动作头都保持冻结。
- 为了避免噪声更新，该方法采样 `K=5` 个动作，计算它们的平方 L2 方差，只在方差落入最近缓冲区下 `ρ=0.3` 分位时接受更新。
- 文中给出的超参数是预测间隔 `n=4`、批大小 `B=4`、方差缓冲区大小 `10`、动作采样数 `K=5` 和百分位阈值 `ρ=0.3`。

## 结果
- 在带扰动训练的 LIBERO-Plus 上，Mantis + T³VF 的平均成功率达到 `52.1%`，Mantis 为 `49.3%`，提升 `+2.8` 个百分点，约 `+5.7%` 相对提升。
- 在同一设置下，表中最大的提升来自 Camera：`55.3%` 对 `50.5%`（`+4.8` 点）；Light：`72.4%` 对 `67.8%`（`+4.6` 点）；Background：`63.0%` 对 `60.3%`（`+2.7` 点）；Layout：`44.9%` 对 `42.3%`（`+2.6` 点）。
- 在没有扰动训练时，T³VF 的提升更小：平均成功率 `40.3%` 对 `39.8%`，即 `+0.5` 点。
- Robot 扰动的消融结果显示，Mantis 为 `29.0%`，未过滤的测试时训练为 `29.8%`，固定方差阈值为 `28.6%`，完整的自适应缓冲区为 `31.8%`。
- 在 Robot 扰动上，T³VF 的运行时间大约是基础每回合时间的 `1.3×`，而未过滤的测试时训练大约是 `1.7×`。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08215v1](https://arxiv.org/abs/2605.08215v1)
