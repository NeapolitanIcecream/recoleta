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
这篇论文认为，标准 Vision-Language-Action 基准上的高分经常夸大了真实的具身推理能力。论文提出 BeTTER，这是一个诊断性基准，通过受控任务干预来测试，结果显示当前 VLAs 在需要落地、状态跟踪和子目标组合的变化下会失效。

## 问题
- 标准机器人基准可能会奖励模仿和捷径使用，所以很高的成功率不一定说明模型真正理解指令、跟踪任务状态或规划多步行为。
- 现有的鲁棒性基准经常只改变外观或布局，但没有把推理失败和低层控制或感知限制清楚地区分开。
- 这对机器人基础模型很重要，因为一个在静态、域内场景中表现良好的策略，在物体布局、任务顺序或语义干扰项变化时可能会失败。

## 方法
- 论文提出 **BeTTER**（Benchmark for Testing True Embodied Reasoning），这是一个基准，把 10 个基础操作任务扩展成 60 种任务变体，方式是施加受控干预。
- 它在测试时检查四个推理轴：空间布局变化、原语重组、对抗性物体扰动和时间外推。
- 该基准使用基于模板的任务生成、开放词汇 3D 资产检索，以及从少量遥操作演示出发的程序化轨迹扩增。
- 它记录特权模拟器状态，比如深度、边界框和分割掩码，这样就可以把失败分析为推理错误，而不是纯执行噪声。
- 作者评估了三种 VLA：pi_0.5、GR00T-N1.6 和 Being-H0.5，并报告了真实机器人上的压力测试，用来检查这些失败是否只来自仿真伪影。

## 结果
- 在一个指令落地压力测试中，随机基线是 **50%**，模型表现出明显的极化，而不是稳定的落地能力：**pi_0.5** 在“top”上得 **65.0%**，在“bottom”上得 **50.0%**，在“red”上得 **70.0%**，在“blue”上得 **35.0%**；**GR00T-N1.6** 分别是 **100.0%**、**100.0%**、**5.0%**、**5.0%**；**Being-H0.5** 分别是 **100.0%**、**30.0%**、**95.0%**、**45.0%**。
- 在子目标重组任务上，三个模型在未见过的组合 **B->C** 上都崩溃了，而在已见过的序列 **A->B** 和 **A->C** 上表现更好。**pi_0.5** 的成功率从 **60.0/45.0** 降到 **5.0**（**-47.5**），**GR00T-N1.6** 从 **75.0/40.0** 降到 **15.0**（**-42.5**），**Being-H0.5** 从 **65.0/40.0** 降到 **0.0**（**-52.5**）。
- 在一个实例级语义对抗测试中，**pi_0.5** 在 **85%** 的试验中拒绝了一个视觉上相似的干扰项，论文把这作为在简单场景下的部分鲁棒性。
- 对于杂乱场景和未见过的布局，论文说所有模型的 Distractor Grasp Rate 都很高，但摘录没有给出具体的 DGR 数值。
- 作者主张的主要发现是，当前 VLAs 依赖词汇-运动映射、布局偏置、行为惯性和较弱的因果状态跟踪等捷径相关性，而这些失败也出现在真实机器人上，作者的压力测试支持这一点。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.18000v1](http://arxiv.org/abs/2604.18000v1)
