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
RAW-Dream 在冻结或轻度适配的任务无关视频世界模型中，用 RL 训练 VLA 策略，并用 Qwen3-VL 作为零样本奖励判定器。核心主张是，广泛的 play 式机器人数据可以替代面向新操作任务的特定任务世界模型和奖励模型训练。

## 问题
- 目前面向 VLA 的世界模型 RL 方法通常会在目标任务回放上训练世界模型和奖励模型，往往需要数千条轨迹。
- 这种数据需求削弱了想象式 RL 的主要优势，因为每个新任务在训练开始前仍然需要新的机器人数据。
- 这个问题对机器人基础模型很关键，因为部署时常会遇到世界模型训练阶段没有见过的新物体、布局和指令。

## 方法
- RAW-Dream 在广泛的、任务无关的机器人行为上预训练动作条件视频世界模型，例如 play 数据或带噪声的探索性回放，而不是目标任务示范。
- 世界模型以 Wan 2.1-T2V-1.3B 扩散 Transformer 为骨干，并通过 AdaLN 和因果时间掩码加入动作条件。
- VLA 策略是 OpenVLA-OFT。它先用 1-shot SFT 获得最少的任务锚定，然后在想象回放中用 GRPO 训练。
- 奖励来自冻结的 Qwen3-VL，它根据想象视频和文本指令给出二元成功判断。
- 双噪声验证会用新的扩散噪声重新运行动作序列，并丢弃那些在 Qwen3-VL 中成功判断变为失败的轨迹，从而减少世界模型幻觉带来的奖励作弊。

## 结果
- 在 LIBERO 上，1-shot SFT 基线在 Spatial、Object、Goal 和 Long 四个任务组上的平均成功率为 43.4%。RAW-Dream 使用零样本世界模型时达到 52.3%，在用于世界模型训练的目标演示为 10 条、目标回放为 0 条的条件下提升了 8.9 个百分点。
- RAW-Dream 搭配 Co-Train WM 时，在 10 条目标演示下平均成功率达到 57.1%，而使用 522 个带真实模拟器奖励的目标 episode 的 Online RL Short 只有 47.9%。
- RAW-Dream 搭配 ID-FT WM 时，使用 510 条目标数据达到 66.0% 的平均成功率，高于使用 2,510 条目标数据的 WoVR WM 的 60.9%。
- 分任务组看，ID-FT WM 的成功率分别为 Spatial 82.0%、Object 79.8%、Goal 63.4%、Long 38.6%；1-shot SFT 分别为 54.6%、46.4%、52.2%、20.2%。
- 在世界模型预测上，ID-FT WM 使用 500 条目标回放，在所有任务组的 FVD 上都优于用 2,500 条目标回放从头训练的 WoVR：Spatial 23.52 对 45.39，Object 26.82 对 92.11，Goal 21.65 对 41.78，Long 38.84 对 80.52。
- 在真实机器人实验中，论文报告相对 3-shot SFT 基线，每个任务的绝对成功率提升了 21.7 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12334v1](https://arxiv.org/abs/2605.12334v1)
