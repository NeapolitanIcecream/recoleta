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
EPFL 的 Kinematic Intelligence 旨在把人类示范的操作技能迁移到运动学结构不同的机器人上，而不需要为每台机器人重写任务代码。核心主张是让多款商用机器人安全、可预测地执行同一组任务序列。

## 问题
- 在一台机器人上编程或示范的任务，换到另一台机器人上往往无法直接使用，因为机器人在关节布局、可达范围、运动限制和稳定性约束上存在差异。
- 为每台机器人从头重新编程会提高部署成本，拖慢升级速度，也会增加机器人集群的维护难度。
- 在制造业等场景中，硬件更替速度快于任务规格变化，技能迁移因此很重要。

## 方法
- 该系统从人类对放置、推动、投掷等操作任务的示范开始，并用运动跟踪进行采集。
- 它把每个示范任务转换成一种与具体机器人无关的运动策略，而不是保留只适用于某一种机器人本体的控制器。
- 它为每台机器人建立一套结构化描述，涵盖其运动学限制和安全边界，包括关节范围、禁止配置和与稳定性相关的约束。
- 它会自动把共享的运动策略适配到每台机器人上，使机器人能在自身可行的运动空间内执行该技能。
- 论文将这种跨机器人技能迁移与安全执行的方法称为“运动学智能”（Kinematic Intelligence）。

## 结果
- 在一项装配线实验中，三款不同的商用机器人复现了同一段示范序列：把木块从传送带上推下，放到桌面上，再投进篮子里。
- 报道称，即使改变机器人之间的任务步骤分配方式，三台机器人也都能安全、稳定地完成执行。
- 摘要中没有提供基准表、错误率、成功率或运行时间数据。
- 最具体的主张是“一次示范，多机执行”式的单次迁移，也就是同一个人类示范技能可用于机械设计不同的多台机器人。

## Problem

## Approach

## Results

## Link
- [https://actu.epfl.ch/news/how-to-teach-the-same-skill-to-different-robots-2/](https://actu.epfl.ch/news/how-to-teach-the-same-skill-to-different-robots-2/)
