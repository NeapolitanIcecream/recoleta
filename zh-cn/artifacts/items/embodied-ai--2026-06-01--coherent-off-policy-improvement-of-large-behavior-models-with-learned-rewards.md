---
source: arxiv
url: https://arxiv.org/abs/2606.02194v1
published_at: '2026-06-01T12:49:14'
authors:
- Christian Scherer
- Joe Watson
- Theo Gruner
- Daniel Palenicek
- Ingmar Posner
- Jan Peters
topics:
- vision-language-action
- robot-foundation-model
- imitation-learning
- inverse-rl
- dexterous-manipulation
- policy-finetuning
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Coherent Off-Policy Improvement of Large Behavior Models with Learned Rewards

## Summary
## 摘要
CSIL++ 使用逆强化学习和一致的学习奖励，在没有常见的 RL 早期性能下滑的情况下，改进了 pi-0.5 在稀疏奖励仿真操作任务上的表现。基于提供的摘录，这项工作与 VLA 和大型行为模型的微调相关，但证据仅限于仿真。

## 问题
- 行为克隆可以训练出用于机器人控制的强大型行为模型，但很小的轨迹误差会把机器人带到演示数据之外的状态。
- 稀疏奖励的 RL 微调会浪费样本，也可能在训练早期让预训练策略退化。
- 人工设计的稠密奖励很难适配不同的操作任务，所以论文改用演示来学习稠密奖励。

## 方法
- 该方法先用专家演示训练一个小型 BC 策略，再把它转成一致奖励：`alpha * (log pi_BC(a|s) - log p(a|s))`。
- 这个奖励会给熟悉状态中的演示动作高分，给熟悉状态中的错误动作低分，并且在未见过的状态中接近零。
- 冻结的 pi-0.5 VLA 每 10 步提出一次动作块，而一个更小的 CSIL++ 策略每一步都执行动作。
- CSIL++ 使用集成动作，把 VLA 动作和学习到的策略动作取平均，而不是加入残差修正。
- 实现里加入了 categorical critic、batch normalization、weight normalization、精确的 Gaussian KL 估计、按相机划分的图像编码器，以及 spatial softmax pooling。

## 结果
- 在 6 个仿真稀疏奖励操作任务上，CSIL++ Ensemble 在表 1 中的每个任务上都持平或优于 pi-0.5 VLA 基线。
- CSIL++ Ensemble 在 6 个任务中的 5 个上都达到至少 90% 成功率：Square 0.94、Coffee 0.96、Mug Cleanup 0.90、Threading 0.92、Hammer Cleanup 1.00。
- Threading 的提升最大：pi-0.5 VLA 只有 0.14 的成功率，而 CSIL++ Ensemble 在 450k 步时达到 0.92。
- Mug Cleanup 从 VLA 的 0.68 提升到 CSIL++ Ensemble 在 100k 步时的 0.90。
- Square 从 VLA 的 0.84 提升到 CSIL++ Ensemble 在 100k 步时的 0.94；Coffee 从 0.78 提升到 200k 步时的 0.96。
- Nut Assembly 是主要失败案例：CSIL++ Ensemble 仍为 0.22，与 VLA 基线相同，而 CSIL++ Residual 达到 0.40，XQC+OD Residual 达到 0.34。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.02194v1](https://arxiv.org/abs/2606.02194v1)
