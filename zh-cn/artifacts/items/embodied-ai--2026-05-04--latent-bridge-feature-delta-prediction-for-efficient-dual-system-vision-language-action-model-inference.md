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
Latent Bridge 通过在两次完整骨干网络调用之间预测下一步 VLM 特征或 KV-cache 状态，加速双系统视觉-语言-动作模型。它在保持成功率接近同步推理的同时，减少了大量 VLM 调用。

## 问题
- GR00T-N1.6 和 $\pi_{0.5}$ 这类双系统 VLA 在每个机器人控制步都要运行大型 VLM 骨干网络，而这部分占据了主要延迟。
- 连续的 VLM 输出随时间变化很小，因此在实时操作中反复完整调用骨干网络会浪费算力。
- 低延迟很重要，因为机器人策略通常需要 10-50 Hz 的控制频率，推理过慢会拉长任务时长，或降低任务成功率。

## 方法
- 该方法训练一个小型 bridge 模型来预测特征增量：不再重新运行 VLM，而是在最新 VLM 特征上加上学到的变化 $\Delta_t$。
- 对 GR00T，bridge 预测动作头使用的特征空间增量；对 $\pi_{0.5}$，它预测逐层 KV-cache 增量。
- bridge 使用缓存的稳定视觉上下文、机器人状态和上一步动作。文本 token 如果几乎不变，就直接复制，不去预测。
- VLM 每隔 $f=2$ 到 $4$ 步运行一次。在跳过的步骤上，动作头使用 bridge 预测的特征。
- 训练先用同步 VLM rollout，再做一轮 DAgger 微调。bridge 在仿真中执行，VLM 沿着 bridge 诱导的轨迹提供特征目标。

## 结果
- 论文报告，在 LIBERO、RoboCasa 和 ALOHA 仿真任务上，VLM 调用减少 50-75%，任务性能保留率为 95-100%。
- 在使用 GR00T-N1.6-3B 的四个 LIBERO 套件上，同步推理的平均成功率为 96.58%，每步 90 ms。Latent Bridge 的平均成功率为 94.54%，每步 49 ms，单回合净加速 1.73 倍。
- 在使用 $\pi_{0.5}$ 的四个 LIBERO 套件上，同步推理的平均成功率为 96.96%，每步 76 ms。Latent Bridge 的平均成功率为 96.92%，每步 46 ms，单回合净加速 1.65 倍。
- 被替换的 VLM 骨干网络每次调用耗时 46-63 ms；bridge 步骤在 GR00T 上耗时 2 ms，在 $\pi_{0.5}$ 上耗时 6 ms。
- 特征缓存的效果弱得多：在相同跳步设置下，GR00T 的 LIBERO 平均成功率为 34.25%，$\pi_{0.5}$ 为 56.38%。
- 跨基准测试中，24 个 RoboCasa 任务的成功率为 63.16%，而同步推理为 66.22%；ALOHA transfer-cube 的成功率为 86.00%，同步推理为 88.00%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02739v1](https://arxiv.org/abs/2605.02739v1)
