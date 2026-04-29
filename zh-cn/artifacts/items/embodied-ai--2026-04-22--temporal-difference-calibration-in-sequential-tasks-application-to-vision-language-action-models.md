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
## 摘要
这篇论文为序列任务定义了校准问题：任务是否成功只能在一个 episode 结束时知道；随后论文证明，校准最优的预测器就是策略的价值函数。论文用时序差分学习来训练 vision-language-action 模型的这个预测器，并报告称，在仿真和真实机器人数据上，它在校准和失败检测方面都优于现有方法。

## 问题
- 标准校准方法适用于单步预测问题，但机器人 episode 的标签是延迟的：任务成功或失败只有在一系列动作完成后才能确定。
- 对 VLA 策略来说，动作层面的置信度可能会误导对整段 rollout 是否成功的判断，因为有些不确定动作与最终结果无关。
- 可靠的成功置信度对安全、早期失败检测，以及通过 API 使用基础模型的黑盒场景都很重要，因为这些场景下内部特征可能不可见。

## 方法
- 论文定义了一个 **sequential Brier score**：在时间步 \(t\) 预测整个 episode 最终成功的概率，再用最终的二元成功标签对这个预测打分。
- 论文证明，对于二元 episodic success，这个 sequential Brier 目标的风险最小化解等同于策略的期望未来回报，也就是价值函数。
- 基于这个联系，论文用 **temporal-difference calibration (TDQC)** 训练成功预测器：每一步的预测会被推向下一步的预测，最后一步则与 episode 的成功标签对齐。
- 该方法既可以使用 VLA 的内部特征（white-box），也可以只使用策略随时间变化的动作概率（black-box）；当隐藏状态不可用时，这一点很重要。
- 论文将 TDQC 与此前工作（如 SAFE）使用的 cross-entropy 或 Monte Carlo 风格训练方法进行了比较。

## 结果
- 论文称，在 Figure 1 展示的所有基准和模型设置中，基于 TD 的方法在未见过的验证任务上都 **稳定优于** 常规的 binary-cross-entropy 预测器；评估指标是按 **time quantiles** 统计并在 **21 random seeds** 上平均的 **sequential Brier score**。
- 论文称，只使用 **action probabilities** 的 TDQC 也能 **达到或超过** 使用内部隐藏特征的 SAFE 风格预测器，这对黑盒 VLA API 很重要。摘录中没有给出确切的 Brier 数值。
- 论文报告了在 **LIBERO** 上针对 **OpenVLA, π0, π0-FAST, and UniVLA**，以及在使用 **π0-FAST** 收集的 **Franka real-robot dataset** 上的 **state-of-the-art early detection** 结果。摘录提到这些结果见 Table 2，但没有包含具体数值。
- 作为策略改进的附带效果，用学到的价值预测器对采样动作排序，使 **OpenVLA on LIBERO** 的成功率提高了 **15%**。
- 摘录还给出了一些背景：此前报告中，VLA 在未见任务上的成功率通常只有 **30% to 60%**。这说明更好的成功预测校准有实际价值，但这些数字是背景信息，不是这篇论文中 TDQC 带来的提升。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.20472v1](http://arxiv.org/abs/2604.20472v1)
