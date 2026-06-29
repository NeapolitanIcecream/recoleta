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
## 总结
PAIR-VLA 在 PPO 微调中加入动作分布引导，让 VLA 机器人策略忽略与任务无关的视觉变化，并对与任务相关的变化作出反应。它在 ManiSkill3 抓取放置任务上提升了 OpenVLA 和 π₀.₅ 在分布外视觉变化下的成功率，而且不改动推理时的架构。

## 问题
- 标准 PPO 奖励只能告诉机器人任务是否成功，不能告诉它某个视觉变化该不该让动作保持不变，还是需要换成另一种动作。
- VLA 策略在部署时遇到视觉变化时会失效，例如未见过的干扰物、桌面纹理、光照、相机视角和目标物体位姿变化。
- 这对机器人操作很关键，因为干扰物或纹理变化通常应该被忽略，而目标物体移动后往往需要新的抓取或轨迹。

## 方法
- PAIR-VLA 用 PPO 加两个辅助损失，对同一观察的成对视觉变体微调 OpenVLA 和 π₀.₅。
- 保持任务不变的变体会移除干扰物并替换背景外观，同时保持机器人、目标物体、容器和所需操作不变。
- 一致性损失最小化原始视图与保持任务不变视图之间动作分布的 KL 散度。
- 改变任务的变体会扰动目标物体位姿，这会改变所需动作。
- 敏感性损失最大化原始视图与改变任务视图之间经过裁剪的 KL 散度；这些损失只在训练时使用，因此部署时没有额外推理成本。

## 结果
- 在 ManiSkill3 抓取放置任务上，OpenVLA 的分布外平均成功率从 PPO 的 77.90% 提升到 PAIR-VLA 的 87.00%，在桌面纹理、光照、目标位姿和杂乱场景测试中提升了 9.10 个百分点。
- OpenVLA 在各项设置中的提升分别是：桌面纹理 86.98%→94.53%，光照 72.14%→80.47%，目标位姿 83.59%→90.63%，杂乱场景 68.88%→82.36%。
- 在 π₀.₅ 上，分布外平均成功率从 PPO 的 46.25% 提升到 62.87%，提升了 16.62 个百分点。
- π₀.₅ 在各项设置中的提升分别是：桌面纹理 63.54%→80.21%，光照 28.54%→51.67%，目标位姿 56.46%→69.38%，杂乱场景 36.46%→50.21%。
- 每个报告的成功率都基于 128 次评估回合，并且是 3 次独立运行的平均值。
- 在 OpenVLA 的分布内测试中，PAIR-VLA 在约 80 个训练步内达到 90% 成功率，而 PPO 约需要 240 个训练步，训练步数约减少 3 倍。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13105v1](https://arxiv.org/abs/2605.13105v1)
