---
source: arxiv
url: http://arxiv.org/abs/2604.13942v1
published_at: '2026-04-15T14:53:09'
authors:
- Zhen Liu
- Xinyu Ning
- Zhe Hu
- Xinxin Xie
- Weize Li
- Zhipeng Tang
- Chongyu Wang
- Zejun Yang
- Hanlin Wang
- Yitong Liu
- Zhongzhu Pu
topics:
- vision-language-action
- long-horizon-manipulation
- robot-planning
- memory-augmented-policy
- adaptive-replanning
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection

## Summary
## 摘要
Goal2Skill 通过把规划和控制分开，并加入记忆、验证和失败恢复，来处理长时程机器人操作。论文声称，这种闭环设计能提升 RMBench 任务上的成功率，而反应式 VLA 策略在这些任务上常常失败。

## 问题
- 现有的 vision-language-action 策略通常只基于短观察窗口和直接动作预测，这让它们在具有部分可观测、遮挡、干扰物和多阶段依赖的长任务中很脆弱。
- 长时程操作要求机器人记住先前结果，把目标拆成子任务，检查每一步是否完成，并在执行偏离轨道时恢复。
- 这很重要，因为在缺少记忆和显式纠正时，局部上看合理的动作也可能毁掉一个多步骤任务。

## 方法
- 该方法使用两个模块：高层 VLM 规划器和低层 VLA 执行器。规划器决定下一步做什么子任务；执行器把这个子任务转成连续的运动动作。
- 规划器维护结构化记忆，包括情节历史、压缩的工作记忆摘要和错误记录。它用这些记忆来拆解目标、跟踪进度、验证后置条件，并决定继续、重试还是重新规划。
- 每个子任务都包含语言指令、前置/后置条件、执行时长、干扰区域和选定的原语技能索引。
- 执行器使用保几何的视觉过滤：规划器预测与任务无关的区域，分割模型把这些区域遮掉，VLA 策略在过滤后的图像、本体感觉和子任务指令上执行。
- 当某一步失败或超时，反思模块会诊断原因，并选择恢复动作，例如重试、调整参数如抓取提示或干扰物约束，或者重建后续计划。

## 结果
- 在五个 RMBench 任务上，Goal2Skill 的**平均成功率为 32.4%**，而最强基线为 **9.8%**。
- 在记忆密集型的 **M(n)** 任务上，它的成功率达到 **38.7%**，而最佳竞争方法为 **9.0%**。
- 论文说明，消融实验表明**结构化记忆**是记忆敏感任务上提升的主要来源。
- 论文还说明，**验证加反思**提升了在易失败任务上的鲁棒性。
- 这段摘要没有给出完整的消融表、逐任务分数、方差或基线名称，所以这里能看到的定量证据只限于这些总体成功率对比。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13942v1](http://arxiv.org/abs/2604.13942v1)
