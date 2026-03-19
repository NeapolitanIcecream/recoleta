---
source: arxiv
url: http://arxiv.org/abs/2603.10158v1
published_at: '2026-03-10T18:50:57'
authors:
- Guangqi Jiang
- Yutong Liang
- Jianglong Ye
- Jia-Yang Huang
- Changwei Jing
- Rocky Duan
- Pieter Abbeel
- Xiaolong Wang
- Xueyan Zou
topics:
- vision-language-action
- dexterous-manipulation
- cross-embodiment
- latent-action-space
- robot-learning
relevance_score: 0.32
run_id: materialize-outputs
language_code: zh-CN
---

# Cross-Hand Latent Representation for Vision-Language-Action Models

## Summary
本文提出 XL-VLA：一种把多种灵巧手动作统一到共享潜变量空间中的视觉-语言-动作模型，用于跨手型训练与迁移。核心价值是减少每种新手型都要单独采集大量示教数据的成本，并提升真实机器人灵巧操作的泛化能力。

## Problem
- 灵巧手的动作空间由具体硬件关节定义，不同手型的关节数、结构和驱动方式差异很大，导致标准 VLA 很难直接共享数据和策略。
- 随着新型灵巧手不断出现，为每个 embodiment 单独采集大规模演示数据既昂贵又不可扩展。
- 如果不能学习跨 embodiment 的统一动作表示，机器人很难实现跨手型复用、零样本迁移和更稳健的真实世界操作。

## Approach
- 提出一个**共享潜在动作空间**：每种手都有各自编码器/解码器，但都映射到同一个 latent space，让不同手型的动作先变成“通用动作代码”，再解码回各自关节命令。
- 潜空间通过多头 VAE 风格自编码器预训练，使用三类约束：关节重建损失、基于可微前向运动学的跨手指尖几何对齐损失、以及 KL 潜变量正则。
- 该潜空间训练是**无配对、无示教**的：只需在各手型关节范围内随机采样姿态，再通过跨手解码和指尖几何一致性来对齐表示。
- 在 VLA 阶段，模型不直接预测原始关节序列，而是预测下一个 latent action chunk；冻结手型专属编码器/解码器，仅微调 VLA action expert，从而把标准 VLA 架构变成 hand-agnostic policy。
- 作者还构建了真实世界数据集：4 种灵巧手、10 个任务、共 2000 条 demonstrations、约 2M state-action pairs。

## Results
- 在 4 种手 × 10 个任务的跨 embodiment 训练中，XL-VLA 相比基线 **\(\pi_0\)** 的总体平均成功率从 **0.32 提升到 0.72**，表中标注为 **+40%**（Table 2，跨手平均）。
- 分手型看：Ability **0.37 → 0.73**，Inspire **0.27 → 0.68**，Paxini **0.35 → 0.78**，XHand **0.29 → 0.70**；说明无论结构相近还是差异较大的手型都受益。
- 分任务平均看，PF **0.20 → 0.70**，SC **0.28 → 0.63**，SoC **0.08 → 0.55**，HB **0.40 → 0.95**，RL **0.10 → 0.43**，PS **0.68 → 0.95**，RB **0.45 → 0.90**，PuS **0.25 → 0.35**，PoS **0.23 → 0.88**，PC **0.55 → 0.90**。
- 论文文字还声称“跨任务与跨手平均成功率”可从 **0.55 提升到 0.90（+0.35）**，但这与表 2 数字口径不完全一致；可确定的最强结论是 XL-VLA 在所有手型和任务上都稳定优于 raw joint space 的标准 VLA。
- 作者进一步声称该方法支持**零样本的未见 hand-task 组合泛化**，并在不同机器人系统（xArm 与 G1 humanoid）联合训练时也能带来收益，但给定摘录中未提供完整的对应数值表。

## Link
- [http://arxiv.org/abs/2603.10158v1](http://arxiv.org/abs/2603.10158v1)
