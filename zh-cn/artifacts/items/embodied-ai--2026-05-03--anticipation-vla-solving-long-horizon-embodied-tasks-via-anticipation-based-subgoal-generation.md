---
source: arxiv
url: https://arxiv.org/abs/2605.01772v1
published_at: '2026-05-03T08:11:35'
authors:
- Zhilong Zhang
- Wenyu Luo
- Haonan Wang
- Yifei Sheng
- Yidi Wang
- Hanyuan Guo
- Haoxiang Ren
- Xinghao Du
- Yuhan Che
- Tongtong Cao
- Lei Yuan
- Yang Yu
topics:
- vision-language-action
- generalist-robot-policy
- long-horizon-planning
- subgoal-generation
- robot-manipulation
- world-model
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Anticipation-VLA: Solving Long-Horizon Embodied Tasks via Anticipation-based Subgoal Generation

## Summary
## 摘要
Anticipation-VLA 为面向目标的 VLA 策略加入了自适应子目标生成，用于长时程机器人任务。它提升了仿真操作结果，并报告在现实世界未见设置中有更大的增益。

## 问题
- 标准 VLA 策略常常在长时程任务上失败，因为小的动作误差会在很多步骤中累积。
- 固定的子任务拆分对当前状态来说可能过粗或过细，所以当机器人停滞或场景变化时，它们可能无法指导执行。
- 这对家居和移动操作任务很重要，因为机器人必须在语言或图像目标下完成多个相互依赖的阶段。

## 方法
- 系统维护一个活动目标和子目标栈。高层预测模型提出下一个可达的子目标，低层 VLA 策略朝这个子目标执行。
- 预测模型先生成文本子目标，再预测匹配的子目标图像。逆动力学检查会拒绝那些推断出的指令与文本子目标不一致的图像子目标。
- 值模型把进展分成三类：目标已达成、进展改善、进展停滞。这个分类会触发目标出栈、继续执行，或递归细化子目标。
- 作者用 Bagel 这个统一多模态模型实现高层模型，并通过微调一个目标条件的 $\pi_{0.5}$ 风格 flow-matching VLA 实现低层策略。
- 训练使用用于预测、值分类和目标条件动作预测的分层数据集。

## 结果
- 在 Libero one-trajectory SFT 上，Anticipation-VLA 的平均成功率为 80.8，$\pi_{0.5}$ 为 76.8，$\pi_{0.5}$+VLM 为 76.0，$\pi_0$ 为 64.6，DreamVLA 为 27.3，UniVLA 为 21.5。
- 在主长时程基准 Libero-Long 上，Anticipation-VLA 得分 63.2，$\pi_{0.5}$ 为 54.6，$\pi_{0.5}$+VLM 为 53.2。
- 在 VLABench Hammer Nail & Hang Picture 上，Anticipation-VLA 的过程奖励为 56.3，成功率为 4.2，$\pi_{0.5}$+VLM 为 47.9 和 2.1。
- 在 Arx-X5 的真实世界测试中，论文对 Rearrange Objects 使用 100 个演示，对 Spell Words 使用 200 个演示，每个任务分成 20 个见过配置和 20 个未见配置，共 40 次 rollout。
- 摘录没有给出精确的真实世界成功率，但报告在见过配置上比基线高 60%，在未见配置上高 107%。它还说 Anticipation-VLA 是在未见的 Spell Words 上唯一有非零成功率的测试模型。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01772v1](https://arxiv.org/abs/2605.01772v1)
