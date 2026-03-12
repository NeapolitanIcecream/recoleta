---
source: arxiv
url: http://arxiv.org/abs/2603.03960v1
published_at: '2026-03-04T11:38:12'
authors:
- Xiaohan Lei
- Min Wang
- Bohong Weng
- Wengang Zhou
- Houqiang Li
topics:
- dexterous-manipulation
- cross-embodiment-transfer
- 3d-point-clouds
- transformer-policy
- flow-matching
- robot-imitation-learning
relevance_score: 0.95
run_id: materialize-outputs
---

# Structural Action Transformer for 3D Dexterous Manipulation

## Summary
本文提出 Structural Action Transformer (SAT)，面向高自由度灵巧手的跨构型模仿学习，把动作从“按时间排”的序列改写为“按关节排”的3D结构序列。该表示让同一个 Transformer 能自然处理不同关节数的手，并在大规模异构人类/机器人数据上实现更好的迁移与样本效率。

## Problem
- 要解决的是**高自由度灵巧手在异构数据上的跨构型技能迁移**：不同手型/关节数/运动学结构差异很大，传统模仿学习很难共享技能。
- 现有方法多用**2D观测**和**时间中心的动作表示 $(T, D_a)$**，难以表达精细操作所需的3D空间关系，也无法自然对齐不同构型的动作维度。
- 这很重要，因为如果不能跨人手、机器人手和仿真平台复用数据，灵巧操作策略就很难扩展到“通用型”高DoF机器人基础模型。

## Approach
- 核心思想是把一个动作块从传统的 **$(T, D_a)$ 时间序列**，重构为 **$(D_a, T)$ 关节序列**：每个 token 不再代表某个时刻的整只手动作，而是代表**一个关节在未来一段时间内的轨迹**。
- 这样做后，不同机器人只是在**序列长度 $D_a$** 上不同；Transformer 天然支持变长序列，因此能更自然地处理异构构型并学习关节功能对应关系。
- 为了告诉模型“这个关节是谁、做什么、怎么转”，作者设计了 **Embodied Joint Codebook**，用三元组 *(embodiment id, functional category, rotation axis)* 给每个关节加上结构先验嵌入。
- 输入端使用**3D点云历史 + 语言指令**：点云通过 FPS + PointNet 提取局部/全局 token，语言通过 T5 编码；这些观察 token 与结构化动作 token 一起送入 DiT。
- 训练时不直接回归动作，而是用**continuous-time flow matching** 学习从高斯噪声到动作块的速度场；推理时用 ODE 求解生成整段动作，文中称可用 **1-NFE** 生成。

## Results
- 在 **11 个仿真灵巧操作任务**（Adroit 3个、DexArt 4个、Bi-DexHands 4个）上，SAT 的**平均成功率为 0.71±0.04**，优于所有对比方法。
- 相比 3D 基线：SAT **0.71±0.04** vs **3D ManiFlow Policy 0.66±0.04** vs **3D Diffusion Policy 0.63±0.06**；分别高出 **0.05** 和 **0.08** 平均成功率。
- 分数据集看，SAT 在 **Adroit/DexArt/Bi-DexHands** 上分别达到 **0.75±0.02 / 0.73±0.03 / 0.67±0.05**；对应最强基线 3D ManiFlow 为 **0.70±0.02 / 0.70±0.03 / 0.59±0.07**。
- 相比 2D 方法，SAT 优势更明显：平均成功率 **0.71** 对比 **UniAct 0.50**、**HPT 0.47**、**Diffusion Policy 0.42**。
- 参数效率也很强：SAT 仅 **19.36M** 参数，却超过 **218.9M** 的 3D ManiFlow、**255.2M** 的 3D Diffusion Policy 和 **1053M** 的 UniAct。
- 消融显示时间压缩维度在 **32/64/128** 时都能达到 **0.71** 成功率，其中 **64维** 配置对应 **19.36M 参数、0.99G FLOPs (1-NFE)**；论文还声称具备更好的样本效率和有效跨构型迁移，但摘录中未给出更细的样本效率曲线数值。

## Link
- [http://arxiv.org/abs/2603.03960v1](http://arxiv.org/abs/2603.03960v1)
