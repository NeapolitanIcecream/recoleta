---
source: arxiv
url: https://arxiv.org/abs/2605.18722v1
published_at: '2026-05-18T17:50:32'
authors:
- Zongzheng Zhang
- Jingrui Pang
- Zhuo Yang
- Kun Li
- Minwen Liao
- Saining Zhang
- Guoxuan Chi
- Jinbang Guo
- Huan-ang Gao
- Modi Shi
- Dongyun Ge
- Yao Mu
- Jiayuan Gu
- Rui Chen
- Hao Dong
- Huazhe Xu
- Li Yi
- Yixin Zhu
- Hang Zhao
- Pengwei Wang
- Shanghang Zhang
- Guocai Yao
- Jianyu Chen
- Hongyang Li
- Hao Zhao
topics:
- vision-language-action
- dexterous-manipulation
- bimanual-robotics
- robot-data-scaling
- diffusion-policy
- sim2real
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Dexora: Open-source VLA for High-DoF Bimanual Dexterity

## Summary
## 摘要
Dexora 是一个开源的视觉-语言-动作系统，用于双臂、双手的高自由度机器人操作。它结合了一个 36 自由度机器人、匹配的仿真、大规模真实与合成数据集，以及按质量加权的扩散策略训练。

## 问题
- 现有 VLA 系统主要面向双臂夹爪或单臂灵巧手，因此无法覆盖需要双臂和可动手指的任务。
- 这一缺口会影响拧瓶盖、使用笔、切食物、从狭窄书架取书、以及双手分离物体等任务。
- 高自由度手的真实遥操作数据噪声很大，原因包括操作者差异、跟踪误差、遮挡和延迟。

## 方法
- 硬件使用两只 6 自由度 AIRBOT 机械臂和两只 12 自由度 XHAND 灵巧手，总计 36 自由度。
- 遥操作把控制问题拆开：自定义外骨骼背包记录手臂运动，Apple Vision Pro 手部跟踪记录手指运动。
- 同一套遥操作接口同时驱动真实机器人和 MuJoCo 数字孪生，并以 20 Hz 记录四个 RGB 视角和完整关节状态。
- 训练语料包括 100K 条仿真轨迹和 650 万帧，以及 1 万段真实遥操作回合和 292 万帧。
- 策略是一个以语言、多视角图像和关节状态为条件的扩散 Transformer；离线判别器给每个片段打质量分，并对扩散损失加权，让低质量示范在训练中的权重更低。

## 结果
- 在 12 个基础真实任务上，Dexora 的平均成功率为 89.6%，高于 GR00T N1 的 82.1%、π0 的 50.4% 和 Diffusion Policy 的 34.2%。
- Dexora 在 12 个基础任务中的 7 个任务上达到至少 90% 的成功率，并在 apple-to-plate、bowl-to-bowl 和 cabinet-door opening 上达到 100%。
- 在 6 个灵巧任务上，Dexora 的平均成功率为 66.7%，高于 GR00T N1 的 51.7%、π0 的 26.7% 和 Diffusion Policy 的 6.7%。
- 灵巧任务的提升包括 Use pen 的 65%、Fetch book 的 80%、Rough dough 的 80% 和 Twist cap 的 25%；所有基线在 Twist cap 上都是 0%。
- 论文声称，在不改变模型架构的情况下，可以迁移到单臂夹爪、双臂夹爪和单臂低自由度手，但摘要片段没有给出这些迁移测试的详细成功率表。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.18722v1](https://arxiv.org/abs/2605.18722v1)
