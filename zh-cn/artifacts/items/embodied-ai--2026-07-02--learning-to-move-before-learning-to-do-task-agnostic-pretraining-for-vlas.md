---
source: arxiv
url: https://arxiv.org/abs/2607.02466v1
published_at: '2026-07-02T17:33:37'
authors:
- Junhao Shi
- Siyin Wang
- Xiaopeng Yu
- Li Ji
- Jingjing Gong
- Xipeng Qiu
topics:
- vision-language-action
- robot-data-scaling
- generalist-robot-policy
- inverse-dynamics
- task-agnostic-pretraining
- robot-random-play
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Learning to Move Before Learning to Do: Task-Agnostic pretraining for VLAs

## Summary
## 摘要
TAP 先用任务无关的机器人运动对 VLA 进行预训练，再进行语言条件的行为克隆。主要主张是，低成本、无标签的交互数据可以教授低层物理控制，并减少对专家遥操作的依赖。

## 问题
- VLA 训练通常需要由人工遥操作收集的观察-语言-动作三元组，这种数据成本高，扩展慢。
- 许多没有有用任务标签的机器人轨迹被丢弃，尽管它们包含接触、抓取、推动和物体运动信息。
- 这一点很重要，因为通用机器人策略需要的物理交互数据，超过团队仅靠带标注专家示范所能收集的规模。

## 方法
- TAP 使用来自两个来源的任务无关轨迹：仿真中不相关的 Bridge 轨迹，以及 WidowX 250s 机器人上的自主随机玩耍。
- 第 1 阶段使用逆动力学训练：给定观察 `o_t` 和下一观察 `o_{t+1}`，模型预测导致该变化的 7D 增量位姿动作 `a_t`。
- 逆动力学目标让模型关注移动的手和物体，而不是静态背景像素。
- 第 2 阶段使用一小组带语言标签的专家示范，通过标准行为克隆对同一骨干网络和动作头进行微调。
- 真实世界随机玩耍流水线构建安全位姿库，采样可达航点，加入接触启发式方法，注入有界高斯噪声，并记录生成的轨迹。

## 结果
- 在 SIMPLER 中，TAP-20k 达到 33.32% Avg-All 成功率；相同架构使用标准行为克隆训练为 23.15%，OpenVLA 为 7.75%，RT-1-X 为 3.03%。
- SIMPLER Avg-Partial 成功率中，TAP-20k 为 45.82%；标准行为克隆为 31.79%，Octo 为 42.30%，π0 为 53.10%。
- SIMPLER Avg-Entire 成功率中，TAP-20k 为 20.82%；标准行为克隆为 14.50%，Octo 为 20.33%，π0 为 27.05%。
- 更多任务无关预训练提升了 8k、14k 和 20k 回合下的 SIMPLER Avg-All 成功率：24.47%、30.21% 和 33.32%。
- 在真实世界 WidowX 测试中，使用 30 小时随机玩耍和每个任务 200 条专家示范，TAP 在 carrot-on-plate 上平均达到 28%，从零训练为 9%，NORA 为 36%。
- 在真实世界 push-pumpkin 任务上，TAP 平均达到 61%，从零训练为 21%，NORA 为 56%；在背景纹理变化下得分为 65%，对比 0% 和 55%；在视角变化下得分为 25%，对比 0% 和 0%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.02466v1](https://arxiv.org/abs/2607.02466v1)
