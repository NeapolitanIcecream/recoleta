---
source: arxiv
url: https://arxiv.org/abs/2606.31846v1
published_at: '2026-06-30T15:46:57'
authors:
- Lang Cao
- Renhong Chen
- Luyi Li
- Peng Wang
- Mofan Peng
- Yitong Li
topics:
- vision-language-action
- robot-reinforcement-learning
- grpo
- robocasa
- robot-policy-post-training
- manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Z-1: Efficient Reinforcement Learning for Vision-Language-Action Models

## Summary
## 摘要
Z-1 是一种面向基于流的视觉-语言-动作机器人策略的 RL 后训练方法，构建在 π0.5 之上，并在 24 个 RoboCasa 任务上测试。它使用公开的 RoboCasa 演示数据，将平均成功率从 SFT 后的 67.4% 提高到 GRPO 后的 80.6%。

## 问题
- 用行为克隆或 SFT 训练的 VLA 机器人策略会复制固定演示，因此长时程错误可能把机器人带到训练数据中没有覆盖的状态。
- 在线 RL 可以通过试错提高任务成功率，但基于流的 VLA rollout 成本高，稀疏奖励的信用分配弱，冻结的视觉-语言模块也可能漏掉视觉 grounding 失败。
- 这个问题重要，因为更好的后训练可以在不增加私有演示数据的情况下改进机器人操作。

## 方法
- Z-1 从预训练的 π0.5 策略开始，在 1,199 条公开 RoboCasa 演示上进行按场景 SFT，然后进行按任务 GRPO 后训练。
- Shared-Prefix GRPO 先运行一次共同的接近阶段前缀，克隆模拟器状态，再采样不同后缀，使组内比较集中在操作阶段。
- Tree-Structured Prefix Branching 在前缀内部加入中间分支点，相比扁平的共享前缀，可让更多接近阶段的动作块参与训练。
- Success-Aware Reward Decay 给更早成功完成的轨迹更高的校准奖励，同时保持失败 rollout 不变。
- Selective VLM-Action Expert 联合训练只在 action-expert-only GRPO 表现较弱的任务上更新视觉-语言主干，依据是最终评估前的训练诊断。

## 结果
- 在 24 个 RoboCasa 任务上，Z-1 RL 报告的平均成功率为 80.6%，高于 Z-1 SFT 的 67.4%，提升 +13.2 个百分点。
- 它报告的平均成功率比 GR00T 高 +30.9 个百分点，比 GR00T N1.5 高 +20.9 个百分点，比 Video Policy 高 +17.3 个百分点，比 X-WAM 高 +1.4 个百分点。
- 与 X-WAM 相比，论文报告 Z-1 RL 为 80.6%，X-WAM 为 79.2%，Z-1 在 7 个任务类别中的 5 个领先。
- 相比 Z-1 SFT，各类别的提升包括：门任务从 93.2% 到 97.0%，抽屉任务从 83.4% 到 96.1%，水槽/水龙头任务从 63.2% 到 94.3%。
- 该比较使用的是既有论文报告的数字，而不是完全受控的复现实验，因此最强的受控结果是相对作者自己 SFT 初始化的 +13.2 个百分点提升。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.31846v1](https://arxiv.org/abs/2606.31846v1)
