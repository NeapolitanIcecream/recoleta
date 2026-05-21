---
source: arxiv
url: https://arxiv.org/abs/2605.03821v1
published_at: '2026-05-05T14:49:00'
authors:
- Hao Wu
- Yuqi Li
- Yuan Gao
- Fan Xu
- Fan Zhang
- Kun Wang
- Penghao Zhao
- Qiufeng Wang
- Yizhou Zhao
- Weiyan Wang
- Yingli Tian
- Xian Wu
- Xiaomeng Huang
topics:
- robot-world-models
- reward-alignment
- video-generation
- multimodal-judge
- long-horizon-prediction
- robot-data-scaling
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# RoboAlign-R1: Distilled Multimodal Reward Alignment for Robot Video World Models

## Summary
## 摘要
RoboAlign-R1 通过蒸馏后的多模态奖励训练机器人视频世界模型，并在推理时刷新长时域 rollout，从而提升模型表现。论文报告称，该方法在 RobotWorldBench、RT-1 和 BridgeData V2 上改善了任务对齐、物理真实感和像素指标。

## 问题
- 机器人视频世界模型通常使用重建、MSE、LPIPS 或 SSIM 损失训练，这些目标可能遗漏指令遵循、操作成功、接触质量和物理一致性。
- 长自回归 rollout 会累积 token 级错误，因此视频预测可能随时间漂移，并降低其对规划的可用性。
- 多模态评判器可以为高层机器人行为打分，但 8B 评判器直接用作在线 RL 奖励时速度太慢、成本太高。

## 方法
- 作者用来自 RT-1、BridgeData V2、CALVIN 和 LIBERO 的 10,000 个带标注视频-指令对构建 RobotWorldBench。
- 他们将 Qwen3-VL-8B-Thinking 微调为 RoboAlign-Judge，用六个维度评估生成的机器人视频：指令遵循、操作成功、动作-结果一致性、时间一致性、接触真实感和物理遵循。
- 他们将 8B 评判器蒸馏为一个 98M 学生奖励模型，该模型约每秒可评估 50 个视频，并为 GRPO 后训练提供奖励。
- 机器人视频模型使用 token 化的动作条件视频序列：上下文 token、动力学 token 和离散化动作 token 由一个 12 层 LLaMA 解码器建模。
- Sliding Window Re-encoding 每 W 步解码最后一个预测帧，将其重新编码为新的上下文，并用更短的活动历史继续生成。

## 结果
- 在 RobotWorldBench 上，RoboAlign-R1 的总分为 8.52±0.15，iVideoGPT 为 7.74±0.62；论文报告称相对最佳基线提升 +10.1%，且分数方差更低。
- 它在全部六个评判维度上领先：指令遵循 2.72±0.06、操作 1.72±0.07、动作-结果 0.72±0.05、时间 0.78±0.05、接触 1.00±0.04、物理 1.58±0.07。
- 摘要报告称，在域内评估协议下，相对最强基线，Manipulation Accuracy 提升 +7.5%，Instruction Following 提升 +4.6%。
- 在像素指标上，论文报告称，相比各自的次优方法，RT-1 上 LPIPS 降低 4.9%，BridgeData V2 上 MSE 降低 8.7%。
- Sliding Window Re-encoding 带来 +2.8% SSIM、+0.62 dB PSNR、-9.8% LPIPS、-12.2% ROI-LPIPS，延迟约增加 +1%。
- 与直接使用 8B 教师评判器相比，奖励蒸馏将在线奖励成本降低 10 倍以上；主要排名也通过外部 VLM 和盲法人工研究进行了核查。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.03821v1](https://arxiv.org/abs/2605.03821v1)
