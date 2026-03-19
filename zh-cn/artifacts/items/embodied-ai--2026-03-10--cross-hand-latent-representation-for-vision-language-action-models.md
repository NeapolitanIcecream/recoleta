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
- robot-data-scaling
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# Cross-Hand Latent Representation for Vision-Language-Action Models

## Summary
本文提出 XL-VLA，通过一个跨不同灵巧手共享的潜在动作空间，把视觉-语言-动作模型从“按各手原始关节空间分别学”改为“先映射到统一动作语义再解码到具体手”。这解决了多手型数据难以复用的问题，并在真实世界多手、多任务灵巧操作中显著优于标准 VLA 基线。

## Problem
- 现有 VLA 在灵巧手场景里受限于**动作空间强依赖具体硬件形态**：不同手的关节数、驱动方式、运动学都不同，导致一个统一策略很难直接跨手训练。
- 新灵巧手不断出现，但为**每种新手单独采集大量演示数据**成本很高，不利于机器人基础模型的数据扩展与长期复用。
- 这很重要，因为如果不能跨 embodiment 共享动作表示，灵巧操作就难以像视觉/语言那样受益于大规模、多来源数据。

## Approach
- 提出 **XL-VLA**：在标准 VLA 架构中插入一个**共享潜在动作空间**，让不同灵巧手都把动作先编码成同一种 latent，再由各自解码器还原为对应关节命令。
- 潜在空间由一个**多头 VAE 式自编码器**学习：每种手有自己的 encoder/decoder，但它们共享同一个 latent 分布，因此策略网络只需预测手无关的 latent 动作。
- 该 latent 训练使用三类约束：**重建损失**保证单手可还原原关节姿态，**retargeting 损失**通过可微前向运动学对齐不同手的指尖几何/捏合关系，**KL 正则**让 latent 平滑可插值。
- 训练 latent 时**不需要跨手配对轨迹或示教数据**，而是从各手关节范围随机采样姿态，再利用跨手解码和 FK 几何一致性做自监督对齐。
- 在 VLA 训练阶段，冻结这些预训练好的 encoder/decoder，只微调主干去根据视觉、语言和历史 latent 动作预测下一个 latent chunk。

## Results
- 数据规模：作者采集了**4 种灵巧手、10 个任务、2000 条示教、约 2M state-action pairs** 的真实世界遥操作数据集；每个任务每种手 **50** 条示教。
- 与标准 **pi0** 基线相比，表 2 中 XL-VLA 在四种手上的平均成功率均明显提升：**Ability 0.37→0.73**，**Inspire 0.27→0.68**，**Paxini 0.35→0.78**，**XHand 0.29→0.70**。
- 表 2 的总体均值显示，XL-VLA 的跨手多任务成功率约为 **0.72**，而基线约为 **0.32**，即**绝对提升 0.40**；作者还按任务均值行报告基线约 **0.55**、XL-VLA 约 **0.90**，对应 **+0.35**，文中称为显著一致提升。
- 若看任务维度，多个高难灵巧任务提升很大，例如 **PF 0.20→0.70**、**HB 0.40→0.95**、**RB 0.45→0.90**、**PoS 0.23→0.88**、**PC 0.55→0.90**。
- 论文还声称 XL-VLA 具备**零样本泛化到未见 hand-task 组合**的能力，并在不同机器人系统（桌面 xArm 与 humanoid G1）联合训练时也有收益，但摘录中未给出对应完整数值表。

## Link
- [http://arxiv.org/abs/2603.10158v1](http://arxiv.org/abs/2603.10158v1)
