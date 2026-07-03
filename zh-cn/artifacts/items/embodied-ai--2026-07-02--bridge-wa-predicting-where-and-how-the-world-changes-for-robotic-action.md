---
source: arxiv
url: https://arxiv.org/abs/2607.02195v1
published_at: '2026-07-02T14:03:44'
authors:
- Yongjie Bai
- Hanting Wang
- Mingtong Dai
- Qijun Zhong
- Yang Liu
- Liang Lin
topics:
- vision-language-action
- robot-world-models
- world-prior-distillation
- manipulation
- real-robot-evaluation
- ood-generalization
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Bridge-WA: Predicting Where and How the World Changes for Robotic Action

## Summary
## 概要
Bridge-WA 为视觉-语言-动作机器人策略加入紧凑的未来变化先验。它预测预期结果、可能变化的像素和局部运动，然后用这些信号指导动作生成，部署时不运行 5B teacher。

## 问题
- 许多 VLA 机器人策略把当前图像、语言和机器人状态直接映射到动作，因此可能漏掉接触后场景应如何变化。
- 稠密图像或视频世界模型会增加训练和推理成本，并把容量花在背景、光照和其他不指导控制的像素上。
- 这会影响操作任务，因为成功通常取决于与动作相关的变化区域和运动方向，尤其是在视觉变化和干扰物存在时。

## 方法
- 作者在 BridgeData V2 操作轨迹上，基于 Wan2.2-5B 生成式骨干网络预训练了一个以机器人状态为条件的未来变化 teacher。
- 冻结的 teacher 为策略训练生成三个缓存目标：表示预期结果的 future tokens、表示场景应在何处变化的 change maps，以及表示变化区域应如何移动的 motion-flow maps。
- 一个轻量预测器从当前 RGB 视图、本体感知和语言中学习这三个先验。
- WorldBridge 通过注意力记忆以及 change 或 flow 注意力偏置，把预测先验注入动作 transformer。
- 推理时移除 teacher 和缓存；部署的策略只运行预测器和条件化后的动作 transformer。

## 结果
- 在 VLABench 上，Bridge-WA 报告的平均成功率为 52.8%；最强的已列 SR 基线是带 delta chunks 的 pi0-Fast，为 43.1%，Bridge-WA 高出 9.7 个百分点。
- 在 VLABench 意图和进度指标上，Bridge-WA 报告的平均 IS 为 71.2%，平均 PS 为 64.0%；X-VLA 报告的 IS 为 70.2%，PS 为 51.2%。
- 在 RoboTwin 2.0 上，Bridge-WA 在 15 任务子集上报告的 Easy 成功率为 79.7%，Hard 成功率为 37.7%；其 Easy/Hard 均值为 58.7%，X-VLA 为 52.3%。
- 在 LIBERO-Plus 零样本评估上，Bridge-WA 报告的平均成功率为 72.1%，高于 OpenVLA-OFT 的 69.6% 和 RIPT-VLA 的 68.4%；它在 Camera 扰动上较弱，为 25.0%。
- 在包含 5 个任务且每个任务 50 个演示的 Dobot 真实机器人套件上，Bridge-WA 报告的 Easy 平均成功率为 73.6%，Hard 平均成功率为 69.1%；X-VLA 分别为 69.6% Easy 和 58.0% Hard。
- 在 Dobot hard-track 平均值中，Bridge-WA 在干扰物条件下报告 62.8%，在光照变化下报告 74.0%，在桌布变化下报告 70.4%；X-VLA 分别报告 53.2%、65.2% 和 55.6%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.02195v1](https://arxiv.org/abs/2607.02195v1)
