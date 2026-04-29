---
source: arxiv
url: http://arxiv.org/abs/2604.18000v1
published_at: '2026-04-20T09:25:30'
authors:
- Haiweng Xu
- Sipeng Zheng
- Hao Luo
- Wanpeng Zhang
- Ziheng Xi
- Zongqing Lu
topics:
- vision-language-action
- robot-benchmarking
- embodied-reasoning
- generalist-robot-policy
- semantic-grounding
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Unmasking the Illusion of Embodied Reasoning in Vision-Language-Action Models

## Summary
## 摘要
这篇论文认为，标准 Vision-Language-Action 基准上的高分常常夸大了真实的具身推理能力。论文提出了 BeTTER，这是一个诊断型基准，通过对任务施加受控干预，显示当前的 VLA 在需要语义 grounding、状态跟踪和子目标组合的变化下会失效。

## 问题
- 标准机器人基准可能会奖励模仿和捷径使用，因此较高的成功率不一定意味着模型真的理解指令、跟踪任务状态，或规划多步行为。
- 现有鲁棒性基准通常会改变外观或布局，但不能清楚地区分推理失败和底层控制或感知能力的限制。
- 这对机器人基础模型很重要，因为一个在静态、域内环境中有效的策略，在物体布局、任务顺序或语义干扰项变化时可能会失败。

## 方法
- 论文提出 **BeTTER**（Benchmark for Testing True Embodied Reasoning），这是一个包含 10 个基础操作任务的基准，并通过受控干预扩展为 60 个任务变体。
- 它在测试时考察四个推理维度：空间布局变化、原子动作重组、对抗性物体扰动和时间外推。
- 该基准使用基于模板的任务生成、开放词汇的 3D 资产检索，以及基于少量遥操作演示的程序化轨迹扩增。
- 它记录模拟器中的特权状态，例如深度、边界框和分割掩码，这样就可以把失败分析为推理错误，而不只是执行噪声。
- 作者评估了三个 VLA：pi_0.5、GR00T-N1.6 和 Being-H0.5，并报告了真实机器人压力测试，以检查这些失败是否不只是仿真伪影。

## 结果
- 在一个指令 grounding 压力测试中，随机基线为 50%，模型表现出明显偏向，而不是稳定的 grounding：**pi_0.5** 在 "top" 上为 **65.0%**，在 "bottom" 上为 **50.0%**，在 "red" 上为 **70.0%**，在 "blue" 上为 **35.0%**；**GR00T-N1.6** 分别为 **100.0%**、**100.0%**、**5.0%**、**5.0%**；**Being-H0.5** 分别为 **100.0%**、**30.0%**、**95.0%**、**45.0%**。
- 在子目标重组测试中，与已见过的序列 **A->B** 和 **A->C** 相比，三个模型在未见过的组合 **B->C** 上都明显失效。**pi_0.5** 的成功率从 **60.0/45.0** 降到 **5.0**（**-47.5**），**GR00T-N1.6** 从 **75.0/40.0** 降到 **15.0**（**-42.5**），**Being-H0.5** 从 **65.0/40.0** 降到 **0.0**（**-52.5**）。
- 在一个实例级对抗语义测试中，**pi_0.5** 在 **85%** 的试验中拒绝了一个视觉上相似的干扰物，论文将其视为模型在简单场景下具有部分鲁棒性。
- 对于杂乱场景和未见过的布局，论文称所有模型都表现出较高的 Distractor Grasp Rate，但摘录没有给出确切的 DGR 数值。
- 论文的主要结论是，当前的 VLA 依赖捷径相关性，例如词汇-运动学映射、布局偏置、行为惯性和较弱的因果状态跟踪；根据作者的压力测试，这些失败在真实机器人上也会出现。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.18000v1](http://arxiv.org/abs/2604.18000v1)
