---
source: arxiv
url: https://arxiv.org/abs/2605.02739v1
published_at: '2026-05-04T15:37:55'
authors:
- Yudong Liu
- Yuan Li
- Zijia Tang
- Yuxi Zheng
- Yueqian Lin
- Qinsi Wang
- Yi Li
- Shuangjun Liu
- Shuai Zhang
- Taotao Jing
- Dashan Gao
- Ning Bi
- Jingwei Sun
- Yiran Chen
- Hai Li
topics:
- vision-language-action
- generalist-robot-policy
- robot-inference
- latent-dynamics
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Latent Bridge: Feature Delta Prediction for Efficient Dual-System Vision-Language-Action Model Inference

## Summary
## 摘要
Latent Bridge 通过在完整骨干网络调用之间预测下一个 VLM 特征或 KV-cache 状态，加速双系统视觉-语言-动作模型。它在减少大量 VLM 调用的同时，使成功率接近同步推理。

## 问题
- GR00T-N1.6 和 $\pi_{0.5}$ 等双系统 VLA 在每个机器人控制步都运行大型 VLM 骨干网络，而该骨干网络是主要延迟来源。
- 连续 VLM 输出随时间变化很小，因此在实时操作中反复完整调用骨干网络会浪费计算。
- 更低延迟很重要，因为机器人策略通常需要 10-50 Hz 控制，推理缓慢可能拉长回合或降低任务成功率。

## 方法
- 该方法训练一个小型桥接模型来预测特征增量：把学习到的变化 $\Delta_t$ 加到最新 VLM 特征上，而不是再次运行 VLM。
- 对于 GR00T，桥接模型预测动作头使用的特征空间增量；对于 $\pi_{0.5}$，它预测逐层 KV-cache 增量。
- 桥接模型使用缓存的稳定视觉上下文、机器人状态和上一动作。它复制近乎恒定的文本 token，而不是预测这些 token。
- VLM 每 $f=2$ 到 $4$ 步运行一次。在跳过的步骤中，动作头使用桥接模型预测的特征。
- 训练先使用同步 VLM rollout，然后进行一轮 DAgger 精炼：桥接模型在仿真中行动，VLM 沿桥接模型产生的轨迹提供特征目标。

## 结果
- 论文称，在 LIBERO、RoboCasa 和 ALOHA 仿真上，VLM 调用减少 50-75%，任务性能保留 95-100%。
- 在使用 GR00T-N1.6-3B 的四个 LIBERO 套件上，同步推理的平均成功率为 96.58%，每步 90 ms。Latent Bridge 达到 94.54%，每步 49 ms，净回合加速为 1.73x。
- 在使用 $\pi_{0.5}$ 的四个 LIBERO 套件上，同步推理的平均成功率为 96.96%，每步 76 ms。Latent Bridge 达到 96.92%，每步 46 ms，净回合加速为 1.65x。
- 被替换的 VLM 骨干网络每次调用耗时 46-63 ms；桥接步骤在 GR00T 上耗时 2 ms，在 $\pi_{0.5}$ 上耗时 6 ms。
- 特征缓存弱得多：在匹配的跳步设置下，GR00T 的 LIBERO 平均成功率为 34.25%，$\pi_{0.5}$ 为 56.38%。
- 跨基准测试报告称，24 个 RoboCasa 任务成功率为 63.16%，同步为 66.22%；ALOHA transfer-cube 成功率为 86.00%，同步为 88.00%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02739v1](https://arxiv.org/abs/2605.02739v1)
