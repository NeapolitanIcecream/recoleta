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
HandITL 是一种用于灵巧 VLA 策略的人工干预方法，允许操作者在 rollout 过程中校正机器人手和机械臂，同时不引发手部姿态突跳。论文称，相比标准遥操作数据，HandITL 显著降低了接管时的不连续性，并且用在策略执行中采集的校正数据进行微调时效果更好。

## 问题
- 灵巧 VLA 策略在长时程、接触密集的任务中可能发生偏移；细小的手指误差或物体姿态误差会累积，导致掉落、抓取失败或无法恢复的状态。
- 交互式模仿学习可以在部署过程中采集恢复数据，但在高自由度手上直接遥操作接管会造成手势突跳，因为人手姿态在接管时与机器人手姿态不匹配。
- 这一点很关键，因为双手拟人机器人手需要在保持现有接触稳定的同时进行精细的手指校正。

## 方法
- HandITL 将人工校正与正在运行的 VLA 策略融合，避免在接管时用绝对遥操作命令直接替换策略命令。
- 对于手部，它以干预时刻为锚点，将操作者的相对指尖运动映射到机器人手；因此，接管后如果人没有动作，机器人手也不会突然动作。
- 手部重定向优化包含指尖形状跟踪、捏合强化、碰撞安全和时间正则化。
- 对于机械臂，它将 Meta Quest 3 手腕控制器的运动转换为残差速度 twist，并叠加到策略的机械臂命令上。
- 系统记录已执行的在策略校正 rollout，并用这些数据微调基础 VLA 策略。

## 结果
- 在 Bread Clip 接管测试中，直接切换遥操作产生的平均命令变化约为 4.38e-2；HandITL 将其降至约 6.8e-5，减少 99.8%，也低于 DeltaCmd 的约 6.23e-3。
- 在 Drill 接管测试中，直接切换产生的平均命令变化约为 2.75e-2；HandITL 将其降至约 2.65e-4。
- 在接管后的 Pick Up and Place the Parts 任务中，HandITL 用时 42.8 ± 5.0 s 完成任务，Teleop 为 52.9 ± 14.2 s，Jacobian 为 68.0 ± 10.8 s，DeltaCmd 为 56.7 ± 14.5 s。
- 在同一个零件任务中，HandITL 在 10 次试验中重试 1 次，Teleop 重试 8 次，报告为抓取失败减少 87.5%。
- 在 Pick Up the Drill 中，HandITL 的平均用时最快，为 14.4 ± 4.7 s；Teleop 为 15.5 ± 5.7 s，DeltaCmd 为 17.3 ± 5.4 s，Jacobian 为 19.4 ± 5.6 s；钻机扳机成功率 HandITL 为 8/10，Teleop 为 10/10。
- 根据摘录，在策略改进方面，HandITL 校正数据在三个长时程灵巧任务上的平均表现比等时长标准遥操作数据高 19%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.15157v1](https://arxiv.org/abs/2605.15157v1)
