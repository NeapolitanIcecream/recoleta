---
source: arxiv
url: http://arxiv.org/abs/2604.02523v1
published_at: '2026-04-02T21:23:08'
authors:
- Antonia Bronars
- Younghyo Park
- Pulkit Agrawal
topics:
- robot-learning
- controller-gains
- behavior-cloning
- reinforcement-learning
- sim2real
relevance_score: 0.81
run_id: materialize-outputs
language_code: zh-CN
---

# Tune to Learn: How Controller Gains Shape Robot Policy Learning

## Summary
## 摘要
本文研究低层 PD 控制器增益如何改变机器人策略学习。核心观点是，增益应当按训练设置中的可学习性来选，而不是假定它们会直接设定任务顺应性。

## 问题
- 已学习的操作策略通常经过位置控制器执行，但增益选择仍常被当作经典控制问题，按刚度或顺应性来定。
- 这种看法忽略了有反应的策略如何工作：策略和控制器一起形成闭环行为，所以增益主要改变的是策略有多容易训练和迁移。
- 这会影响行为克隆、强化学习和 sim-to-real 迁移，因为同一组增益可能帮助一个流程，也可能拖累另一个流程。

## 方法
- 论文把控制器增益重新看作接口参数，并在三种设置下测试它的影响：行为克隆、从零开始的强化学习，以及零样本 sim-to-real 迁移。
- 在行为克隆中，作者构建了受控数据集，并使用 **Torque-to-Position Retargeting (TPR)**，让不同增益下的轨迹保持接近，同时位置命令标签随增益变化。
- TPR 先用 PD 控制方程把力矩示教转换成位置目标，再以策略频率重放这些目标，从而隔离增益依赖的动作标签带来的影响。
- 在强化学习中，作者针对每个增益设置重新调整动作空间和训练超参数，降低结果差异来自超参数不匹配的可能。
- 在 sim-to-real 中，作者按增益做系统辨识，在匹配的仿真环境里训练 RL 策略，然后在真实 Franka 机器人上评估零样本迁移，同时做了域随机化和控制频率消融实验。

## 结果
- **行为克隆：** 在多个操作任务和机器人形态上，最佳闭环成功率集中在 **顺应、过阻尼** 增益区间；刚性强或阻尼较弱的增益会降低成功率。节选没有给出热图里各任务的精确成功率。
- **TPR 保真度：** 在最高 **25x decimation（20 Hz）** 的增益设置下，重定向轨迹仍保持 **>=90% 成功率** 和 **关节位置 MSE < 1e-3**。
- **遥操作研究：** 用户研究包含 **12 名用户**、**1 小时** 会话和在箱体推动任务上的 **1,297 次总试验**。节选说结果会在后文报告，但这里没有给出数值结果表。
- **强化学习：** 论文声称，只要把超参数调到和增益设置匹配，RL 就能在 **所有测试过的增益区间** 内学到成功策略，覆盖操作和运动任务。节选没有给出最终成功率或奖励数值。
- **sim-to-real：** 论文声称 **刚性** 和 **过阻尼** 增益会恶化电机层面的 sim-to-real 迁移；评估时，每个增益设置使用 **30 次真实世界 rollout**，以状态轨迹 MSE 为指标。节选没有给出最终 MSE 数值。
- **数据实践观察：** 作者分析 DROID 和 Open X-Embodiment 数据集后发现，现有数据集似乎把 **刚性跟踪行为** 当作默认设置，这个判断依据是命令跟随曲线，而不是已公开的增益值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02523v1](http://arxiv.org/abs/2604.02523v1)
