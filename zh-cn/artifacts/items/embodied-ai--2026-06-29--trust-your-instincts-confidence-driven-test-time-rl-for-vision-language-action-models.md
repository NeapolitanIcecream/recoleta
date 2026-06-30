---
source: arxiv
url: https://arxiv.org/abs/2606.29892v1
published_at: '2026-06-29T07:31:41'
authors:
- Siyao Chen
- Jiakang Yuan
- Jiaxin Wang
- Tao Chen
topics:
- vision-language-action
- test-time-rl
- self-rewarding
- robot-manipulation
- policy-optimization
- confidence-estimation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Trust Your Instincts: Confidence-Driven Test-Time RL for Vision-Language-Action Models

## Summary
## 摘要
T2VLA 在测试时用模型自身置信度作为奖励来源来训练 VLA 策略，因此 RL 更新不需要环境成功标签。论文报告称，在 LIBERO 上，T2VLA 提高了 OpenVLA-OFT、π0 和 π0.5 的成功率，其中 π0 的平均增益最大。

## 问题
- 现有 VLA 模型 RL 方法通常需要外部奖励，例如模拟器成功标志、人工标签或辅助模型评分。
- 机器人轨迹很难自检，因为多种不同动作序列都可能完成同一任务，所以数学或代码任务中的多数投票验证不能直接迁移。
- 这个问题会限制新机器人任务上的测试时改进，并增加机器人数据扩展的成本。

## 方法
- 该方法用模型内部置信度给每次 rollout 打分：离散动作 VLA 使用平均动作 log-probability，基于流的连续动作 VLA 使用去噪转移 log-likelihood。
- 对每条语言指令，它选择当前 batch 中置信度最高的 rollout 作为局部伪专家。
- 它维护一个按任务条件化的全局专家池，保留排名前 K 的历史局部专家；实现中 K=5。
- 它通过计算 rollout 与局部专家以及最佳匹配全局专家之间的动态时间规整（Dynamic Time Warping）相似度，把专家匹配转化为奖励。
- 它使用自奖励和相对于初始 SFT 策略的 KL 惩罚，通过 GRPO 更新策略。

## 结果
- 论文报告了在 LIBERO 上对 2,000 条 OpenVLA-OFT rollout 的置信度-成功相关性分析，其中更高的平均 log-probability 对应更高的执行成功率。
- 在 LIBERO 上，OpenVLA-OFT 的平均成功率从 91.0% 升至使用 T2VLA 后的 97.2%，增益为 +6.2 个百分点。各套件增益为 Spatial +6.1、Object +4.3、Goal +5.5、Long +8.8。
- 在 LIBERO 上，π0 的平均成功率从 57.7% 升至 81.9%，增益为 +24.2 个百分点。各套件增益为 Spatial +21.0、Object +26.6、Goal +32.2、Long +16.8。
- 在 LIBERO 上，π0.5 的平均成功率从 77.1% 升至 85.1%，增益为 +8.0 个百分点。各套件增益为 Spatial +10.3、Object +3.0、Goal +7.2、Long +11.2。
- OpenVLA-OFT 的 97.2% 平均成功率低于使用环境成功奖励的 SimpleVLA-RL 的 99.1%，但高于报告的 LIBERO 表中 OpenVLA-OFT SFT 基线的 91.0%，也高于 EVOLVE-VLA 的 95.8%。
- 摘要还称，该方法在连续动作和双臂任务上带来超过 20 个绝对百分点的增益，并且适用于 OpenVLA-OFT 和 π 系列。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.29892v1](https://arxiv.org/abs/2606.29892v1)
