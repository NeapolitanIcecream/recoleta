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
## 总结
ACA 通过先在选定的锚点条件上重复示范，再加入有针对性的边界数据，改进了低预算真实机器人 VLA 自适应。

## 问题
- 真实机器人的示范成本很高，所以把一个预训练 VLA 适配到新机器人时，往往只有几十到几百条轨迹可用。
- 论文认为，在预算很小的时候，为很多不同条件各采一条示范会失败，因为每个条件的数据太少，会留下很高的动作估计噪声。
- 这会影响机器人部署，因为在具身不匹配和工作空间变化下，稀疏覆盖会让策略在物理任务中不稳定。

## 方法
- 论文把自适应建模为学习一个条件动作向量场，并把误差分成估计项和覆盖项。
- 在有 N 条轨迹和 K 个唯一条件时，简化界写成 Cσ√(K/N) + LcK^(-1/d)，所以增加唯一条件会降低覆盖误差，但会提高估计误差。
- ACA 先在少量工作空间锚点上用重复示范训练，形成一个稳定的基础策略。
- 然后，它对探测示范做 teacher-forced 偏差打分，选出误差最高的边界条件，并采集局部边界数据。
- 第二阶段冻结第一阶段策略，并在 Action Expert 中训练一个 LoRA 残差分支，把边界修正加进去，同时避免完整参数漂移。

## 结果
- 在 7 自由度 Franka Panda 和 4 个桌面任务上，ACA 评估了 Block Stacking、Cup Placement、Table Cleaning 和 Toy Tidying，在 S@1、S@2 和 S@3 区域中进行比较。
- 当 N=50 条轨迹时，π0.5 + ACA 的平均成功率达到 46.3%，而 π0.5 为 13.8%，提高了 32.5 个百分点。
- 当 N=100 条轨迹时，π0.5 + ACA 的平均成功率达到 72.5%，而 π0.5 为 31.7%，提高了 40.8 个百分点。
- 当 N=150 条轨迹时，π0.5 + ACA 的平均成功率达到 83.8%，而 π0.5 为 52.9%，提高了 30.9 个百分点。
- 论文报告每个任务-区域设置做 20 次评估 rollout；S@1 覆盖工作空间的 25%，S@2 覆盖 50%，S@3 覆盖 90%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07381v1](https://arxiv.org/abs/2605.07381v1)
