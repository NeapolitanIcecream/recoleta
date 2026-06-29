---
source: arxiv
url: https://arxiv.org/abs/2606.03268v1
published_at: '2026-06-02T07:35:18'
authors:
- Qian Zhao
- Xin Tong
- Chengdong Wu
- Yang Yang
- Yingtian Li
topics:
- dexterous-manipulation
- low-cost-demonstrations
- cross-embodiment
- reinforcement-learning
- motion-retargeting
- contact-rewards
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# EaDex: A Cross-Embodiment Dexterous Manipulation Framework from Low-Cost Demonstrations

## Summary
## 摘要
EaDex 从单个 RGB-D 人体示范中训练双手灵巧操作策略，并将其迁移到多种机器人手形态上。它的主要收益来自：在策略学到稳定接触之后，降低对噪声示范的依赖。

## 问题
- 灵巧操作的控制空间很大，纯强化学习需要大量探索，而且常常无法收敛。
- 模仿学习可以减少探索，但高质量的灵巧手示范通常需要动作捕捉、遥操作硬件或精细标定。
- 这篇论文针对低成本示范，希望这些示范仍能为有铰接物体开启任务提供有用的接触和运动线索。

## 方法
- EaDex 使用一台 Intel RealSense D435i RGB-D 相机记录双手人体手部运动。
- 它用 MediaPipe 检测手部关键点，拟合 MANO 手部姿态参数，用高斯滤波平滑轨迹，并将数据保存为 ARCTIC 格式。
- 同一组人体示范会被重定向到三种灵巧手：Inspire Hand、Allegro Hand 和 XHand。
- 策略在 Genesis 中使用 PPO 训练，奖励包括任务奖励、模仿奖励、行为克隆奖励和接触奖励。
- 基于接触奖励的退火规则，只有在接触奖励和回合长度超过固定稳定阈值后，才降低模仿和行为克隆的权重。

## 结果
- 在自建的低成本数据集上，EaDex 评估了 3 种手 × 3 种有铰接物体，得到 9 种跨形态操作设置。
- 平均成功率从没有退火时的 23.5% 提高到有退火时的 36.5%，相对提升 55.3%。
- 自建数据集上的最佳任务成功率达到 93.3%。
- 评测任务包括盒子、华夫饼机和搅拌机开启；成功的定义是把物体保持在 0.2 m × 0.2 m × 0.1 m 的平台上，并让最终铰接角度超过 45°。
- 在使用 ADD-AUC3 的 ARCTIC Ability Hand 任务上，退火将 Ketchup 从 9.0 ± 0.6 提高到 57.91 ± 28.12，Waffleiron 从 9.1 ± 0.7 提高到 23.01 ± 0.65，Mixer 从 28.1 ± 7.4 提高到 35.14 ± 4.02。
- 作者报告，从示范采集到训练好的策略，某些完整流程在一块 RTX 3090 GPU 上大约 1 小时内完成。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.03268v1](https://arxiv.org/abs/2606.03268v1)
