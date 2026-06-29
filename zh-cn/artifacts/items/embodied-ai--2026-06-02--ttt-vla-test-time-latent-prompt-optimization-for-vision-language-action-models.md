---
source: arxiv
url: https://arxiv.org/abs/2606.03127v1
published_at: '2026-06-02T04:10:39'
authors:
- Wenbo Zhang
- Jianxiong Li
- Shuai Yang
- Sijin Chen
- Jiajun Liu
- Lingqiao Liu
- Xiao Ma
topics:
- vision-language-action
- test-time-training
- latent-prompt-optimization
- robot-foundation-model
- sim2real
- robot-data-scaling
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# TTT-VLA: Test-Time Latent Prompt Optimization for Vision-Language-Action Models

## Summary
## 摘要
TTT-VLA 通过优化已学习的潜在提示 token，并配合自监督的状态对齐损失，在部署时对冻结的视觉-语言-动作策略进行适配。在 SimplerEnv 上，它在 WidowX、Google Robot 和多具身设置中都提升了基于 π0.5 的成功率。

## 问题
- 在大规模机器人数据上训练的 VLA 策略，在视觉、环境或具身条件发生变化时，部署表现仍然会下降。
- 提示词引导可以改善行为，但常见方法依赖人工或外部指导，不能直接从部署交互中学习。
- 强化学习式后训练可以从交互中学习，但它需要奖励，而且通常会更新策略本身，带来成本和稳定性问题。

## 方法
- 该方法在 VLA 的条件输入中加入一个可学习的潜在提示 `z`，与观测和显式任务上下文一起使用。
- 训练时，策略同时优化常规动作损失和一个代理状态对齐损失，该损失预测末端执行器位置和夹爪状态。
- 测试时，机器人在当前环境中收集交互数据，冻结策略主干，只用状态对齐损失更新潜在提示。
- 实现采用 Mixture-of-Transformers 设计，包含动作专家和状态对齐专家，并从预训练的 π0.5 检查点初始化。
- 在多具身训练中，方法按具身类型分配提示；在单具身训练中，它使用提示-动作注意力丢弃和梯度约束，迫使提示携带有用的状态对齐上下文。

## 结果
- 在 SimplerEnv 的 WidowX 单具身任务上，平均成功率从 π0.5 的 51.1% 提升到带状态对齐潜在提示的 63.5%，测试时提示优化后提升到 67.4%。
- 在同一 WidowX 基准上，完整方法的平均成功率为 67.4%，高于表中列出的最强公开基线 CogACT 的 52.1%。
- 在 Google Robot 视觉匹配上，平均成功率从 π0.5 的 67.5% 提升到潜在提示训练的 68.9%，测试时训练后提升到 72.4%。
- 在 Google Robot 变体聚合上，平均成功率从 π0.5 的 58.1% 提升到潜在提示训练的 58.6%，测试时训练后提升到 60.1%。
- 在用 OXE-Aug Bridge V2 的九种具身进行训练、并在 WidowX 上评测的多具身设置中，平均成功率从 π0.5 的 22.8% 提升到潜在提示训练的 28.5%，测试时训练后提升到 31.6%。
- 测试时训练只更新提示：WidowX 进行 500 步优化，Google Robot 进行 1000 步，batch size 为 128，学习率为 1e-5，在 8 张 NVIDIA H100 GPU 上耗时 15–30 分钟。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.03127v1](https://arxiv.org/abs/2606.03127v1)
