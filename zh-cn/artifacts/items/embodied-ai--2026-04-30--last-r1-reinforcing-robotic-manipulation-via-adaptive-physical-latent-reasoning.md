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
LaST-R1 是一种用于 VLA 机器人策略的 RL 后训练方法，它同时训练潜在推理嵌入和动作 token。文中报告，在每个任务只用一个示范进行预热后，LIBERO 上的平均成功率达到 99.9%，在真实机器人任务中相对监督式基线最高提升 22.5%。

## 问题
- 具有潜在推理能力的 VLA 策略可以在行动前建模物理状态变化，但早期版本依赖静态模仿学习和成本高昂的专家示范。
- 只针对动作的 RL 后训练能改善闭环行为，但不会训练为动作提供条件的内部潜在推理路径。
- 这个问题很重要，因为操作策略会遇到误差累积、场景变化和长时序任务，而固定示范覆盖不了足够多的状态。

## 方法
- LaST-R1 以带有 SigLIP2-Large 视觉编码的 Qwen3-VL-4B 为起点，然后在解码机器人动作 token 之前生成潜在推理嵌入。
- 潜在目标来自 DINOv3 的 CLS 特征，选择这些特征是为了匹配 VLA 的隐藏层尺寸，这样策略就有了紧凑的视觉状态目标，而且推理时不需要运行 DINOv3。
- Latent-to-Action Policy Optimization，简称 LAPO，把 RL 同时应用到潜在序列和动作序列，使用逐步似然比和类似 PPO 的裁剪。
- 模型把潜在嵌入当作决策变量，因此任务成功带来的奖励会同时更新推理路径和输出的动作片段。
- 自适应潜在 CoT 机制学习何时发出 latent_end token，在 rollout 过程中从候选位置里选择更短或更长的推理时长。

## 结果
- 在 LIBERO 上，LaST-R1 在四个套件上的平均成功率为 99.9%，每个任务只用一个示范进行预热；已列出的最强先前 RL 基线 pi_RL 报告为 98.3% 的平均成功率，并且使用两个摄像头视角。
- LIBERO 各套件得分分别为 99.8% Spatial、100.0% Object、100.0% Goal 和 99.8% Long。
- 在 LIBERO-Long 上，LaST-R1 报告 99.8% 的成功率，OpenVLA-OFT 为 94.5%，pi_RL 为 94.0%，比最好的已列先前分数高 5.3 个百分点。
- 与每个任务用 50 条轨迹训练的仅 SFT 基线相比，LaST-R1 的平均 LIBERO 成功率高于 OpenVLA 的 76.5%、GR00T-N1 的 93.9%、pi_0 的 94.2%、pi_0.5 的 96.9% 和 OpenVLA-OFT 的 97.1%。
- 在真实部署中，论文声称相对一种监督式微调方法，在四个复杂任务上平均最高提升 22.5%，在单臂和双臂设置中的平均成功率达到 90%。
- 论文还声称，经过 LAPO 后训练后，模型可以对未见过的物体、背景和光照条件实现 zero-shot 泛化，但摘要里没有给出这些测试的完整数值表。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.28192v3](https://arxiv.org/abs/2604.28192v3)
