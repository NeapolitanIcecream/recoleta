---
source: arxiv
url: https://arxiv.org/abs/2604.28192v3
published_at: '2026-04-30T17:59:52'
authors:
- Hao Chen
- Jiaming Liu
- Zhonghao Yan
- Nuowei Han
- Renrui Zhang
- Chenyang Gu
- Jialin Gao
- Ziyu Guo
- Siyuan Qian
- Yinxi Wang
- Peng Jia
- Shanghang Zhang
- Pheng-Ann Heng
topics:
- vision-language-action
- robot-rl
- latent-reasoning
- generalist-robot-policy
- robot-data-scaling
- manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# LaST-R1: Reinforcing Robotic Manipulation via Adaptive Physical Latent Reasoning

## Summary
## 摘要
LaST-R1 是一种用于 VLA 机器人策略的 RL 后训练方法，会同时训练潜在推理嵌入和动作 token。论文报告称，在每个任务使用一个演示后，LaST-R1 在 LIBERO 上达到 99.9% 的平均成功率；在真实机器人任务中，相比有监督基线最高提升 22.5%。

## 问题
- 带潜在推理的 VLA 策略可以在行动前建模物理状态变化，但此前版本依赖静态模仿学习和成本高的专家演示。
- 只针对动作的 RL 后训练可以改善闭环行为，但不会训练影响动作的内部潜在推理路径。
- 这个问题很重要，因为操作策略会遇到误差累积、场景变化和长程任务，固定演示覆盖的状态不够多。

## 方法
- LaST-R1 从 Qwen3-VL-4B 出发，使用 SigLIP2-Large 进行视觉编码，然后先生成潜在推理嵌入，再解码机器人动作 token。
- 潜在目标来自 DINOv3 CLS 特征，并被选择为匹配 VLA 隐藏层大小，因此策略拥有紧凑的视觉状态目标，推理时不需要运行 DINOv3。
- Latent-to-Action Policy Optimization，即 LAPO，对潜在序列和动作序列都应用 RL，使用步级似然比和 PPO 风格的裁剪。
- 模型将潜在嵌入视为决策变量，因此任务成功带来的奖励会更新推理路径，也会更新输出的动作块。
- 自适应潜在 CoT 机制会学习何时输出 latent_end token，并在 rollout 期间从候选位置中选择较短或较长的推理范围。

## 结果
- 在 LIBERO 上，LaST-R1 报告称使用每个任务一个演示进行热身后，在四个套件上的平均成功率为 99.9%；列出的最强既有 RL 基线 pi_RL 平均成功率为 98.3%，并使用两个相机视角。
- LIBERO 各套件得分为：Spatial 99.8%、Object 100.0%、Goal 100.0%、Long 99.8%。
- 在 LIBERO-Long 上，LaST-R1 报告的成功率为 99.8%，OpenVLA-OFT 为 94.5%，pi_RL 为 94.0%，比列出的最佳既有得分高 5.3 个百分点。
- 与每个任务使用 50 条轨迹训练的 SFT-only 基线相比，LaST-R1 的平均 LIBERO 成功率高于 OpenVLA 的 76.5%、GR00T-N1 的 93.9%、pi_0 的 94.2%、pi_0.5 的 96.9% 和 OpenVLA-OFT 的 97.1%。
- 在真实世界部署中，论文称相比一种有监督微调方法，LaST-R1 在四个复杂任务上的平均表现最高提升 22.5%，在单臂和双臂设置中的平均成功率为 90%。
- 论文还称，LAPO 后训练后可对未见过的物体、背景和光照条件进行零样本泛化，但摘录未包含这些测试的完整数值表。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.28192v3](https://arxiv.org/abs/2604.28192v3)
