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
- 3d-point-clouds
- imitation-learning
- cross-embodiment-transfer
- transformer-policy
relevance_score: 0.18
run_id: materialize-outputs
---

# Structural Action Transformer for 3D Dexterous Manipulation

## Summary
本文提出 Structural Action Transformer（SAT），把高自由度灵巧手的动作从“按时间排列的动作向量”改写为“按关节排列的轨迹序列”，以更自然地支持不同机器人形态之间的技能迁移。它结合3D点云、语言条件和关节结构编码，在异构模仿学习与灵巧操作上取得了更强表现与更高样本效率。

## Problem
- 现有灵巧操作模仿学习方法大多采用时间中心的动作表示 $(T,D_a)$，当自由度很高时，单个动作向量内部的复杂关节相关性难以学习。
- 不同机器人手在关节数、运动学结构和功能上存在差异，固定维度动作表示不适合跨 embodiment（跨形态）迁移，这限制了从异构人类/机器人数据中学习。
- 许多通用机器人策略依赖2D观测，难以捕捉精细灵巧操作所需的3D空间关系，因此会影响高精度操作能力。

## Approach
- 提出结构中心的动作表示：将一个动作块表示为 $D_a \times T$，把每个关节视为一个 token，其特征是该关节未来一段时间的整条轨迹；这样不同机器人只是在 token 数量上不同，Transformer 可原生处理变长序列。
- 使用 Embodied Joint Codebook 为每个关节加入结构先验，编码其 **embodiment ID、功能类别、旋转轴**，帮助模型在不同机械手之间找到功能相似的关节对应关系。
- 观测端直接使用 **3D点云历史 + 语言指令**：通过 FPS + PointNet 提取局部/全局点云 token，再与 T5 语言 token 拼接形成条件输入。
- 生成端使用基于 DiT 的 Structural Action Transformer，在条件 flow matching 框架下学习动作速度场，并通过 ODE 求解生成完整动作块；文中强调可用 **1-NFE** 推理。
- 作者声称这是**首个**沿“结构维度”而非“时间维度”对动作进行 tokenization 的策略框架，用于高DoF异构操纵器策略学习。

## Results
- 在 **11个仿真任务**（Adroit 3个、DexArt 4个、Bi-DexHands 4个）上，SAT 的平均成功率为 **0.71±0.04**，优于：3D ManiFlow Policy **0.66±0.04**、3D Diffusion Policy **0.63±0.06**、UniAct **0.50±0.05**、HPT **0.47±0.04**、Diffusion Policy **0.42±0.04**。
- 分基准看，SAT 在 **Adroit** 上达到 **0.75±0.02**，高于 3D ManiFlow 的 **0.70±0.02** 和 3D Diffusion Policy 的 **0.68±0.03**。
- 在 **DexArt** 上，SAT 为 **0.73±0.03**，高于 3D ManiFlow 的 **0.70±0.03**、3D Diffusion Policy 的 **0.69±0.02**。
- 在 **Bi-DexHands** 上，SAT 为 **0.67±0.05**，高于 3D ManiFlow 的 **0.59±0.07**、3D Diffusion Policy 的 **0.55±0.14**。
- 参数效率突出：SAT 仅 **19.36M** 参数，却优于 **218.9M** 的 3D ManiFlow、**255.2M** 的 3D Diffusion Policy，以及 **1053M** 的 UniAct。
- 时序压缩消融显示，token dim 从 **16/32/64/128/256** 变化时，成功率分别为 **0.66/0.71/0.71/0.71/0.70**；**32维**已达到最优水平之一，且对应 **8.65M** 参数、**0.77G** 1-NFE FLOPs，说明该结构表示在较小模型下也有效。

## Link
- [http://arxiv.org/abs/2603.03960v1](http://arxiv.org/abs/2603.03960v1)
