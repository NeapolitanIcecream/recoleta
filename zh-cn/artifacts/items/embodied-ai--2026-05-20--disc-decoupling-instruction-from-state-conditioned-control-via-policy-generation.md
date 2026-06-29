---
source: arxiv
url: https://arxiv.org/abs/2605.20856v1
published_at: '2026-05-20T07:45:50'
authors:
- Hanxiang Ren
- Pei Zhou
- Xunzhe Zhou
- Yanchao Yang
topics:
- vision-language-action
- generalist-robot-policy
- robot-data-scaling
- dexterous-manipulation
- language-grounding
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# DISC: Decoupling Instruction from State-Conditioned Control via Policy Generation

## Summary
## 摘要
DISC 让语言指令生成一个任务专用的视觉运动策略，因此控制策略只接收观测。论文称，这种分离提升了语言对齐和机器人仿真与真实操作中的任务成功率。

## 问题
- 语言条件机器人策略常把指令 token 和观测混在共享参数里，这会让场景线索驱动动作，即使指令要求别的操作也是如此。
- 这很重要，因为机器人数据集常常复用场景和物体，所以策略可能学到场景到动作的捷径，在同一场景对应多个任务时失效。
- 长时程任务受影响更大，因为只要一个由语言条件决定的子目标出错，整个回合就可能失败。

## 方法
- DISC 用冻结的语言编码器编码指令，然后由超网络生成任务专用视觉运动策略的完整参数集。
- 生成的策略接收 RGB 和本体感觉观测，再预测动作。控制时它没有直接的语言输入。
- 这个超网络分两阶段：Weight Initialization Network 根据指令嵌入生成初始策略权重，Iterative Refinement Module 通过学习到的前馈步骤更新这些权重。
- 细化模块复现了优化过程的形式，使用学习到的前向、伪梯度和更新操作，但在推理时不计算梯度。
- 训练端到端使用行为克隆：动作误差通过生成的策略更新超网络。

## 结果
- 在 LIBERO-90 上，DISC 在每个任务使用 50 个示范时报告 94.3% 的成功率，比最强的从零训练、参数纠缠基线高 7.7 个百分点。
- 在 Meta-World ML45 上，DISC 在每个任务使用 100 个专家示范时报告 92.2% 的成功率。
- DISC 在 LIBERO-90 上的成功率高于预训练的 π₀，后者为 91.6%，但低于 π₀.₅ 的 95.7%。
- 在一个真实世界的 3 个物体 × 3 个容器基准上，9 个语言条件任务共享相同视觉上下文，DISC 的成功率为 86.4%，最佳纠缠基线为 78.5%。
- 论文还声称，生成的参数空间里有更好的小样本适应、改写指令处理和任务聚类，但摘要没有给出这些结论的具体数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.20856v1](https://arxiv.org/abs/2605.20856v1)
