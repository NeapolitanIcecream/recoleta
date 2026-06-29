---
source: arxiv
url: http://arxiv.org/abs/2604.20472v1
published_at: '2026-04-22T11:58:05'
authors:
- Shelly Francis-Meretzki
- Mirco Mutti
- Yaniv Romano
- Aviv Tamar
topics:
- vision-language-action
- uncertainty-calibration
- temporal-difference-learning
- robot-failure-detection
- sequential-decision-making
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Temporal Difference Calibration in Sequential Tasks: Application to Vision-Language-Action Models

## Summary
## 总结
本文为成功只在一个 episode 结束时才知道的序列任务定义了校准问题，然后证明最佳校准预测器就是策略的价值函数。它用时序差分学习来训练 vision-language-action 模型的这个预测器，并在仿真和真实机器人数据上报告了比现有方法更好的校准和失败检测。

## 问题
- 标准校准方法适用于单步预测问题，但机器人 episode 的标签是延迟的：任务要到一连串动作结束后才知道成功还是失败。
- 对 VLA 策略来说，动作级置信度未必能反映 rollout 的成功，因为有些不确定动作与最终结果无关。
- 可靠的成功置信度对安全、早期失败检测，以及通过 API 使用黑盒基础模型都很重要，因为内部特征可能不可见。

## 方法
- 论文定义了**序列 Brier 分数**：在时间步 \(t\)，预测整个 episode 最终成功的概率，然后用最终的二元成功标签来评估这个预测。
- 它证明，对于二元 episode 成功，序列 Brier 目标的风险最小化解与策略的期望未来回报，也就是价值函数，一致。
- 基于这个联系，它用**时序差分校准（TDQC）**训练成功预测器：每一步的预测被拉向下一步的预测，最后一步与 episode 成功标签对齐。
- 这种方法既可以使用 VLA 的内部特征（白盒），也可以只用策略随时间变化的动作概率（黑盒）；在隐藏状态不可用时这一点很重要。
- 论文把 TDQC 与先前工作中使用的交叉熵或蒙特卡洛式训练方法进行了比较，例如 SAFE。

## 结果
- 论文声称，在图 1 展示的所有基准和模型设置下，基于 TD 的方法在未见验证任务上都**稳定优于**常规二元交叉熵预测器，指标是按**时间分位数**统计、并在**21 个随机种子**上取平均的**序列 Brier 分数**。
- 它声称，只用**动作概率**训练的 TDQC 可以**匹配或优于**使用内部隐藏特征的 SAFE 风格预测器，这对黑盒 VLA API 很重要。摘要没有给出精确的 Brier 数值。
- 它报告了在 **LIBERO** 上针对 **OpenVLA、π0、π0-FAST 和 UniVLA** 的**最先进早期检测**结果，也报告了用 **π0-FAST** 收集的 **Franka 真实机器人数据集**上的结果。摘要把这些结果放在表 2，但没有给出数值。
- 作为策略改进的副产物，用学到的价值预测器对采样动作排序，让 **OpenVLA 在 LIBERO 上的成功率提升了 15%**。
- 摘要还给出一个更大的背景：以往报告中，未见任务上的 VLA 成功率常在 **30% 到 60%** 之间，这说明更好的成功预测很有用；但这些数字是背景，不是本文 TDQC 的提升幅度。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.20472v1](http://arxiv.org/abs/2604.20472v1)
