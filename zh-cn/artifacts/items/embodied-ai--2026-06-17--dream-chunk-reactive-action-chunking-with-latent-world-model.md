---
source: arxiv
url: https://arxiv.org/abs/2606.18589v1
published_at: '2026-06-17T01:28:07'
authors:
- Wenxi Chen
- Kaidi Zhang
- Chi Lin
- Zhiyuan Zhang
- Yu She
- Yuejiang Liu
- Raymond A. Yeh
- Shaoshuai Mou
- Yan Gu
topics:
- vision-language-action
- action-chunking
- latent-world-model
- test-time-scaling
- robot-manipulation
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# DREAM-Chunk: Reactive Action Chunking with Latent World Model

## Summary
## 摘要
DREAM-Chunk 通过在测试时采样多个动作块，并用潜在世界模型选择预测状态最接近真实机器人状态的动作块，提升采用动作分块的 VLA 策略。它面向随机动力学、硬件误差、部分可观测性和扰动，不需要微调基础策略。

## 问题
- 动作分块策略在一次 VLA 推理后执行多个动作，因此当机器人或环境在执行中偏离时，后续动作可能过时。
- 这会影响长时程操作任务，因为执行噪声、移动物体和外部扰动可能让开环动作块错过抓取点、端口或插入目标。
- 现有修复方法通常会更频繁地重新规划、修改策略或加入测试时优化；DREAM-Chunk 保持基础 VLA 不变，使用额外的推理时采样和一个小型世界模型。

## 方法
- 在每个重新规划步骤，该方法从冻结的分块策略中采样 N 个候选动作块。
- 一个轻量编码器将每个观测映射到潜在状态，潜在动力学模型预测每个候选动作块导致的未来潜在状态。
- 执行期间，机器人编码当前观测，并将其与相位对齐的预测潜在状态比较。
- 它执行预测潜在状态最近的候选动作块中的动作，因此当实际 rollout 发生偏移时可以切换动作块。
- 该方法依赖策略在其采样动作分布中包含有用的纠正行为；它在采样到的行为中选择，不生成新行为。

## 结果
- 在 Kinetix 中，论文报告 N 增大时，在动作噪声下的求解率更高，结果在 12 个环境上取平均；摘录没有给出图中的确切求解率数值。
- 在 Kinetix 动作噪声 σ=0.3 下，当示范来自用更高动作噪声训练的专家时，DREAM-Chunk 从更大采样数量中获得的收益更大；σ=0.1 等低噪声专家数据带来的收益较小。
- 在 Kinetix 消融实验中，当 σ=0.2 且 N=20 时，RSSM 风格的 R2-Dreamer 和 LEWM 潜在模型优于 EB-JEPA 和冻结策略编码器变体；摘录没有给出这些曲线的确切数值分数。
- 在硬件上，论文使用 SmolVLA 和 π0.5，在 SO-101 和 Franka Panda 两个平台上测试 4 个操作任务，每个任务约有 50 到 100 条遥操作示范。
- 在外部扰动下的精密插入任务中，DREAM-Chunk 将开环 π0.5 成功率从 10% 提高到 65%。
- 辅助模型比 VLA 小得多、快得多：JEPA 世界模型可以有 15M 参数，SmolVLA 约有 450M 参数，π0.5 超过 2B 参数，VLA 推理耗时超过 100 ms，世界模型编码加预测耗时少于 10 ms。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.18589v1](https://arxiv.org/abs/2606.18589v1)
