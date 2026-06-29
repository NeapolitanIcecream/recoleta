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
RoboAlign-R1 通过蒸馏的多模态奖励训练机器人视频世界模型，并在推理时刷新长时域 rollout，从而提升性能。论文报告了在 RobotWorldBench、RT-1 和 BridgeData V2 上更好的任务对齐、物理真实性和像素指标。

## 问题
- 机器人视频世界模型通常用重建、MSE、LPIPS 或 SSIM 损失训练，这些目标会漏掉指令遵循、操作成功率、接触质量和物理一致性。
- 长自回归 rollout 会累积 token 级错误，视频预测会随时间漂移，规划价值下降。
- 多模态裁判可以评估机器人高层行为，但 8B 裁判直接用于在线 RL 奖励时速度太慢、成本太高。

## 方法
- 作者构建了 RobotWorldBench，包含来自 RT-1、BridgeData V2、CALVIN 和 LIBERO 的 10,000 对带标注的视频-指令样本。
- 他们将 Qwen3-VL-8B-Thinking 微调为 RoboAlign-Judge，用六个维度给生成的机器人视频打分：指令遵循、操作成功、动作-结果一致性、时间一致性、接触真实性和物理遵循。
- 他们把这个 8B 裁判蒸馏成一个 9800 万参数的学生奖励模型，每秒可打分约 50 个视频，并为 GRPO 后训练提供奖励。
- 机器人视频模型使用带动作条件的 token 化视频序列：上下文 token、动力学 token 和离散化动作 token 由一个 12 层 LLaMA 解码器建模。
- Sliding Window Re-encoding 每隔 W 步解码最近预测帧，再把它重新编码为新的上下文，用更短的活动历史继续生成。

## 结果
- 在 RobotWorldBench 上，RoboAlign-R1 的总分为 8.52±0.15，iVideoGPT 为 7.74±0.62。论文报告这比最强基线高 10.1%，且分数方差更低。
- 它在六个裁判维度上都领先：指令遵循 2.72±0.06、操作 1.72±0.07、动作-结果 0.72±0.05、时间一致性 0.78±0.05、接触 1.00±0.04、物理 1.58±0.07。
- 摘要报告，在域内评估协议下，操控准确率比最强基线高 7.5%，指令遵循高 4.6%。
- 在像素指标上，论文报告 RT-1 的 LPIPS 降低 4.9%，BridgeData V2 的 MSE 相比各自次优结果降低 8.7%。
- Sliding Window Re-encoding 带来 +2.8% SSIM、+0.62 dB PSNR、-9.8% LPIPS、-12.2% ROI-LPIPS，延迟约增加 1%。
- 奖励蒸馏把在线奖励成本降到直接使用 8B 教师裁判的 1/10 以上，同时主排名还经过外部 VLM 和盲审人类研究核对。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.03821v1](https://arxiv.org/abs/2605.03821v1)
