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
## 摘要
T³VF 为视觉前瞻 VLA 模型加入测试时训练，使模型在部署时视觉条件变化的情况下能够适应。它用预测未来图像与随后观测图像之间的差距作为监督信号，再用动作方差筛选更新。

## 问题
- 视觉前瞻 VLA 模型先预测未来视觉状态，再基于该预测生成动作，因此分布外视觉变化会同时损害图像预测和动作生成。
- 论文针对 LIBERO-Plus 扰动，包括机器人状态、语言、噪声、布局、背景、相机和光照变化。
- 这一点很重要，因为即使基础模型在同分布 LIBERO 任务上表现良好，VF-VLA 在部署变化下的成功率也可能下降。

## 方法
- 在步骤 `t`，模型预测未来观测 `ô_{t+n}` 并执行一个动作。经过 `n` 步后，环境给出实际观测 `o_{t+n}`。
- T³VF 将 `(ô_{t+n}, o_{t+n})` 作为自监督训练对，并使用训练时相同的图像损失来更新图像预测路径。
- 更新只改变可学习查询 token `q`；VLM 主干、图像头和动作头保持冻结。
- 为避免噪声更新，该方法采样 `K=5` 个动作，计算它们的 L2 平方方差，并且只有当方差位于近期缓冲区较低的 `ρ=0.3` 分位数内时才接受更新。
- 报告的超参数为预测间隔 `n=4`、批大小 `B=4`、方差缓冲区大小 `10`、动作采样数 `K=5` 和百分位阈值 `ρ=0.3`。

## 结果
- 在带扰动训练的 LIBERO-Plus 上，Mantis + T³VF 的平均成功率达到 `52.1%`，Mantis 为 `49.3%`，提升 `+2.8` 个百分点，相对提升约 `+5.7%`。
- 在同一设置下，列出的最大增益为 Camera `55.3%` 对 `50.5%`（`+4.8` 点）、Light `72.4%` 对 `67.8%`（`+4.6` 点）、Background `63.0%` 对 `60.3%`（`+2.7` 点）和 Layout `44.9%` 对 `42.3%`（`+2.6` 点）。
- 在没有扰动训练的情况下，T³VF 带来的提升较小：平均成功率为 `40.3%`，Mantis 为 `39.8%`，即 `+0.5` 点。
- Robot 扰动消融报告中，Mantis 为 `29.0%`，未筛选的测试时训练为 `29.8%`，固定方差阈值为 `28.6%`，完整自适应缓冲区为 `31.8%`。
- 在 Robot 扰动上的运行时间约为 T³VF 基础每回合时间的 `1.3×`，未筛选测试时训练约为 `1.7×`。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08215v1](https://arxiv.org/abs/2605.08215v1)
