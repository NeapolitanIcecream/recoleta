---
source: arxiv
url: https://arxiv.org/abs/2605.07381v1
published_at: '2026-05-08T07:35:24'
authors:
- Yanzhe Chen
- Kevin Yuchen Ma
- Qi Lv
- Yiqi Lin
- Zechen Bai
- Chen Gao
- Mike Zheng Shou
topics:
- vision-language-action
- robot-adaptation
- data-efficient-learning
- real-robot-manipulation
- active-data-collection
- low-rank-adaptation
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Escaping the Diversity Trap in Robotic Manipulation via Anchor-Centric Adaptation

## Summary
## 摘要
ACA 通过先在选定锚点条件下重复收集演示，再加入有针对性的边界数据，提升了低预算真实机器人 VLA 适配效果。

## 问题
- 真实机器人演示成本高，因此把预训练 VLA 适配到新机器人时，通常只有几十到几百条轨迹。
- 论文认为，在小预算下，为许多不同条件各收集一次演示可能失败，因为每个条件的数据太少，会留下较高的动作估计噪声。
- 这会影响机器人部署，因为在存在具身差异和工作空间变化的物理任务中，稀疏覆盖可能让策略不稳定。

## 方法
- 论文把适配建模为学习条件动作向量场，并把误差拆分为估计项和覆盖项。
- 在 N 条轨迹和 K 个唯一条件下，简化界为 Cσ√(K/N) + LcK^(-1/d)，因此增加唯一条件会降低覆盖误差，但会提高估计误差。
- ACA 先在一小组工作空间锚点上用重复演示进行训练，得到稳定的基础策略。
- 随后，它在探测演示上运行教师强制偏差评分，选择误差最高的边界条件，并收集局部边界数据。
- 第 2 阶段冻结第 1 阶段策略，并在 Action Expert 中训练 LoRA 残差分支，因此可以加入边界修正，避免全参数漂移。

## 结果
- 在一台 7-DoF Franka Panda 和 4 个桌面任务上，ACA 在 Block Stacking、Cup Placement、Table Cleaning、Toy Tidying 中接受评估，覆盖 S@1、S@2、S@3 区域。
- 当 N=50 条轨迹时，π0.5 + ACA 的平均成功率达到 46.3%，而 π0.5 为 13.8%，提升 +32.5 个百分点。
- 当 N=100 条轨迹时，π0.5 + ACA 的平均成功率达到 72.5%，而 π0.5 为 31.7%，提升 +40.8 个百分点。
- 当 N=150 条轨迹时，π0.5 + ACA 的平均成功率达到 83.8%，而 π0.5 为 52.9%，提升 +30.9 个百分点。
- 论文报告每个任务-区域设置使用 20 次评估 rollout；S@1 覆盖 25% 的工作空间，S@2 覆盖 50%，S@3 覆盖 90%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07381v1](https://arxiv.org/abs/2605.07381v1)
