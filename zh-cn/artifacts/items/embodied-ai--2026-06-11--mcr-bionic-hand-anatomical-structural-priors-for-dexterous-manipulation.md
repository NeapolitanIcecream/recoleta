---
source: arxiv
url: https://arxiv.org/abs/2606.13601v1
published_at: '2026-06-11T17:20:15'
authors:
- Haosen Yang
- Guowu Wei
topics:
- dexterous-manipulation
- musculoskeletal-hand
- anatomical-priors
- tendon-actuation
- robot-hand-design
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# MCR-Bionic Hand: Anatomical Structural Priors for Dexterous Manipulation

## Summary
## 摘要
MCR-Bionic Hand 围绕解剖学手部结构构建了一只仿生机器人手。这些结构会在控制之前影响抓握形成，也会在接触之后调节接触状态。论文认为，这些结构把有用的运动、稳定性和协调性写进了硬件，从而减轻主动控制的负担。

## 问题
- 灵巧机器人手通常依赖高自由度控制，同时简化了手腕、肌腱、韧带和伸肌帽，而这些结构帮助人手在抓握前完成预成形并稳定抓握。
- 这种简化把抓握形成、远端协调和接触后的调整都交给控制器处理，尽管解剖结构本可以承担其中一部分功能。
- 论文要回答的是，哪些解剖结构会改变输入、运动、接触和稳定性之间的关系，并且这些变化为什么对操作有用。

## 方法
- 论文把 MCR-Bionic 做成一只 1:1 的肌骨仿生手，包含 23 块骨骼、61 条腕部韧带、超过 103 个软组织限位结构、46 个肌肉单元和一个 3 自由度手腕。
- 它重建了三种解剖映射：用于预成形的腕-指腱性联结，用于 PIP-DIP 协调的伸肌帽走线，以及用于 MCP 控制和远端稳定性的 intrinsic-plus 通路。
- 它用闭式液压人工肌肉为每条肌腱通路提供局部手内激活。
- 它用象棋棋子抓取、硬币旋转、背侧硬币转移、钢笔传递、钢笔摆动、方块推动和背侧硬币翻转等任务测试这只手。
- 它还配套使用了伸肌帽、腕-指耦合和 intrinsic-plus 行为的几何力学模型。

## 结果
- 该手部原型包含 23 块骨骼、61 条腕部韧带、超过 103 个软组织约束、46 个肌肉单元和 24 个简化自由度；如果把小旋转和掌侧形变算进去，可动自由度超过 45。
- 估计输出在长手指上约为 MCP 1.8 Nm、PIP 1.2 Nm、DIP 0.5 Nm，指尖力约 20 N/指。
- 拇指的输出约为 MCP 1.4 Nm、PIP 0.8 Nm、DIP 0.5 Nm，指尖力约 20 N。
- 手腕活动范围报告为屈伸 -53° 到 18°、桡偏/尺偏 -29° 到 19°、轴向旋转 -60° 到 50°。
- 实验显示，手腕伸展可以触发食指和拇指的被动闭合，用于捏取和提起；重建的伸肌帽会让 DIP 运动跟随 PIP 姿态。
- 论文没有报告与其他机器人手相比的任务成功率或基准数值；它最强的定量结论来自结构计数、扭矩估计、力估计和手腕活动范围。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.13601v1](https://arxiv.org/abs/2606.13601v1)
