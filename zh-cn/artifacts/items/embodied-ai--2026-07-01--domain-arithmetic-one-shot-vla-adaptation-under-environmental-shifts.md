---
source: arxiv
url: https://arxiv.org/abs/2607.00666v1
published_at: '2026-07-01T09:13:40'
authors:
- Taewook Kang
- Taeheon Kim
- Donghyun Shin
- Jonghyun Choi
topics:
- vision-language-action
- one-shot-adaptation
- robot-foundation-models
- weight-arithmetic
- domain-adaptation
- embodiment-transfer
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Domain Arithmetic: One-Shot VLA Adaptation under Environmental Shifts

## Summary
## 概要
DART 用一个目标域任务示范，把 Vision-Language-Action 策略适配到变化后的环境。它从微调后的权重中提取域偏移向量，并把该向量加到基础策略上，使其他已学习任务也能在目标域中运行。

## 问题
- 即使任务本身不变，摄像机位姿、光照、传感器校准或机器人本体发生变化时，VLA 策略也可能失败。
- 现有适配方法通常需要为目标域中的每个任务收集示范，这会增加真实机器人部署成本。
- 只在单个目标任务上做 one-shot 微调，往往只提升该任务表现，同时在留出任务上失败，因此不能保留基础策略的多任务行为。

## 方法
- 在同一任务的一个源域示范和一个目标域示范上分别微调基础 VLA 模型，得到两个权重更新向量。
- 用目标更新减去源更新，抵消共享的任务方向，并分离出环境偏移对应的域向量。
- 对各层更新运行 SVD，并在相减前只保留与目标更新子空间对齐的源奇异方向，以减少源域伪影。
- 按源-目标子空间对齐分数缩放每层的域向量，然后用系数 α 把缩放后的向量加到基础模型上。
- 该方法只改变权重，因此不需要新的策略架构。

## 结果
- 摘录没有给出任务成功率百分比、标准误或相对基线的差距，因此无法根据所给文本用数值核验主要性能主张。
- 论文声称用 1 个目标域任务的 1 个示范，再加上一个匹配的源域示范完成 one-shot 适配，然后在源任务集的所有任务上评估。
- 在 LIBERO 上使用 π0.5、处于 Medium 摄像机视角偏移时，one-shot 微调在适配任务上的表现高于留出任务；摘录未提供成功率。
- 权重分析使用来自 4 个任务 × 4 个域的 16 个更新向量；组合得到的任务加域估计与目标更新的子空间对齐最高，但摘录没有给出对齐数值。
- 论文报告了在仿真和真实机器人上使用 π0.5 与 π0-FAST、覆盖视觉和本体偏移的实验，并声称 DART 优于现有 one-shot VLA 适配基线；摘录未给出数值差距。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.00666v1](https://arxiv.org/abs/2607.00666v1)
