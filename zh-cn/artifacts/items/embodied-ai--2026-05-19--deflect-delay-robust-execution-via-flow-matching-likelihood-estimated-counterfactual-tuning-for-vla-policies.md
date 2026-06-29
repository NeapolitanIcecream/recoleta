---
source: arxiv
url: https://arxiv.org/abs/2605.19294v1
published_at: '2026-05-19T03:14:11'
authors:
- Yixiang Zhu
- Yonghao Chen
- Rui Meng
- Jingyu Guo
- Jiaxiang Zou
- Zijie Yang
- Taowen Wang
- Xinyu Chen
topics:
- vision-language-action
- asynchronous-inference
- flow-matching
- preference-optimization
- robot-manipulation
- delay-robust-control
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# DEFLECT: Delay-Robust Execution via Flow-matching Likelihood-Estimated Counterfactual Tuning for VLA Policies

## Summary
## 摘要
DEFLECT 是一种针对 flow-matching VLA 策略的离线后训练方法，用来改善存在推理延迟时的异步机器人控制。它从新鲜观测和过时观测构造偏好对，并训练策略偏向与执行时状态一致的动作。

## 问题
- 异步 VLA 部署会在模型计算下一段动作时执行旧的动作块，因此新的动作块可能基于已经落后几个控制步的场景。
- 这会影响移动或反应型任务：在 Kinetix 上，当推理延迟达到 7 个控制步时，朴素异步回滚的成功率从 89% 降到 1% 以下。
- 监督微调不会把与新鲜状态一致的动作排在与过时状态一致的动作之前，而 flow-matching 策略又没有可用于标准 DPO 的解析动作似然。

## 方法
- DEFLECT 使用离线轨迹，并采样一个延迟 d，训练延迟最高到 d_max=4。
- 一个冻结的 VLASH 参考策略用共享采样噪声生成两个动作块：A+ 来自 t+d 时刻的新鲜上下文，A- 来自 t 时刻的过时上下文。
- 这两个动作块都在部署时的混合上下文下打分，该上下文使用向前滚动后的本体感觉和过时视觉，与异步运行时输入一致。
- 论文把负的 flow-matching 损失当作隐式对数似然替代项，然后施加带参考校准的 DPO 损失，并在专家动作块上加一个 SFT 锚点。
- 部署时使用与基础策略相同的 ODE 推理，没有额外运行时开销。

## 结果
- Kinetix：DEFLECT 在 d=0-7 的平均成功率达到 83.3%，VLASH 为 79.4%，PFM 为 78.4%，RTC 为 48.9%，BID 为 46.7%，朴素异步为 42.4%。
- Kinetix 高延迟区间 d=5-7，在训练中未见过：DEFLECT 的平均成功率为 73.5%，VLASH 为 67.1%，PFM 为 65.5%，分别高出 +6.4 和 +8.0 个百分点。
- Kinetix 高延迟基线会崩溃：在 d=5-7 时，朴素异步平均成功率为 1.5%，RTC 为 2.0%，BID 为 2.0%。
- LIBERO 上使用 pi_0.5 规模的 VLA：DEFLECT 在每个延迟下都优于 VLASH，在 d=7、经过 200 步微调后提升 4.6 个百分点。
- 真实机器人，每个任务 N=30：Conveyor-I 上，pi_0.5 和 DEFLECT 的完整任务成功率都是 96.7%，VLASH 为 86.7%；Conveyor-II 上，DEFLECT 为 90.0%，VLASH 为 83.3%，pi_0.5 为 46.7%。
- 真实 Whack-a-Mole，N=30：DEFLECT 每 30 秒试验击中 13.6 个地鼠，VLASH 为 10.4 个，pi_0.5 为 8.9 个。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.19294v1](https://arxiv.org/abs/2605.19294v1)
