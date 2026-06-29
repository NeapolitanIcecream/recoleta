---
source: arxiv
url: https://arxiv.org/abs/2605.15157v1
published_at: '2026-05-14T17:51:40'
authors:
- Zhuohang Li
- Liqun Huang
- Wei Xu
- Zhengming Zhu
- Nie Lin
- Xiao Ma
- Xinjun Sheng
- Ruoshi Wen
topics:
- vision-language-action
- dexterous-manipulation
- interactive-imitation-learning
- human-in-the-loop
- robot-data-scaling
- bimanual-robotics
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Hand-in-the-Loop: Improving Dexterous VLA via Seamless Interventional Correction

## Summary
## 摘要
HandITL 是一种用于灵巧 VLA 策略的人类介入方法，允许操作员在 rollout 过程中修正机器人手臂和手部动作，而不会造成手部姿态的突然跳变。论文声称，这种方法大幅降低了接管时的不连续性，并且用基于在策略纠正的数据微调策略时，比标准遥操作数据效果更好。

## 问题
- 灵巧 VLA 策略在长时程、强接触任务中容易漂移；很小的手指或物体姿态误差会累积成掉落、抓取失败或无法恢复的状态。
- 交互式模仿学习可以在部署过程中收集恢复数据，但在高自由度手部上直接切换到遥操作，会因为人手姿态与机器人手姿态不一致而产生 gesture jumps。
- 这会影响双手仿人手的精细手指修正，同时还要保持现有接触的稳定。

## 方法
- HandITL 将人类修正与运行中的 VLA 策略结合起来，而不是在接管时用绝对遥操作直接替换策略指令。
- 对于手部，它以介入时刻为锚点，把操作员的相对指尖运动映射到机器人手部，因此接管后如果人没有继续移动，机器人手也不会突然动作。
- 手部重定向优化包含指尖形状跟踪、捏合增强、碰撞安全和时间正则化。
- 对于手臂，它把 Meta Quest 3 腕部控制器的运动转换为残差速度 twist，并将其加到策略的手臂指令上。
- 系统记录执行过的在策略纠正 rollout，并用这些数据微调基础 VLA 策略。

## 结果
- 在 Bread Clip 接管测试中，直接切换到遥操作的平均指令变化约为 4.38e-2；HandITL 将其降到约 6.8e-5，下降 99.8%，也低于 DeltaCmd 的约 6.23e-3。
- 在 Drill 接管测试中，直接切换的平均指令变化约为 2.75e-2；HandITL 将其降到约 2.65e-4。
- 在接管后的 Pick Up and Place the Parts 任务中，HandITL 完成任务用时 42.8 ± 5.0 s，而 Teleop 为 52.9 ± 14.2 s，Jacobian 为 68.0 ± 10.8 s，DeltaCmd 为 56.7 ± 14.5 s。
- 在同一 parts 任务中，HandITL 在 10 次试验里只有 1 次重试，而 Teleop 有 8 次重试，论文将其报告为抓取失败减少 87.5%。
- 在 Pick Up the Drill 任务中，HandITL 的平均时间最短，为 14.4 ± 4.7 s；Teleop 为 15.5 ± 5.7 s，DeltaCmd 为 17.3 ± 5.4 s，Jacobian 为 19.4 ± 5.6 s；drill-trigger 成功率方面，HandITL 为 8/10，Teleop 为 10/10。
- 用于策略微调时，HandITL 的纠正数据在三项长时程灵巧任务上的平均表现比等时长的标准遥操作数据高 19%，根据摘要中的描述。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.15157v1](https://arxiv.org/abs/2605.15157v1)
