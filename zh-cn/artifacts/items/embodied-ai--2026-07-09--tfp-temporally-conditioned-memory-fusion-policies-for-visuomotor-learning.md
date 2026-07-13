---
source: arxiv
url: https://arxiv.org/abs/2607.08283v1
published_at: '2026-07-09T09:24:30'
authors:
- Yushen Liang
- Yue Peng
- Baosheng Jin
- Tianluo Zhang
- Xinyu Zhang
- Shuyi Zhou
- Zhuoran Chen
- Xinqi Liu
- Shenji Wan
topics:
- robot-foundation-model
- vision-language-action
- generalist-robot-policy
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# TFP: Temporally Conditioned Memory-Fusion Policies for Visuomotor Learning

## Summary
## 摘要
TFP 为一个 33 亿参数的 VLA 策略加入回合内连续时间记忆状态，使动作依据任务进度和经过的时间生成，而不只依赖当前观测。它提升了仿真基准和真实机器人分阶段操作任务的表现，在长时程、存在遮挡和视觉受到扰动的任务上提升最大。

## 问题
- 当视觉相似的场景在不同任务阶段需要不同动作时，反应式 VLA 策略可能选择错误动作。
- 遮挡、接触、释放以及不规则的策略查询间隔，使固定步长的记忆更新不可靠。
- 操作任务需要在含义不明确的观测期间保留任务进度，并在获得新的交互证据时更新信念状态，因此这个问题会直接影响任务完成。

## 方法
- TFP 维护一个 256 维的回合内潜在信念状态，用于概括任务进度和交互历史。
- 液态时间常数递归使用测得的经过时间和依赖输入的时间常数，决定保留或修正多少信念状态。
- 更新后的信念状态被投影到流匹配动作解码器中，并通过 AdaLN 调制注入，使记忆直接改变生成的动作块。
- 回合感知时间批处理在连续动作块上训练，同时为活动回合保留彼此独立的隐藏状态。
- 自适应滚动时域执行器会在夹爪状态切换或高风险区域附近缩短动作块，并将实际经过的时间间隔传递给记忆更新模块。

## 结果
- 在 LIBERO 上，TFP 的平均成功率为 98.75%，反应式 pi0.5 基线为 96.85%；在 Long-10 划分上，TFP 为 97.0%，基线为 92.4%。
- 在 LIBERO-plus 上，TFP 的平均成功率为 93.77%，pi0.5 为 91.4%。在噪声条件下，成功率从 85.2% 提升到 88.5%；在光照扰动条件下，从 93.9% 提升到 96.1%。
- 在 MIKASA-Robo ShellGameTouch 上，TFP 的成功率为 75.0%，高于已报告的 OpenVLA-OFT 结果 47.0%，但低于 MemoryVLA 已报告的 88.0%。
- 在 Galaxea A1 机器人上，物体交换任务的成功次数从使用 pi0.5 时的 3/20 增至使用 TFP 时的 15/20；计数抓取与放置任务的成功次数从 8/20 增至 18/20。
- 机制测试显示，操作事件附近的写入增益变化约为远离事件阶段的 6 倍；隐藏状态干预实验表明，信念状态会因果性地改变生成的动作块。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.08283v1](https://arxiv.org/abs/2607.08283v1)
