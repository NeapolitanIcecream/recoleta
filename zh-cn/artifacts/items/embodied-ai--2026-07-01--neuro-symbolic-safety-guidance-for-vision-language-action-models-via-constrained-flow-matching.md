---
source: arxiv
url: https://arxiv.org/abs/2607.01378v1
published_at: '2026-07-01T18:41:33'
authors:
- William English
- Hao Zheng
- Rickard Ewetz
topics:
- vision-language-action
- robot-safety
- flow-matching
- control-barrier-functions
- collision-avoidance
- generalist-robot-policy
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Neuro-Symbolic Safety Guidance for Vision-Language-Action Models via Constrained Flow Matching

## Summary
## 摘要
这篇论文为基于流匹配的 VLA 机器人策略加入了轨迹级碰撞引导。该方法在去噪过程中引导 π0.5 的动作块，使机器人能避开未来数步内会出现的碰撞。

## 问题
- 基于流匹配的 VLA 会输出动作块，但常见安全过滤器只修正下一步动作，在杂乱操作场景中可能反应过晚。
- 不安全的操作可能导致任务失败或损坏机器人硬件；训练期安全方法也需要重新训练。
- 在 SafeLIBERO 上，未加引导的 π0.5 基线只有 18.69% 的避碰率和 50.88% 的任务成功率。

## 方法
- 该方法把每个中间流匹配动作块视为一条预测的 10 步末端执行器轨迹。
- 它将夹爪建模为椭球体，将障碍物建模为球体，并在安全边距下计算带符号的间隙分数。
- 它在整条预测轨迹上应用离散时间控制屏障函数约束，而不只约束下一次状态转移。
- 当未来违规出现时，它使用 SLSQP 求解最小范数约束优化问题，以调整平移动作分量。
- 修正后的动作块进入下一次去噪步骤，因此 π0.5 会从经过安全修正的轨迹继续生成。

## 结果
- 在 SafeLIBERO 总体结果上，该方法报告的避碰率为 82.81%，任务成功率为 81.62%。
- 相比 AEGIS 的单步 CBF 过滤，它将避碰率从 77.85% 提高到 82.81%，将任务成功率从 68.13% 提高到 81.62%。
- 相比未加引导的 π0.5，它将避碰率从 18.69% 提高到 82.81%，将任务成功率从 50.88% 提高到 81.62%。
- 在 Long 任务上，该方法报告的避碰率为 82.50%，任务成功率为 76.75%；AEGIS 分别为 79.63% 和 43.75%。
- 代价是执行更慢：平均执行时间步为 299.97，而 AEGIS 为 262.30，未加引导的 π0.5 为 278.24。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.01378v1](https://arxiv.org/abs/2607.01378v1)
