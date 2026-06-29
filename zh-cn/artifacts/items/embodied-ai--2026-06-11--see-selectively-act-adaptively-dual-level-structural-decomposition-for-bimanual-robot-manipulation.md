---
source: arxiv
url: https://arxiv.org/abs/2606.13279v1
published_at: '2026-06-11T12:33:55'
authors:
- Yoon-Ji Choi
- Young-Chae Son
- Soo-Chul Lim
topics:
- bimanual-manipulation
- vision-language-action
- mixture-of-experts
- visual-routing
- robot-learning
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# See Selectively, Act Adaptively: Dual-Level Structural Decomposition for Bimanual Robot Manipulation

## Summary
## 摘要
本文处理双臂操作中的失败问题，这些失败来自任务阶段中视觉相关性和双臂协作方式的变化。它加入了显式路由来决定看什么、怎么行动，并报告在仿真和真实任务上相对单体 VLA 基线有大幅提升。

## 问题
- 双臂任务会随着任务进展在独立运动和协同运动之间切换。
- 有用的腕部相机视角也会随阶段变化，因此单一共享策略可能把无关视觉线索和任务关键线索混在一起。
- 单体 Vision-Language-Action 策略没有把视图相关性和交互模式分开，这会影响鲁棒性和泛化。

## 方法
- 以预训练 VLA 策略为基础，加入两个模块。
- 使用 View-Selective Visual Router，按当前任务上下文重新加权左右腕部视图 token。
- 使用 Interaction-Aware Action Mixture-of-Experts，在协同动作专家和按手臂动作专家之间进行选择。
- 用基于 KNN 的半自动流程生成监督标签来训练路由器，并联合优化主 flow-matching 动作损失和路由器损失。

## 结果
- 在六个 RoboTwin 2.0 仿真任务上，完整模型的平均成功率达到 69.6%，单体基线为 41.9%，去掉 IAMoE 的变体为 54.3%，去掉 VSR 的变体为 59.7%。
- 在仿真中，它比单体基线的平均提升了 27.7 个百分点。
- 在三个长时程真实任务的实测评估中，它比单体基线的整体平均成功率高 43.3 个百分点。
- 在困难设置的仿真评估中，它比基线平均高 35.7 个百分点。
- 在真实世界的困难评估中，它在 R1、R2 和 R3 上分别比基线高 30%、40% 和 50%。
- 在复杂仿真任务 S5 和 S6 上，在简单设置中把两个模块结合起来，相比两个单模块变体分别提升 13.4% 和 6.7%；在困难设置中分别提升 17.3% 和 13.2%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.13279v1](https://arxiv.org/abs/2606.13279v1)
