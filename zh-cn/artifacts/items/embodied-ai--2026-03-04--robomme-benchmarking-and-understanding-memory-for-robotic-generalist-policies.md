---
source: arxiv
url: http://arxiv.org/abs/2603.04639v1
published_at: '2026-03-04T21:59:32'
authors:
- Yinpei Dai
- Hongze Fu
- Jayjun Lee
- Yuejiang Liu
- Haoran Zhang
- Jianing Yang
- Chelsea Finn
- Nima Fazeli
- Joyce Chai
topics:
- robot-benchmark
- vision-language-action
- memory-augmented-policy
- generalist-robot-policy
- long-horizon-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# RoboMME: Benchmarking and Understanding Memory for Robotic Generalist Policies

## Summary
RoboMME提出了一个专门评测机器人通用策略“记忆能力”的大规模基准，并在统一的\(\pi_{0.5}\)骨干上系统比较多种记忆设计。论文的核心结论是：机器人记忆并不存在一种通吃方案，不同任务需要不同的记忆表示与注入方式。

## Problem
- 现有机器人操作评测多数并不**显式要求记忆**，仅靠当前观测也常能成功，因此无法真实衡量长时程、历史依赖的能力。
- 已有少量记忆相关基准和方法使用的**任务范围窄、协议不统一、骨干不同**，导致不同记忆方法难以公平比较，也难以判断哪些结论可泛化。
- 这很重要，因为真实机器人任务常常依赖过去信息，例如**计数、遮挡下追踪、指代消解、模仿先前演示**；如果没有可靠记忆，通用机器人策略很难处理长时程和非马尔可夫场景。

## Approach
- 作者构建了**RoboMME**：一个面向记忆增强操作的标准化仿真基准，按四类认知记忆组织为四个任务套件：**temporal、spatial、object、procedural memory**。
- 基准包含**16个任务、1,600条演示、770k训练时间步**，任务故意设计成**非马尔可夫、部分可观测、动态变化**，并覆盖视频条件、语言指令、子目标和关键帧标注。
- 在统一的**\(\pi_{0.5}\)** VLA骨干上，作者实现了**14个记忆增强变体**，比较三类记忆表示：**symbolic**（语言子目标）、**perceptual**（历史视觉token）、**recurrent**（压缩历史的隐状态）。
- 同时比较三种记忆注入机制：**memory-as-context**（把记忆token直接拼到输入里）、**memory-as-modulator**（用记忆去调制动作网络中间层）、**memory-as-expert**（增加单独的记忆专家分支）。
- 最简单地说，这篇论文做的是：先造一套专门考“机器人是否记得过去发生了什么”的题库，再把不同“记忆插件”装到同一个机器人模型上做公平对比。

## Results
- 基准规模与覆盖面方面，RoboMME包含**16个任务 / 1,600 demonstrations / 770k timesteps**，平均每条轨迹约**481步**；对比MemoryBench仅**3个任务 / 300 demos**，MIKASA-robo(VLA)为**12个任务 / 1,250 demos / 平均72步**，说明RoboMME更偏长时程和系统化记忆评测。
- 任务长度上，多项任务明显长时程，例如**VideoPlaceOrder平均1134步**、**VideoPlaceButton 974步**、**VideoRepick 687步**、**BinFill 604步**，强化了对历史依赖而非瞬时感知的要求。
- 评测设置上，作者在统一条件下比较**14个自家VLA变体 + 4个已有方法**，使用**512-token memory budget**，在**50 episodes/任务、共800 episodes**上评测，并对**3个随机种子、最后3个checkpoint**求均值，提高了比较的可控性。
- 论文的最强实证结论是：**没有任何单一记忆表示或集成策略在全部任务上始终最优**；记忆效果**高度依赖任务类型**，这直接挑战了先前方法在少量自定义任务上得出的泛化结论。
- 定性上，作者声称**symbolic memory**更擅长**counting和短时程推理**，而**perceptual memory**对**时间敏感和动作/轨迹相关行为**更关键。
- 在所有变体中，作者声称**perceptual memory + memory-as-modulator**在**性能与计算效率的平衡**上最好；但给定摘录未提供完整主结果表中的具体平均成功率数字，因此无法在此准确列出其相对\(\pi_{0.5}\)或其他基线的精确增益。

## Link
- [http://arxiv.org/abs/2603.04639v1](http://arxiv.org/abs/2603.04639v1)
