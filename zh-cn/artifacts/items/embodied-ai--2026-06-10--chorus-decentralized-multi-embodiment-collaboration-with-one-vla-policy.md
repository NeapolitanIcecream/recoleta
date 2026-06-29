---
source: arxiv
url: https://arxiv.org/abs/2606.12352v1
published_at: '2026-06-10T17:26:08'
authors:
- Ria Doshi
- Tian Gao
- Annie Chen
- Chelsea Finn
- Jeannette Bohg
topics:
- vision-language-action
- multi-robot-collaboration
- decentralized-control
- robot-foundation-model
- multi-embodiment
- mobile-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# CHORUS: Decentralized Multi-Embodiment Collaboration with One VLA Policy

## Summary
## 总结
CHORUS 用一个预训练的 VLA 策略，让异构机器人队伍中的每个机器人独立运行。每个机器人只看自己的观测和一个身份提示，但这套共享策略仍然能在真实移动机械臂任务中完成协同，不需要运行时通信。

## 问题
- 多机器人操作要求机器人在部分可观测条件下行动时，还要对队友的行为作出反应。
- 集中式策略需要团队范围内的观测和动作，因此上下文长度和通信需求会随着队伍规模增加。
- 分散式的单机器人策略可能需要共享相机、队友本体感觉、在线对齐，或者为每个机器人单独训练一套策略，这会让部署和扩展更难。

## 方法
- CHORUS 以预训练的 $\pi_{0.5}$ 视觉-语言-动作骨干模型为起点，并用 LoRA 在多机器人演示数据上进行微调。
- 训练数据被拆成单机器人元组 $(o_r^t, A_r^t, c_r)$，因此模型一次只看到一个机器人的本地观测、动作片段和身份提示。
- 一个标识机器人的提示词会说明该具身和角色，从而让一套共享策略为不同机器人选择动作。
- 填充到 32 维的动作向量和可变的图像 token，让同一策略可以处理不同的机器人、传感器和动作空间。
- 在推理时，每个机器人只用本地观测运行自己的 CHORUS 副本；不使用机器人之间的消息、共享相机或共享本体感觉状态。

## 结果
- 在篮筐抬举、卷尺测量、图书递交和 3 机器人搬运的真实世界测试中，论文报告每个任务有 25-45 次演示和 10-18 次评估 rollout。
- 与从零训练的分散式扩散策略相比，CHORUS 的平均任务成功率提高了 64 个百分点。
- 在一个受队友扰动的递交测试中，CHORUS 在 20 次试验中成功 17 次，而同一 VLA 骨干模型训练成独立的每机器人策略时是 9/20，提升了 40 个百分点。
- 扰动划分中，左侧扰动为 8/10 对 3/10，右侧扰动为 9/10 对 6/10。
- 在三个双机器人任务上，CHORUS 与集中式 VLA 基线持平或更好，尽管集中式基线同时条件于两台机器人的观测。
- 在一个使用 Kinova 和 YAM 移动机械臂的 3 机器人搬运任务上，一套不变的 CHORUS 策略达到 90% 的成功率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.12352v1](https://arxiv.org/abs/2606.12352v1)
