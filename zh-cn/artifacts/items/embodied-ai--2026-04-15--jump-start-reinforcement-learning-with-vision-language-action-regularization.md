---
source: arxiv
url: http://arxiv.org/abs/2604.13733v1
published_at: '2026-04-15T11:17:54'
authors:
- Angelo Moroncelli
- Roberto Zanetti
- Marco Maccarini
- Loris Roveda
topics:
- vision-language-action
- reinforcement-learning
- robot-manipulation
- sim2real
- sample-efficiency
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Jump-Start Reinforcement Learning with Vision-Language-Action Regularization

## Summary
## 摘要
VLAJS 用一个预训练的视觉-语言-动作模型来加快机器人操作中的强化学习。它在训练早期提供稀疏的动作提示，随后移除这些提示，让 RL 策略继续自行改进。

## 问题
- 用于机器人操作的 on-policy RL 在长时程任务和奖励稀疏或设计不佳的任务上学习很慢，因为探索和信用分配效果较差。
- 视觉-语言-动作模型包含有用的任务先验，但它们的控制频率低、依赖预训练数据，不能直接作为精确闭环操作的控制器使用。
- 论文关注的问题是，如何利用 VLA 的知识提高 RL 的样本效率，同时又不让策略一直模仿教师模型。

## 方法
- 该方法 **VLAJS** 在 PPO 上加入了来自预训练 VLA 教师模型（如 OpenVLA）的稀疏指导。
- 教师模型在每次 rollout 中只查询少数几次，最多覆盖 20% 的 rollout 步数。每个低频教师动作会扩展为接下来几个控制步的短时指导目标。
- VLAJS 不用 MSE 去匹配教师动作，而是使用 **方向动作一致性损失**：对平移和旋转部分用余弦相似度对齐 RL 策略与教师动作的方向，同时让 PPO 自己决定动作幅度。
- 指导是 **暂时的**。随着 rollout 奖励提升，查询率和辅助损失权重会衰减；当近期奖励改进保持单调并超过 3 的阈值后，指导会被永久关闭。
- 学到的控制器仍然是一个高频、基于状态的 PPO 策略。教师动作从不直接在环境中执行。

## 结果
- 在 **6 个 ManiSkill 操作任务**上评估：lifting、pick-and-place、peg reorientation、peg insertion、poking 和 pushing，其中一部分迁移到了 **真实 Franka Panda** 机器人。
- 论文称，VLAJS **持续优于 PPO 和蒸馏式基线**，并且在若干任务上将所需环境交互次数降低了 **50% 以上**。
- 在长时程实验中，任务时域增加到 **10 倍**，稀疏教师查询仍然可行；标准的密集 RPD 因训练时间过高而未纳入。
- 教师模型是 **OpenVLA-best**，单独作为指导来源时，平均成功率约为 **40%**。
- 真实环境测试称其实现了 **零样本 sim-to-real 迁移**，并且对杂乱环境、物体变化、背景变化和外部扰动具有鲁棒性。
- 这段摘录 **没有给出主要结果表中的具体数值**，例如 SR at t*、AUC 或各任务与基线的差距，因此这里能得到的最强定量结论是：在若干任务上，环境交互次数减少了 **50% 以上**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13733v1](http://arxiv.org/abs/2604.13733v1)
