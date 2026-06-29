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
VLAJS 用一个预训练的视觉-语言-动作模型来加快机器人操作中的强化学习。它在训练早期提供稀疏的动作提示，然后逐步移除这些提示，让 RL 策略继续自行改进。

## 问题
- 面向机器人操作的 on-policy RL 在长时程任务和稀疏或奖励塑形较差的任务上学习很慢，因为探索和信用分配都不够好。
- 视觉-语言-动作模型包含有用的任务先验，但它们控制频率低，依赖预训练数据，也不适合作为精细闭环操作的直接控制器。
- 这篇论文要解决的问题是：如何利用 VLA 知识提高 RL 的样本效率，同时又不让策略一直模仿教师。

## 方法
- 该方法 **VLAJS** 在 PPO 上加入来自预训练 VLA 教师（例如 OpenVLA）的稀疏指导。
- 教师每次 rollout 只查询少数几次，最多占 rollout 步数的 20%。每个低频教师动作会被扩展为接下来几个控制步的短期指导目标。
- VLAJS 不用 MSE 去匹配教师动作，而是使用 **方向一致性损失**：它用余弦相似度在平移和旋转方向上对齐 RL 策略与教师，同时让 PPO 决定动作幅度。
- 指导是 **短暂的**。随着 rollout 奖励提升，查询率和辅助损失权重会衰减；当最近的奖励提升呈单调增长且超过 3 的阈值时，指导会永久关闭。
- 学到的控制器仍然是一个高频、基于状态的 PPO 策略。教师动作不会被直接执行到环境里。

## 结果
- 在 **6 个 ManiSkill 操作任务** 上评估：lifting、pick-and-place、peg reorientation、peg insertion、poking 和 pushing，其中一部分迁移到 **真实的 Franka Panda** 机器人上。
- 论文称 VLAJS **持续优于 PPO 和蒸馏式基线**，并且在多个任务上把所需环境交互次数减少了 **超过 50%**。
- 在长时程实验中，任务时长增加了 **10 倍**，稀疏教师查询仍然可行；标准的密集 RPD 被省略，因为训练时间太高。
- 教师使用的是 **OpenVLA-best**，作为单独的指导来源，平均成功率约为 **40%**。
- 真实世界测试声称实现了 **零样本仿真到真实迁移**，并且对杂乱环境、物体变化、背景变化和外部扰动有较强鲁棒性。
- 这段摘要 **没有给出主结果表中 SR at t*、AUC 或逐任务基线差距的数值**，所以这里能确认的最强定量结论是：在多个任务上，环境交互次数减少了 **超过 50%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13733v1](http://arxiv.org/abs/2604.13733v1)
