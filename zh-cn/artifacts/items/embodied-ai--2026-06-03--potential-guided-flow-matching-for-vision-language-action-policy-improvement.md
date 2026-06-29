---
source: arxiv
url: https://arxiv.org/abs/2606.04968v1
published_at: '2026-06-03T14:49:35'
authors:
- Yunpeng Mei
- Jiakai He
- Hongjie Cao
- Chenyu Wang
- Xiaowen Zhu
- Yihan Zhou
- Jiamin Wang
- Chenbo Xin
- Peng Cheng
- Yuxuan Yang
- Yijie Wang
- Xinhu Zheng
- Gao Huang
- Jie Chen
- Gang Wang
topics:
- vision-language-action
- robot-policy
- flow-matching
- offline-rl
- bimanual-manipulation
- robot-data-scaling
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Potential-Guided Flow Matching for Vision-Language-Action Policy Improvement

## Summary
## 总结
ForesightFlow 通过给每个动作块加入生成的成功潜势分数，改进了在混合机器人数据上训练的视觉-语言-动作流策略。它用这些分数做 best-of-K 动作选择，不需要单独的 critic。

## 问题
- 已部署的机器人会收集混合轨迹，里面既有成功动作，也有部分进展、可恢复错误和失败；直接做行为克隆会把失败也学进去。
- 过滤后的行为克隆会丢掉有用的子轨迹，而 IDQL 这类离线强化学习方法要加一个很大的 critic，训练开销也更高。
- 这篇论文面向长时程操作任务，在稀疏成功标签下，很难学到哪些局部动作块真的能推进任务进展。

## 方法
- 策略在生成时同时输出一个动作块 `a` 和一个与该块时域对齐的成功潜势向量 `s`。
- 用阶段级二元标签训练潜势向量，所以即使整条轨迹最后失败，部分有用的进展也能得到监督。
- 优势加权流匹配会提高高优势动作的权重，使用 `min(M, exp(A/tau))` 这类权重。
- 动作损失和潜势损失分开训练：优势权重只作用在动作速度上，潜势速度则在成功和失败样本上统一训练。
- 一步边界估计器为优势计算提供上下文基线；推理时采样 `K` 个候选，并执行平均生成潜势最高的那个。

## 结果
- 在五个 BEHAVIOR-1K 仿真任务上，ForesightFlow 的平均归一化分数最好：`0.46`，而 IDQL 为 `0.44`，FQL 为 `0.39`，Filtered BC 为 `0.38`，BC 为 `0.35`。
- 在仿真中，它的平均成功率为 `39.6%`，接近 IDQL 的 `39.0%`，高于 FQL 的 `34.4%`、Filtered BC 的 `31.6%` 和 BC 的 `31.0%`；这里使用 `K=5` 个自引导候选。
- 在五个真实世界的双臂任务上，它的平均分数为 `0.62`，成功率为 `35.4%`，对比 IDQL 的 `0.59` 和 `32.6%`，以及 Filtered BC 的 `0.51` 和 `24.6%`。
- 训练计算量从 IDQL 的 `287` GPU 小时降到 `178` GPU 小时，报告中的降幅为 `38%`。
- 与价值相关的参数开销约为 `1K` 参数，而 IDQL 的独立 critic 约有 `~500M` 参数；总参数量为 `2.35B`，而 IDQL 约为 `~2.84B`。
- 在 `K=5` 时，报告的延迟为 ForesightFlow 的 `155 ms`，IDQL 为 `183 ms`；Radio 消融报告显示，解耦训练的最终阶段完成率为 `51.0%`，耦合训练为 `42.0%`，BC 为 `44.0%`。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.04968v1](https://arxiv.org/abs/2606.04968v1)
