---
source: arxiv
url: https://arxiv.org/abs/2606.31958v1
published_at: '2026-06-30T17:00:33'
authors:
- Jagdeep Singh Bhatia
- Andrew Wagenmaker
- William Chen
- Sergey Levine
topics:
- vision-language-action
- generalist-robot-policy
- robot-rl
- prompt-optimization
- robot-data-scaling
- long-horizon-manipulation
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Adapting Generalist Robot Policies with Semantic Reinforcement Learning

## Summary
## 概要
SARL 通过训练作用于语言提示的 RL 策略来适配 VLA 机器人策略，低层电机动作仍由 VLA 生成。这一点很关键，因为长时程任务可能在单个零样本提示下失败，即使 VLA 已经具备所需的低层技能。

## 问题
- 通用机器人策略在预训练分布之外的复杂长时程任务上经常失败。
- 标准 RL 方法会更新或引导低层机器人动作，因此要求基础策略的动作分布一开始就接近有效解。
- VLM 提示选择可以提出合理的子命令，但它不知道哪些提示会在特定机器人上产生有用的物理行为。

## 方法
- SARL 将每个 VLA 语言提示视为一个语义动作。
- 在每一步，SARL 选择一个提示，VLA 将该提示和当前观测转换为机器人动作，环境返回奖励和下一个状态。
- SARL 学习一个语义 Q 函数，并用时序差分备份按预期任务进展为提示打分。
- VLM 根据当前图像和高层任务提出候选语义动作，从而缩小提示搜索范围。
- 真实世界交互会把每个提示锚定到它诱发的行为上，因此学到的控制器可以把简单技能串接成更长的任务。

## 结果
- 在 Libero-10 和 4 个真实世界 WidowX 长时程任务上，SARL 将基础 VLA 在任务提示下接近 0% 的初始成功率提升到 60-100 个在线 episode 后约 80% 的成功率。
- 在 Libero-10 中，SARL 在 5 个任务上成功适配，在 1 个本已接近解决的任务上达到相当表现，另有 4 个任务未被任何测试方法解决。
- Libero-10 曲线中，每个绘图点使用 64 次评估，并报告 3 个随机种子上的标准误。
- 真实世界 WidowX 曲线中，每个绘图点使用 10 次评估。
- 对比基线包括 DSRL、Residual RL，以及一种基于上下文学习的 VLM 提示选择方法；论文报告称，SARL 在测试的长时程适配任务上优于这些方法。
- 真实世界训练为每个任务使用 3 个语言引导演示，并将其加入 SARL 和 Residual RL 的回放缓冲区；DSRL 在评估时不使用这些演示，因为它的潜在噪声动作空间无法直接接收这些演示。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.31958v1](https://arxiv.org/abs/2606.31958v1)
