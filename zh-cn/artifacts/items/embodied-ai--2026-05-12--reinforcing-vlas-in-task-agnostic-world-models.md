---
source: arxiv
url: https://arxiv.org/abs/2605.12334v1
published_at: '2026-05-12T16:16:15'
authors:
- Yucen Wang
- Rui Yu
- Fengming Zhang
- Junjie Lu
- Xinyao Qin
- Tianxiang Zhang
- Kaixin Wang
- Li Zhao
topics:
- vision-language-action
- world-model
- robot-foundation-model
- generalist-robot-policy
- robot-data-scaling
- sim2real
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# Reinforcing VLAs in Task-Agnostic World Models

## Summary
## 摘要
RAW-Dream 在冻结或轻量适配的任务无关视频世界模型中用 RL 训练 VLA 策略，并用 Qwen3-VL 作为零样奖励评判器。论文的核心主张是，广泛的玩耍式机器人数据可以替代新操作任务中针对具体任务的世界模型和奖励模型训练。

## 问题
- 现有用于 VLA 的世界模型 RL 方法通常在目标任务 rollout 上训练世界模型和奖励模型，往往需要数千条轨迹。
- 这种数据需求削弱了想象式 RL 的主要收益，因为每个新任务在训练开始前仍需要新的机器人数据。
- 这个问题会影响机器人基础模型，因为部署时常会遇到世界模型训练中没有出现过的新物体、新布局和新指令。

## 方法
- RAW-Dream 在广泛的无任务机器人行为上预训练动作条件视频世界模型，例如玩耍数据或带噪声的探索 rollout，而非目标任务演示。
- 世界模型使用 Wan 2.1-T2V-1.3B Diffusion Transformer 骨干，并通过 AdaLN 和因果时间掩码加入动作条件。
- VLA 策略是 OpenVLA-OFT。它先通过 1-shot SFT 获得最少量的任务锚定，然后在想象 rollout 中用 GRPO 训练。
- 奖励来自冻结的 Qwen3-VL，它根据想象视频和文本指令给出二元成功判断。
- Dual-Noise Verification 用新的扩散噪声重新运行动作序列，并丢弃那些 Qwen3-VL 将成功判断改为失败的轨迹，从而减少世界模型幻觉导致的奖励黑客行为。

## 结果
- 在 LIBERO 上，1-shot SFT 基线在 Spatial、Object、Goal 和 Long 上的平均成功率为 43.4%。使用零样世界模型的 RAW-Dream 达到 52.3%，在使用 10 条目标演示且用于世界模型训练的目标 rollout 为 0 的条件下提升 +8.9 个百分点。
- 使用 Co-Train WM 的 RAW-Dream 在 10 条目标演示下达到 57.1% 平均成功率；相比之下，Online RL Short 使用 522 个带真实模拟器奖励的目标 episode，成功率为 47.9%。
- 使用 ID-FT WM 的 RAW-Dream 在使用 510 条目标数据时达到 66.0% 平均成功率，高于使用 2,510 条目标数据的 WoVR WM 的 60.9%。
- ID-FT WM 在各套件上的成功率分别为 Spatial 82.0%、Object 79.8%、Goal 63.4% 和 Long 38.6%；1-shot SFT 对应为 54.6%、46.4%、52.2% 和 20.2%。
- 在世界模型预测上，ID-FT WM 使用 500 条目标 rollout，并在所有套件的 FVD 上击败从零开始用 2,500 条目标 rollout 训练的 WoVR：Spatial 23.52 vs 45.39、Object 26.82 vs 92.11、Goal 21.65 vs 41.78、Long 38.84 vs 80.52。
- 在真实机器人实验中，论文报告相较每个任务 3-shot SFT 基线取得 +21.7 的绝对成功率提升。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12334v1](https://arxiv.org/abs/2605.12334v1)
