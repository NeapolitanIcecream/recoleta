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
## 摘要
ROSClaw 是一个用单一语义到物理控制闭环来协调不同机器人的系统。它把语言层任务规划、工具调用、数字孪生安全检查和执行数据记录结合起来，让多机器人任务在更少人工集成的情况下运行。

## 问题
- 现有具身机器人系统通常把规划、数据采集、技能训练和部署拆成独立阶段，这会导致模型计划的内容与硬件实际能做的事情之间出现偏差。
- 对异构机器人来说，长时程、多步骤任务很难处理，因为高层语言模型不会建模关节限制、碰撞、时序或硬件专用 SDK 细节。
- 人工硬件测试和按机器人分别编程会拖慢多智能体部署，也让跨平台复用成本更高。

## 方法
- ROSClaw 采用三层架构：用于低频推理的认知层、用于工具/API 映射和调度的协同层，以及用于高频机器人控制的物理层。
- 它构建了一个 **Online Tool Pool**，把 LLM/VLM 智能体给出的抽象指令映射为可执行的 SDK、MCP 和 API 调用，以适配不同机器人平台。
- 它加入了一个基于 **e-URDF** 的物理安全保障机制：在执行前，命令会在 Isaac Lab 中结合机器人模型和约束进行前向动力学与碰撞验证。
- 它把机器人状态、多模态观测和执行轨迹记录到 **Local Resource Pool** 中，以便系统复用经验并支持后续策略优化。
- 在部署阶段，一个统一智能体会在规划与执行之间保持任务上下文，并根据工作空间和能力约束把子任务分配给不同机器人。

## 结果
- 论文报告了在一个 **约 60 平方米的智能家居** 场景中的真实世界验证，主协作任务中有 **三台活跃机器人**：一台人形机器人、一台固定机械臂和一台移动操作机器人。
- 在演示任务中，机器人完成了一个多步骤流程：移动操作机器人开门，人形机器人进入并搬运篮子，固定机械臂抓取用户指定的 **猕猴桃** 并放入篮子中，随后人形机器人把篮子运到水槽。
- 第二项验证使用了 **七个实体云台单元**，在真实执行前进行了 e-URDF 安全检查和仿真编舞验证。
- 最明确的量化说法是，ROSClaw 将多云台协同舞蹈生成时间缩短到 **约 3 分钟**，人工输入只限于最初指令。
- 论文还称标注和演示成本可以 **从数天降到数小时**，但这一点在摘录中只是系统层面的说法，没有配套的受控基准表支撑。
- 这段摘录**没有**提供多机器人任务的标准基准指标、成功率、消融实验，或与具名基线方法的直接数值比较。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04664v1](http://arxiv.org/abs/2604.04664v1)
