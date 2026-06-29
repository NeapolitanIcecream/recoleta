---
source: arxiv
url: https://arxiv.org/abs/2606.19990v1
published_at: '2026-06-18T09:29:30'
authors:
- Pu Li
- Zhigang Lin
- Qiang Wu
- Yongxuan Lv
- Fei Wang
- Shan You
topics:
- embodied-world-models
- robot-foundation-models
- diffusion-rl
- reward-modeling
- grpo
- robotics-evaluation
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Reward as An Agent for Embodied World Models

## Summary
## 摘要
论文提出一种用于具身世界模型的 RL 后训练方法，使用智能体式奖励评估器和动态感知的 GRPO rollout 方法。核心主张是：当奖励信号检查物理合理性、指令遵循和任务完成情况时，更广的探索可以改进世界模型。

## 问题
- 现有世界模型 RL 方法让 rollout 保持在训练分布附近，因为奖励模型在更广探索下会失效。
- 在具身场景中，弱奖励可能给带有模糊、静态运动、简化背景或错误物理的视频打高分，因此优化会提高奖励分数，却不改进任务表现。
- 这一点重要，因为机器人世界模型需要合理的物体交互和任务完成，不只是外观好看的视频。

## 方法
- 奖励系统使用前沿 VLM 作为评估器，从四个维度评估：视觉质量、指令遵循、物理合规性和任务完成。
- 它先制定全局评分计划，再使用课程机制，让基础视频有效性作为后续检查的门控，例如任务完成和物理检查。
- 它把困难检查拆成更小的投票项，例如目标一致性、智能体一致性、视角一致性、交互真实性、形变和穿透。
- 它加入反思步骤，让评估器重新检查自己的分数和解释。
- DynDiff-GRPO 主要在从时间变化中检测出的动态区域加入扩散噪声，因此移动物体和接触区域比静态场景区域获得更多探索。

## 结果
- 摘录没有给出 Table 1 的最终数值准确率提升，因为表格被截断。
- 论文称在两个开源具身世界模型上取得提升：Kairos-3.0-Robot 和 Cosmos-Predict2.5-2B。
- 评估使用 PAI-Bench 的机器人子集，并按每个 prompt 报告 Domain Score 和 Overall/Quality Score，其中 Qwen3.5 用作裁判模型。
- 奖励黑客示例显示，较差 rollout 会得到较高代理分数：视觉遮挡在 VideoAlign VQ 上得到 0.79/1.0，背景简化在 VideoAlign VQ 上得到 0.80/1.0，运动退化在 UnifiedReward Alignment Score 上得到 2.76/5.0，物理失效在 UnifiedReward Physics Score 上得到 3.0/5.0。
- 奖励设计经过 20 多轮迭代细化；需要时，每轮会人工检查数百条采样轨迹。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.19990v1](https://arxiv.org/abs/2606.19990v1)
