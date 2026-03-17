---
source: arxiv
url: http://arxiv.org/abs/2603.12231v1
published_at: '2026-03-12T17:49:47'
authors:
- Ying Wang
- Oumayma Bounou
- Gaoyue Zhou
- Randall Balestriero
- Tim G. J. Rudner
- Yann LeCun
- Mengye Ren
topics:
- world-model
- latent-planning
- representation-learning
- gradient-based-planning
- self-supervised-learning
relevance_score: 0.72
run_id: materialize-outputs
---

# Temporal Straightening for Latent Planning

## Summary
本文提出**Temporal Straightening**，通过在世界模型训练中加入轨迹曲率正则，让潜在空间中的可行状态演化更“笔直”，从而更适合做梯度规划。核心贡献是把“好表征”与“好规划几何”直接联系起来，提升潜在目标距离的可用性和规划优化稳定性。

## Problem
- 现有潜在世界模型常依赖预训练视觉特征，但这些特征并非为规划设计，包含与控制无关甚至有害的信息。
- 当潜在轨迹在表征空间里高度弯曲时，欧氏距离不能真实反映沿可行动力学到达目标的“地质距离”，导致目标代价误导规划。
- 这会让梯度式动作优化目标高度非凸、条件数差、容易卡住，因此很多方法被迫使用计算更重的 CEM/MPPI 等搜索式规划器。

## Approach
- 联合训练一个世界模型：观测编码器、动作编码器和潜在动力学预测器，用预测下一步潜在状态作为主学习目标。
- 对连续三个潜在状态 $z_t,z_{t+1},z_{t+2}$，计算相邻“速度”向量 $v_t=z_{t+1}-z_t$ 与 $v_{t+1}=z_{t+2}-z_{t+1}$ 的余弦相似度，并最小化 $1-\cos(v_t,v_{t+1})$，从而惩罚局部曲率。
- 直观上，这会让潜在轨迹更接近直线，使潜在欧氏距离更接近真实可达路径距离，也让终点误差的优化景观更平滑。
- 训练总损失为预测 MSE 加上曲率正则；为防止表示坍塌，目标分支使用 stop-gradient。
- 理论上，论文在线性动力学下证明：若转移足够“straight”，规划 Hessian 的有效条件数更好，梯度下降收敛更快；并给出上界 $\kappa_{\mathrm{eff}}(H)\le \kappa(B)^2((1+\varepsilon)/(1-\varepsilon))^{2(K-1)}$。

## Results
- 论文声称在一组目标到达任务上，**open-loop 梯度规划成功率提升 20–60%**，**MPC 提升 20–30%**；这是摘要中给出的核心定量结论。
- 实验环境包括 **Wall、PointMaze UMaze、Medium Maze、PushT**，并与 **DINO-WM**（基于冻结 DINOv2 特征）比较。
- 论文展示了经过 straightening 后，潜在轨迹曲率下降、动作空间损失景观更接近凸形，梯度规划更稳定；但给定摘录中未提供完整表格数值。
- 在 PointMaze 可视化中，straightening 后的潜在欧氏距离热力图更接近 A-star 计算的真实 geodesic 距离，支持“距离更忠实”的关键主张。
- 作者还观察到：仅靠预测目标已有一定“隐式 straightening”，但显式曲率正则能进一步降低曲率并带来更好的规划表现。
- 就提供文本而言，最强的量化证据是 **20–60% open-loop** 与 **20–30% MPC** 的成功率增益；其余多为可视化和理论支持，缺少更多具体基线分数。

## Link
- [http://arxiv.org/abs/2603.12231v1](http://arxiv.org/abs/2603.12231v1)
