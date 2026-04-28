---
source: arxiv
url: http://arxiv.org/abs/2604.16585v1
published_at: '2026-04-17T15:12:15'
authors:
- Noureddine Kermiche
topics:
- world-model
- discrete-latents
- action-conditioned-planning
- self-supervised-learning
- topological-representation
relevance_score: 0.8
run_id: materialize-outputs
language_code: zh-CN
---

# The Global Neural World Model: Spatially Grounded Discrete Topologies for Action-Conditioned Planning

## Summary
## 摘要
GNWM 是一种世界模型，它将观测映射到离散的二维网格中，并根据动作预测未来的网格状态。论文称，这种离散拓扑可以减少 rollout 漂移，并在不做像素重建、也不使用 BYOL 风格目标网络的情况下生成可解释的状态图。

## 问题
- 连续潜变量世界模型在自回归 rollout 中会发生漂移：微小的预测误差会累积，潜变量变得模糊，长时域规划会失去物理结构。
- 现有用于预测式自监督学习的抗坍塌方法，往往依赖额外的训练机制，例如目标网络、stop-gradient 路径、对比负样本或协方差惩罚。
- 对于规划任务，作者希望状态空间既足够离散，能随时间保持稳定，又仍然可以用梯度下降进行端到端训练。

## 方法
- GNWM 将每个输入编码到一个二维潜在网格中，然后施加固定的高斯空间卷积。这样会把激活扩散到邻近单元，使相邻状态在网格上保持接近。
- 平滑后的网格会被转换为一个概率分布。预测器接收当前潜在状态和动作，预测下一个潜在状态；目标分支则编码真实的下一帧观测。
- 训练使用三个损失：用于匹配预测下一状态和目标下一状态的相似性损失、用于避免坍塌的批级均匀使用损失，以及推动每个状态朝稀疏、接近 one-hot 激活发展的尖峰损失。
- 在推理时，模型可以在下一个循环步之前，把预测分布“吸附”到其 argmax 网格单元。论文将此描述为一种纠错步骤，用来防止长 rollout 中的漂移。
- 作者在四个玩具场景上测试了该方法：被动单球视频、动作条件随机游走控制、双球因子分解，以及一个合成语法序列任务。

## 结果
- 在 **15x15 grid** 的被动观测任务中，模型使用了 **225 个神经元中的 173 个**，并形成一个连续、有组织的区块。论文将此作为未发生 codebook collapse 的证据。
- 在 **100-step autoregressive rollouts** 中，一个连续基线的标准差衰减到 **0.066**，而带有 grid snapping 的 GNWM 保持在 **0.016**。摘录中没有说明该基线架构的具体名称，只称其为连续基线。
- 在具有 **4 个动作**（上、下、左、右）的主动控制随机游走场景中，模型分配了 **41 个活跃神经元**。按作者说法，这与经验访问分布一致。
- 在抽象序列任务中，面对 **40 个唯一的 32D 词嵌入**，模型使用了 **恰好 40 个活跃神经元**，并按语法角色对它们聚类：名词、动词、形容词、宾语。
- 论文还声称成功将两个独立运动的小球分离到两个潜在通道中，但摘录没有给出这个实验的数值指标。
- 证据目前只来自小型合成环境和描述性指标。摘录没有报告标准规划基准、机器人任务、真实世界数据，也没有在常见数据集上与已有世界模型基线做比较。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16585v1](http://arxiv.org/abs/2604.16585v1)
