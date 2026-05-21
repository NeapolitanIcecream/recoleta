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
TRAP 通过改变触发观测对想象轨迹的排序来攻击世界模型规划器。论文报告称，TRAP 在 DreamerV3 和 TD-MPC2 上使用部署时视觉补丁实现了高攻击成功率，且不需要训练时投毒或参数修改。

## 问题
- 世界模型通过给大量想象未来打分来选择动作，因此针对一步预测或策略输出的浅层后门攻击可能被规划过程抵消。
- 改变顶部候选轨迹排序的视觉触发器可以重定向长时程行为，同时干净输入下的表现大多保持正常。
- 这关系到机器人、自动驾驶和其他规划控制场景，因为受损的规划器可能在触发器出现后持续做出错误决策。

## 方法
- 攻击者对白盒访问目标世界模型，并在推理时在有界扰动预算下优化一个通用视觉补丁。
- 对每个干净观测和触发观测，模型会想象候选轨迹，并计算两种条件下的分数变化。
- TRAP 选择干净规划下的高分尾部，因为这些轨迹会驱动动作选择。
- 尾部感知排序损失会压低这些被选中轨迹的分数，并用跨候选轨迹的 softmin 聚合来聚焦难以压低的轨迹。
- 两个门控控制优化：符号门控惩罚分数上升，幅度门控惩罚低于边界 beta 的过度压制。

## 结果
- 在补丁比例 0.09、epsilon 64 下，TRAP 在 DreamerV3 Crafter 上达到 98.1 ± 0.8% ASR 和 63.2 ± 0.9% 平均回报下降；随机补丁基线为 43.9 ± 8.4% ASR 和 -0.1 ± 3.5% 平均下降。
- 在 DreamerV3 DMControl 上，TRAP 报告 humanoid-walk 的下降为 69.8 ± 0.7%、ASR 为 100.0 ± 0.0%，cheetah-run 为 22.8 ± 2.3% 和 99.6 ± 0.5%，walker-walk 为 18.5 ± 1.5% 和 100.0 ± 0.0%，dog-run 为 9.8 ± 3.8% 和 77.2 ± 3.7%。
- 在 DreamerV3 Atari 上，TRAP 报告 seaquest、pong、breakout 和 invaders 的 ASR 均为 100.0 ± 0.0%，平均回报下降分别为 97.5 ± 0.8%、164.5 ± 8.3%、98.8 ± 0.7% 和 93.3 ± 1.8%。
- 在 TD-MPC2 DMControl 上，TRAP 报告 hopper-hop、cheetah-run 和 walker-walk 的 ASR 均为 100.0 ± 0.0%，平均回报下降分别为 99.8 ± 0.3%、98.4 ± 0.4% 和 92.4 ± 0.9%。
- 在 TD-MPC2 walker-walk 上，相比随机补丁基线的 1.9 ± 3.2% 下降和 64.0 ± 2.5% ASR，TRAP 提升到 92.4 ± 0.9% 下降和 100.0 ± 0.0% ASR。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01950v1](https://arxiv.org/abs/2605.01950v1)
