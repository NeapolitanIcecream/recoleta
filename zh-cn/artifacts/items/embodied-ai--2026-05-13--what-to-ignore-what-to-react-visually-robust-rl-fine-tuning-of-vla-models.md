---
source: arxiv
url: https://arxiv.org/abs/2605.13105v1
published_at: '2026-05-13T07:15:37'
authors:
- Yuanfang Peng
- Jingjing Fu
- Chuheng Zhang
- Li Zhao
- Jiang Bian
- Mingyu Liu
- Ling Zhang
- Jun Zhang
- Rui Wang
topics:
- vision-language-action
- rl-fine-tuning
- robot-manipulation
- visual-generalization
- sim2real
- policy-regularization
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# What to Ignore, What to React: Visually Robust RL Fine-Tuning of VLA Models

## Summary
## 摘要
PAIR-VLA 在 PPO 微调中加入动作分布指导，使 VLA 机器人策略忽略与任务无关的视觉变化，并对与任务相关的变化作出反应。它在 ManiSkill3 抓取放置任务中提高了 OpenVLA 和 π₀.₅ 在分布外视觉变化下的成功率，且不改变推理时架构。

## 问题
- 标准 PPO 奖励会告诉机器人任务是否成功，但不会告诉它某个视觉变化应让动作保持不变，还是需要采取不同动作。
- VLA 策略在部署时可能遇到未见过的干扰物、桌面纹理、光照、相机视角和目标物体姿态等视觉变化，并因此失败。
- 这对机器人操作很关键，因为干扰物或纹理变化通常应被忽略，而目标物体移动后可能需要新的抓取方式或运动轨迹。

## 方法
- PAIR-VLA 使用 PPO 加上两个辅助损失来微调 OpenVLA 和 π₀.₅，这些辅助损失在同一观测的成对视觉变体上计算。
- 保持任务不变的变体会移除干扰物并替换背景外观，同时保持机器人、目标物体、容器和所需操作不变。
- 不变性损失会最小化原始视图与保持任务不变视图之间动作分布的 KL 散度。
- 改变任务的变体会扰动目标物体姿态，这可能改变所需动作。
- 敏感性损失会最大化原始视图与改变任务视图之间经过裁剪的 KL 散度；这些损失只在训练期间使用，因此部署时没有额外推理成本。

## 结果
- 在 ManiSkill3 抓取放置任务中，OpenVLA 的平均分布外成功率从 PPO 的 77.90% 提高到 PAIR-VLA 的 87.00%，在桌面纹理、光照、目标姿态和杂乱场景测试上提升 +9.10 个百分点。
- OpenVLA 在各设置下的提升为：桌面纹理 86.98%→94.53%，光照 72.14%→80.47%，目标姿态 83.59%→90.63%，杂乱场景 68.88%→82.36%。
- 在 π₀.₅ 上，平均分布外成功率从 PPO 的 46.25% 提高到 62.87%，提升 +16.62 个百分点。
- π₀.₅ 在各设置下的提升为：桌面纹理 63.54%→80.21%，光照 28.54%→51.67%，目标姿态 56.46%→69.38%，杂乱场景 36.46%→50.21%。
- 每个报告的成功率都使用 128 个评估 episode，并在 3 次独立运行上取平均。
- 在含 1 个干扰物的 OpenVLA 同分布测试中，PAIR-VLA 约用 80 个训练步达到 90% 成功率，而 PPO 约需 240 个训练步，训练步数约减少到三分之一。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13105v1](https://arxiv.org/abs/2605.13105v1)
