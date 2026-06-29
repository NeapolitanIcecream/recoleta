---
source: arxiv
url: http://arxiv.org/abs/2604.04664v1
published_at: '2026-04-06T13:16:24'
authors:
- Rongfeng Zhao
- Xuanhao Zhang
- Zhaochen Guo
- Xiang Shao
- Zhongpan Zhu
- Bin He
- Jie Chen
topics:
- multi-robot-coordination
- embodied-agent-framework
- vision-language-robotics
- sim-to-real
- digital-twin
- heterogeneous-robots
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# ROSClaw: A Hierarchical Semantic-Physical Framework for Heterogeneous Multi-Agent Collaboration

## Summary
## 概述
ROSClaw 是一个用单一的语义到物理控制闭环来协调不同机器人的系统。它把语言层任务规划、工具调用、数字孪生安全检查和执行数据记录放在一起，减少多机器人任务中的人工集成工作。

## 问题
- 现有具身机器人系统把规划、数据收集、技能训练和部署拆成不同阶段，这会让模型的规划和硬件实际能做的事情之间出现不一致。
- 面向异构机器人的长时序、多步骤任务很难，因为高层语言模型不会建模关节限制、碰撞、时序或硬件特定的 SDK 细节。
- 人工硬件测试和按机器人分别编程会拖慢多智能体部署，也让跨平台复用的成本变高。

## 方法
- ROSClaw 使用三层架构：认知层负责低频推理，协调层负责工具/API 映射和调度，物理层负责高频机器人控制。
- 它构建了一个 **Online Tool Pool**，把 LLM/VLM 智能体的抽象指令映射成不同机器人平台可执行的 SDK、MCP 和 API 调用。
- 它加入了一个 **基于 e-URDF 的物理保护机制**：在执行前，系统会在 Isaac Lab 中结合前向动力学和碰撞验证，检查指令是否符合机器人模型和约束。
- 它把机器人状态、多模态观测和执行轨迹记录到 **Local Resource Pool**，让系统可以复用经验，并支持后续策略细化。
- 在部署时，一个统一智能体会在规划和执行之间保持任务上下文，并根据工作空间和能力约束，把子任务分配给不同机器人。

## 结果
- 论文报告了在一个约 **60 m²** 的智能家居环境中的真实验证，主协作任务里有 **3 台活跃机器人**：一台人形机器人、一台固定机械臂和一台移动操作臂。
- 在演示任务中，机器人完成了一个多步骤序列：移动操作臂开门，人形机器人进入并拿着一个篮子，固定机械臂抓取用户指定的 **kiwi** 并放入篮子，人形机器人把篮子送到水槽。
- 第二个验证使用 **7 个实体云台单元**，先做 e-URDF 安全检查和仿真编队验证，再进行真实执行。
- 最明确的定量结果是，ROSClaw 把协同多云台舞蹈生成时间降到 **约 3 分钟**，人的输入只限于最初指令。
- 论文还声称标注和示范成本可以 **从几天降到几小时**，但这在文中是系统层面的说法，摘要片段里没有对应的受控基准表。
- 该片段**没有**提供标准基准指标、成功率、消融实验，或针对多机器人任务与已命名基线的直接数值比较。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04664v1](http://arxiv.org/abs/2604.04664v1)
