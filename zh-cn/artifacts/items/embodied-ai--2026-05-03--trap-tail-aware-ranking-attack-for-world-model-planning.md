---
source: arxiv
url: https://arxiv.org/abs/2605.01950v1
published_at: '2026-05-03T16:19:45'
authors:
- Siyuan Duan
- Ke Zhang
- Xizhao Luo
topics:
- world-models
- backdoor-attacks
- trajectory-ranking
- reinforcement-learning-security
- visual-triggers
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# TRAP: Tail-aware Ranking Attack for World-Model Planning

## Summary
## 摘要
TRAP 通过改变触发观测下想象轨迹的排序来攻击世界模型规划器。它在 DreamerV3 和 TD-MPC2 上报告了很高的攻击成功率，使用的是部署时视觉补丁，没有训练时投毒或参数改动。

## 问题
- 世界模型通过对许多想象中的未来进行评分来选动作，所以针对单步预测或策略输出的浅层后门攻击，常会被规划过程抵消。
- 能改变候选轨迹前列排序的视觉触发器，可以在清洁输入大体正常的情况下改写长时程行为。
- 这会影响机器人、自动驾驶和其他规划式控制场景，因为一旦触发器出现，被攻陷的规划器还会继续做出错误决策。

## 方法
- 攻击者对目标世界模型有白盒访问权限，并在推理时在受限扰动预算下优化一个通用视觉补丁。
- 对每个干净观测和触发观测，模型都会想象候选轨迹，并计算两种条件下的分数变化。
- TRAP 先在干净规划下选取高分尾部，因为这些轨迹会驱动动作选择。
- 一个面向尾部的排序损失会压低这些被选中轨迹的分数，并用跨候选项的 softmin 聚合，把优化重点放在更难压低的轨迹上。
- 两个门控控制优化：符号门控对分数上升进行惩罚，幅度门控对低于阈值 beta 的过度压制进行惩罚。

## 结果
- 在 patch ratio 0.09 和 epsilon 64 下，TRAP 在 DreamerV3 Crafter 上达到 98.1 ± 0.8% 的 ASR 和 63.2 ± 0.9% 的平均回报下降；随机补丁基线的 ASR 为 43.9 ± 8.4%，平均下降为 -0.1 ± 3.5%。
- 在 DreamerV3 DMControl 上，TRAP 在 humanoid-walk 上报告 69.8 ± 0.7% 的下降和 100.0 ± 0.0% 的 ASR，在 cheetah-run 上报告 22.8 ± 2.3% 和 99.6 ± 0.5%，在 walker-walk 上报告 18.5 ± 1.5% 和 100.0 ± 0.0%，在 dog-run 上报告 9.8 ± 3.8% 和 77.2 ± 3.7%。
- 在 DreamerV3 Atari 上，TRAP 在 seaquest、pong、breakout 和 invaders 上都报告 100.0 ± 0.0% 的 ASR，对应的平均回报下降分别为 97.5 ± 0.8%、164.5 ± 8.3%、98.8 ± 0.7% 和 93.3 ± 1.8%。
- 在 TD-MPC2 DMControl 上，TRAP 在 hopper-hop、cheetah-run 和 walker-walk 上都报告 100.0 ± 0.0% 的 ASR，对应的平均回报下降分别为 99.8 ± 0.3%、98.4 ± 0.4% 和 92.4 ± 0.9%。
- 在 TD-MPC2 walker-walk 上，TRAP 相比随机补丁基线，把下降从 1.9 ± 3.2% 和 64.0 ± 2.5% 的 ASR 提高到 92.4 ± 0.9% 的下降和 100.0 ± 0.0% 的 ASR。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01950v1](https://arxiv.org/abs/2605.01950v1)
