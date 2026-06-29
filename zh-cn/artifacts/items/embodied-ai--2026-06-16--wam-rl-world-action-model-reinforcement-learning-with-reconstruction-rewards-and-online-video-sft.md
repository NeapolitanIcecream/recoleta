---
source: arxiv
url: https://arxiv.org/abs/2606.17906v1
published_at: '2026-06-16T13:29:12'
authors:
- Zezhong Qian
- Xiaowei Chi
- Yu Qi
- Haozhan Li
- Zhi Yang Chen
- Shanghang Zhang
topics:
- world-action-model
- robot-rl
- world-model-adaptation
- reconstruction-rewards
- long-horizon-manipulation
- libero-rlbench
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# WAM-RL: World-Action Model Reinforcement Learning with Reconstruction Rewards and Online Video SFT

## Summary
## 摘要
WAM-RL 在在线交互中同时训练 World-Action 机器人策略的两个部分：视频世界模型和动作模型。这一点很关键，因为只用演示数据训练的 WA 模型，在演示数据之外的精细操作、错误恢复和长时程任务上表现受限。

## 问题
- 现有 WA 模型依赖专家轨迹，因此策略会贴近演示数据支撑范围，学到的精细技能有限。
- 只对 actor 做 RL 可以提升短时程任务表现，但长时程成功率仍受世界模型预测误差限制。
- 在线更新世界模型会改变潜在特征，并破坏 actor 已学到的从潜在预测到动作的映射。

## 方法
- 该方法基于 Genie Envisioner-ACT，使用 DiT 视频生成器作为世界模型，并使用一个 actor 读取中间潜在特征并输出机器人动作。
- 在 rollout 期间，世界模型预测未来观测，actor 执行动作，真实观测用于更新两个模块。
- 世界模型使用成功轨迹做在线视频 SFT，并加入 KL 正则化，使潜在特征接近一个冻结的预训练副本。
- actor 使用策略梯度优化，奖励为重建奖励，用于比较想象的未来观测和执行后的未来观测。
- 测试的奖励变体包括 pixel MSE、optical flow MSE、DINO feature MSE 和 V-JEPA2 feature similarity；Flow-SDE 为基于 flow 的 actor 提供随机去噪转移和动作似然。

## 结果
- 在 LIBERO-Object 上，成功率从 Base 模型的 68% 提升到 WAM-RL 的 82%；仅 actor 的 π_RL 达到 78%。
- 在 RLBench Water Plants 上，成功率从 Base 的 19% 提升到 WAM-RL 的 22%；仅 actor 的 π_RL 达到 18%。
- 在 RLBench Water Plants 奖励消融中，Pixel MSE 达到 21%，Optical Flow MSE 为 19%，DINO MSE 为 16%，V-JEPA2 为 17%；相比之下，Base 为 19%，仅 actor 的 π_RL 为 18%。
- 训练使用 8 块 NVIDIA A800 GPU，耗时 8 小时，采用混合在线 RL 和视频微调。
- 论文报告了在线视频 SFT 后的定性恢复行为，例如夹爪重新定位，以及抓取失败后的重新抓取；摘录未给出恢复率的数值指标。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.17906v1](https://arxiv.org/abs/2606.17906v1)
