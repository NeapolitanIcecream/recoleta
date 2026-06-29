---
source: arxiv
url: https://arxiv.org/abs/2606.06245v1
published_at: '2026-06-04T14:48:44'
authors:
- Boyang Zhang
- Lianlei Shan
topics:
- vision-language-action
- latent-reasoning
- test-time-scaling
- robot-manipulation
- long-horizon-control
- world-model-supervision
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# MPCoT: Reward-Guided Multi-Path Latent Reasoning for Test-Time Scalable Vision-Language-Action

## Summary
## 摘要
MPCoT 为长时程视觉-语言-动作控制给 OpenVLA-OFT 加入了测试时 latent 推理。它声称在保持相同的 8 步动作输出且不生成推理 token 的情况下，提高了 LIBERO 和 CALVIN 的成功率。

## 问题
- VLA 策略通常一次性解码动作，面对长指令链时，几乎没有空间修正不确定的选择。
- 显式 chain-of-thought 可以增加推理深度，但会带来 token 延迟，并把连续控制转成文本接口。
- 这个问题会放大早期机器人动作错误，因为它们会在多步操作任务中累积。

## 方法
- MPCoT 从同一观测和语言指令出发，先生成 M 个 latent 动作假设。
- 共享的残差细化器对每个假设更新 K 步，因此更大的 K 只增加计算量，不增加细化器参数。
- 一个学习到的评分器给这 M 个细化后的假设分配软权重，然后模型在不改动的 OpenVLA-OFT 动作头之前对它们求平均。
- 训练时，候选分支会收到路径偏好监督，信号来自专家动作一致性、world-model/VLM 的进展和成功反馈。
- 推理时，MPCoT 只使用学习到的 latent 评分器；它不会查询奖励、成功标签、rollout 或 world-model/VLM 评估器。

## 结果
- 在 LIBERO 上，用一个策略覆盖全部 4 个 suite 时，MPCoT 将 OpenVLA-OFT 的平均成功率从 96.8% 提升到 98.9%，将 Long 成功率从 95.3% 提升到 98.9%。
- 在 LIBERO 上，每个 suite 用一个策略时，MPCoT 达到 99.0% 的平均成功率和 97.8% 的 Long 成功率；AVA-VLA 的对应结果是 98.3% 和 96.2%。
- 在 CALVIN ABC→D 上，MPCoT 对 1 步到 5 步链的成功率分别达到 99.8%、98.9%、96.8%、93.7% 和 89.4%，平均序列长度为 4.92。
- 在 CALVIN 的 4 步和 5 步任务上，MPCoT 分别比 AVA-VLA 高 3.8 和 5.3 个百分点，也比 OpenVLA-OFT 高 13.3 和 16.5 个百分点。
- 最好的固定设置 K=5、M=4，把 LIBERO Long 从 95.3% 提高到 98.9%，同时把测得延迟从 24 ms 增加到 38 ms，并且没有额外的 reasoning token 开销。
- Reward-guided 的路径监督把 Path Consistency 从 68.5% 提高到 84.3%，并且和不带奖励的 multi-path 版本相比，把 CALVIN 4 步成功率从 90.8% 提高到 93.7%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.06245v1](https://arxiv.org/abs/2606.06245v1)
