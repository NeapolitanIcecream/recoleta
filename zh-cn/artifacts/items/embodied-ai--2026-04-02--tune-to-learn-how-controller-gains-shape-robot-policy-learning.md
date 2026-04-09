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
## 概要
本文研究底层 PD 控制器增益如何改变机器人策略学习。核心结论是，增益应根据训练设置中的可学习性来选择，而不是假设它们会直接决定任务中的顺应性。

## 问题
- 学到的操作策略通常通过位置控制器执行，但增益选择仍被当作经典控制中的选择，主要依据刚度或顺应性。
- 这种看法忽略了反应式策略的工作方式：策略与控制器共同形成闭环行为，因此增益主要改变的是策略训练和迁移的难易程度。
- 这对行为克隆、强化学习和 sim-to-real 迁移都很重要，因为同一组增益设置可能有利于一种流程，却会损害另一种流程。

## 方法
- 论文将控制器增益重新看作一种接口参数，并在三种设置中测试其影响：行为克隆、从零开始的 RL，以及零样本 sim-to-real 迁移。
- 在行为克隆部分，作者使用 **Torque-to-Position Retargeting (TPR)** 构建受控数据集，使不同增益设置下的轨迹保持接近，同时位置命令标签会随增益变化。
- TPR 使用 PD 控制方程将力矩示范转换为位置目标，然后按策略频率重放，以隔离依赖增益的动作标签所带来的影响。
- 在 RL 部分，作者针对每种增益设置重新调节动作空间和训练超参数，以减少因超参数不匹配导致结果较差的可能性。
- 在 sim-to-real 部分，作者对每组增益分别进行系统辨识，在匹配的模拟器中训练 RL 策略，并在真实 Franka 机器人上评估零样本迁移，同时进行领域随机化和控制频率消融实验。

## 结果
- **行为克隆：** 在多个操作任务和机器人平台上，最佳闭环成功率集中在 **高顺应、过阻尼** 的增益区间；刚性高或阻尼不足的增益会降低成功率。摘录没有给出热图中各任务的精确成功率数值。
- **TPR 保真度：** 在增益设置变化的情况下，重定向轨迹在最高 **25x decimation (20 Hz)** 时仍保持 **>=90% success** 和 **joint-position MSE < 1e-3**。
- **遥操作研究：** 用户研究包括 **12 users**、**1-hour sessions** 和 **1,297 total trials**，任务是推动箱子。摘录说明结果在后文报告，但这里没有给出具体数值表。
- **强化学习：** 论文称，只要超参数经过调节并与增益设置匹配，RL 就能在 **all tested gain regimes** 中学到成功策略，覆盖操作和运动任务。摘录没有包含最终成功率或回报数值。
- **Sim-to-real：** 论文称 **stiff and overdamped** 增益会使电机层面的 sim-to-real 迁移变差；迁移评估基于每组增益设置 **30 real-world rollouts** 的状态轨迹 MSE。摘录没有给出最终 MSE 数值。
- **数据实践观察：** 通过分析 DROID 和 Open X-Embodiment 数据集，作者报告现有数据集似乎默认使用 **stiff tracking behavior**，这一判断依据是命令跟踪曲线，而不是已发表的增益数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02523v1](http://arxiv.org/abs/2604.02523v1)
