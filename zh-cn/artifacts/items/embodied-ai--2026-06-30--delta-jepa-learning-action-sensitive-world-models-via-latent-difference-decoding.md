---
source: arxiv
url: https://arxiv.org/abs/2606.31232v1
published_at: '2026-06-30T07:08:24'
authors:
- Zhenghao Zhang
- Yuanxiang Wang
- Zhenyu Guan
- Yujia Yang
- Bingkang Shi
- Tianyu Zong
- Hongzhu Yi
- Guoqing Chao
- Xingchen Chen
- Tiankun Yang
- Chenxi Bao
- Tao Yu
- Jingjing Zhou
- Jungang Xu
topics:
- world-model
- latent-dynamics
- visual-control
- robot-manipulation
- planning
- representation-learning
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding

## Summary
## 摘要
Delta-JEPA 是一种用于视觉连续控制规划的无重构潜在世界模型。它的核心做法是从两个潜在状态之间的变化解码已执行动作，从而推动潜在动力学保留动作效果。

## 问题
- JEPA 风格的潜在世界模型如果只用潜在预测损失训练，可能坍缩为近似常量的嵌入，因此低损失可能掩盖无法用于规划的状态。
- 像素重构会增加计算量，也可能把模型容量用在对控制无帮助的视觉细节上。
- 规划需要潜在 rollout，其中不同候选动作会产生不同的预测状态。

## 方法
- 编码器将图像映射为潜在状态，动力学预测器根据当前潜在状态和连续动作预测下一个潜在状态。
- Latent Difference Action Decoder 计算 Δz = z_{t+1} - z_t，并从该位移重构已执行动作。
- 模型用两个损失进行端到端训练：潜在下一状态均方误差和动作重构均方误差，并由 λ 加权。
- 多步版本使用一个小型 Transformer 和 N 个学习到的动作查询，从 z_{t+N} - z_t 解码长度为 N 的动作序列。
- 该方法避免了像素重构、冻结编码器、stop-gradient 分支和分布匹配正则项。

## 结果
- 在 3 个种子的规划成功率上，Delta-JEPA 在全部 4 个任务中表现最好：Two-Room 100.00±0.00、Reacher 81.33±0.50、Push-T 89.07±1.90、OGB-Cube 79.27±1.81。
- 相比每个任务中最强的基线，它在 Two-Room 上比 PLDM 93.73±1.03 高 +6.27 点，在 Reacher 上比 Sub-JEPA 81.00±2.40 高 +0.33 点，在 Push-T 上比 LeWM 84.53±1.50 高 +4.54 点，在 OGB-Cube 上比 LeWM 64.13±1.89 高 +15.14 点。
- 位移解码器在全部 4 个任务中都优于端点拼接动作解码：Two-Room 高 +4.07 点，Reacher 高 +1.07 点，Push-T 高 +12.60 点，OGB-Cube 高 +0.67 点。
- 在 Reacher 目标消融中，解码原始动作效果最好，为 81.33±0.50；相比之下，Δ finger position 为 64.93±1.10，Δ joint position 为 80.47±2.10，两种 delta 同时使用为 76.40±1.40。
- Push-T 的 λ 消融报告显示，λ=0 时接近坍缩，λ=0.1 时性能较弱，中等范围的 λ 值带来更稳定、更高的规划成功率，最佳结果出现在 λ=50.0。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.31232v1](https://arxiv.org/abs/2606.31232v1)
