---
source: arxiv
url: https://arxiv.org/abs/2607.02092v1
published_at: '2026-07-02T12:30:50'
authors:
- Liuhaichen Yang
- Zhuang Jiang
- Chenchao Sheng
- Zezhi Tang
topics:
- vision-language-action
- flow-matching
- q-guided-inference
- robot-manipulation
- critic-guidance
- libero
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Guided Action Flow: Q-Guided Inference for Flow-Matching Vision-Language-Action Policies

## Summary
## 摘要
Guided Action Flow 为冻结的 SmolVLA 流匹配 VLA 策略加入测试时 Q 引导。一个学习得到的动作块评论器在推理时引导采样器，并在单任务和验证设置中提高了 LIBERO 成功率，但在锁定留出测试上的提升很小。

## 问题
- 冻结的 VLA 机器人策略在分布偏移、早期动作错误，或局部看似合理但无法完成任务的动作块之后，可能会失败。
- 当只有少量任务局部 rollout 数据可用时，完整的 VLA 微调成本可能很高，也难以验证。
- 论文研究的是：一个用成功和失败 rollout 训练的小评论器，能否在不改变冻结流匹配 VLA 权重的情况下改进它。

## 方法
- 基础策略是官方 SmolVLA LIBERO checkpoint，在所有 QGF 实验中都保持冻结。
- 该方法在 rollout 动作块上训练一个 MLP 评论器。评论器接收策略侧观察特征、候选动作块和可选的任务描述特征，然后预测稀疏的后续成功值。
- 在 SmolVLA 反向时间采样期间，该方法将干净动作块估计为 `a_hat = x_t - t v_t`，计算评论器相对于该动作块的梯度，对梯度进行裁剪，用评论器集成的分歧进行门控，并调整流速度。
- 由 3 个评论器组成的集成通过价值分歧提供不确定性。高分歧会减少引导，同时最小门控会保留少量有效的引导信号。
- 最强的评论器变体以冻结的 SmolVLA VLM 隐状态任务特征为条件，使用基础策略的语言路径，而不训练新的文本编码器。

## 结果
- 冻结 SmolVLA 基线锚点：LIBERO vanilla 达到 65/100 成功率（65.0%），LIBERO-Plus 空间子集达到 39/50（78.0%），LIBERO-PRO zero-shot 达到 1/100（1.0%）。
- 单任务 QGF 在 seed window 3000 上将一个 LIBERO 空间任务从 34/50（68.0%）提高到 41/50（82.0%），提升 +14.0 个百分点。
- 在同一单任务设置的 seed window 4000 上，QGF 将成功率从 41/50（82.0%）提高到 43/50（86.0%），提升 +4.0 个百分点。
- 仅空间迁移评论器未能迁移：验证成功率最高为 31/60（51.7%），而基线为 32/60（53.3%），至少下降 -1.7 个百分点。
- 多族任务描述评论器将验证成功率从 23/50（46.0%）提高到 28/50（56.0%），提升 +10.0 个百分点。
- 在锁定留出测试上，多族任务描述评论器将成功率从 26/40（65.0%）提高到 27/40（67.5%），提升 +2.5 个百分点，显示出正向但有限的泛化。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.02092v1](https://arxiv.org/abs/2607.02092v1)
