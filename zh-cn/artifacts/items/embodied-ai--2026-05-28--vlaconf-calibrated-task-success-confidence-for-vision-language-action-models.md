---
source: arxiv
url: https://arxiv.org/abs/2605.29605v1
published_at: '2026-05-28T08:42:12'
authors:
- Dehao Huang
- Aoxiang Gu
- Chengjie Zhang
- Bolin Zou
- Wenlong Dong
- Zilang Cen
- Yue Wang
- Hong Zhang
topics:
- vision-language-action
- robot-confidence
- uncertainty-calibration
- failure-detection
- manipulation
- libero
relevance_score: 0.87
run_id: materialize-outputs
language_code: zh-CN
---

# VLAConf: Calibrated Task-Success Confidence for Vision-Language-Action Models

## Summary
## 摘要
VLAConf 通过在冻结的 VLA 特征上训练一个仅用成功样本的置信度头，来估计 VLA 机器人策略的任务成功置信度。它面向更快的置信度查询，并支持离散动作和连续动作的 VLA 主干。

## 问题
- 机器人需要对当前操作 rollout 是否会成功给出在线估计，这样才能在失败完成前停止、恢复、回滚或寻求帮助。
- 现有 VLA 置信度方法常用提示词集成或动作 token 概率，这会增加重复推理成本，也更适合离散动作模型，而不适合连续动作模型。
- 失败 rollout 的采集成本高且不安全，所以论文主要从成功示范中学习置信度信号。

## 方法
- VLAConf 冻结预训练 VLA，池化其视觉和语言隐藏状态，再通过小型 MLP 与本体感知状态融合。
- 用一个 Coin-Flip Network 头只在成功 rollout 的步骤上训练。它的输出范数变成异常分数：熟悉的成功状态通常分数更低，异常状态通常分数更高。
- 这个异常头会用 rollout 步骤条件化，方法是把学习到的步骤嵌入和归一化进度值一起输入，再用 FiLM 式调制和残差门控。
- 先把观测到的前缀上的步骤分数汇总，再用 Platt scaling 将标量分数映射为任务成功概率，所用数据是一小组带二元结果的完整 rollouts。

## 结果
- 在标准 LIBERO 上，使用 OpenVLA-OFT 时，VLAConf 的执行前 ECE 为 0.0340、Brier 为 0.1614、NLL 为 0.4991；ConfidenceVLA 分别为 ECE 0.0363、Brier 0.1702、NLL 0.5295。
- 对于 OpenVLA-OFT 的在线执行，VLAConf 的 Brier 为 0.1073、NLL 为 0.3335，优于 ConfidenceVLA 的 Brier 0.1647 和 NLL 0.5041，但其 ECE 为 0.1188，差于 0.0276。
- 在 OpenVLA-OFT 上，VLAConf 比 ConfidenceVLA 快得多：平均推理时间 64.9 ms，对比 712.9 ms，约快 11 倍。
- 在连续动作的 π^0.5 主干上，因为 ConfidenceVLA 依赖动作 token 概率，所以没有报告该方法；VLAConf 报告的执行前 ECE 为 0.0370、Brier 为 0.0821、NLL 为 0.3141。
- 在 π^0.5 的在线执行中，VLAConf 的 ECE 为 0.0515、Brier 为 0.0668、NLL 为 0.2501；对比 VLAConf-NoStep 的 ECE 0.0448、Brier 0.0884、NLL 0.3261。
- 报告的策略成功率是：在平均后的标准 LIBERO 套件上，OpenVLA-OFT 配合 VLAConf 为 78.2%，π^0.5 配合 VLAConf 为 91.3%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.29605v1](https://arxiv.org/abs/2605.29605v1)
