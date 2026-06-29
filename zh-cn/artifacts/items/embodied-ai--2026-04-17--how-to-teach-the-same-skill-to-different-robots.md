---
source: hn
url: https://actu.epfl.ch/news/how-to-teach-the-same-skill-to-different-robots-2/
published_at: '2026-04-17T22:45:36'
authors:
- hhs
topics:
- cross-robot-transfer
- skill-learning
- manipulation
- kinematics
- safe-control
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# How to teach the same skill to different robots

## Summary
## 摘要
EPFL 的 Kinematic Intelligence 目标是把人类示范的操作技能迁移到不同运动学结构的机器人之间，而不需要为每台机器人重写任务代码。核心主张是，让多台商用机器人安全、可预测地执行同一串任务步骤。

## 问题
- 在一台机器人上编写或示范的任务，换到另一台机器人上往往不能直接使用，因为机器人的关节布局、可达范围、运动限制和稳定性约束都不同。
- 每台机器人都从头重新编程会提高部署成本，拖慢升级速度，也会让机器人车队更难维护。
- 在制造业和其他硬件变化快于任务规格的场景里，技能迁移很重要。

## 方法
- 系统从人类示范的操作任务出发，例如放置、推动和抛掷，这些任务通过动作捕捉记录。
- 它把每个示范任务转换成与机器人无关的运动策略，而不是保留一个只绑定单一机器人本体的控制器。
- 它为每种机器人的运动学和安全限制建立结构化描述，包括关节范围、禁止构型以及与稳定性相关的约束。
- 它把共享的运动策略自动适配到每台机器人上，使机器人能在自身可行的运动空间内执行该技能。
- 论文把这套方法描述为用于跨机器人技能迁移和安全执行的 “Kinematic Intelligence”。

## 结果
- 在一项装配线实验中，三种不同的商用机器人复现了同一串示范动作：把木块从传送带上推下，放到桌上，再把它扔进篮子里。
- 报告的结果是三台机器人都能安全、可靠地执行，即使任务步骤在机器人之间的分配方式发生了变化。
- 摘要没有给出基准对照表、误差率、成功率或运行时间数据。
- 最明确的具体主张是一次示范、多台执行，也就是同一项人类示范技能可以在不同机械设计的机器人之间使用。

## Problem

## Approach

## Results

## Link
- [https://actu.epfl.ch/news/how-to-teach-the-same-skill-to-different-robots-2/](https://actu.epfl.ch/news/how-to-teach-the-same-skill-to-different-robots-2/)
