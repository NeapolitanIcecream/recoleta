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
Goal2Skill 通过将规划与控制分开，并加入记忆、验证和失败恢复，来处理长时程机器人操作。论文称，这种闭环设计提高了 RMBench 任务上的成功率，而反应式 VLA 策略在这些任务上经常失败。

## 问题
- 现有视觉-语言-动作策略通常依赖较短的观测窗口和直接动作预测，因此在具有部分可观测性、遮挡、干扰项和多阶段依赖的长任务中较脆弱。
- 长时程操作要求机器人记住先前结果，将目标拆分为子任务，检查每一步是否成功，并在执行偏离轨道时恢复。
- 这一点很重要，因为即使局部动作看起来合理，如果系统缺少记忆和明确的纠错机制，仍可能破坏整个多步任务。

## 方法
- 该方法使用两个模块：高层 VLM 规划器和低层 VLA 执行器。规划器决定下一步执行哪个子任务；执行器将该子任务转换为连续电机动作。
- 规划器维护结构化记忆，包括情节历史、紧凑的工作记忆摘要和错误寄存器。它利用这些记忆来分解目标、跟踪进度、验证后置条件，并决定继续、重试还是重新规划。
- 每个子任务都包含语言指令、前置/后置条件、执行时域、干扰区域以及选定的原子技能索引。
- 执行器采用保留几何结构的视觉过滤：规划器预测与任务无关的区域，分割模型将其掩蔽，VLA 策略再基于过滤后的图像、本体感觉信息和子任务指令执行动作。
- 当某一步失败或超时，反思模块会诊断原因，并选择恢复动作，例如重试、调整抓取提示或干扰约束等参数，或重建剩余计划。

## 结果
- 在五个 RMBench 任务上，Goal2Skill 的**平均成功率为 32.4%**，而最强基线为 **9.8%**。
- 在记忆负担较重的 **M(n)** 任务上，其成功率达到 **38.7%**，而最佳竞争方法为 **9.0%**。
- 论文称，消融实验表明，**结构化记忆**是记忆敏感任务上性能提升的主要来源。
- 论文还称，**验证与反思**提高了易失败任务上的鲁棒性。
- 这段摘录没有给出完整的消融表、各任务分数、方差或基线名称，因此这里可用的定量证据仅限于这些总体成功率对比。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13942v1](http://arxiv.org/abs/2604.13942v1)
