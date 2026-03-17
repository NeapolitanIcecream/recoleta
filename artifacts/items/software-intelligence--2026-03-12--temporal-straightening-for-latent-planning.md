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
- world-models
- latent-planning
- representation-learning
- trajectory-regularization
- gradient-based-planning
relevance_score: 0.31
run_id: materialize-outputs
---

# Temporal Straightening for Latent Planning

## Summary
本文提出一种用于潜在规划的表示学习正则化方法“temporal straightening”，通过让潜在轨迹在时间上更“直”，改善世界模型中的距离度量与梯度规划稳定性。核心思想是联合训练编码器和动力学预测器，并惩罚相邻潜在速度方向的弯曲。

## Problem
- 潜在世界模型虽然能压缩高维观测并支持规划，但其潜在空间常常**高度弯曲**，导致规划目标非凸、梯度优化困难。
- 预训练视觉特征（如 DINOv2）语义强，但**不是为规划而设计**，会保留与控制无关甚至有害的信息。
- 当潜在轨迹弯曲时，**欧氏距离不能真实反映可达路径上的测地距离**，从而误导目标到达型规划。

## Approach
- 构建一个联合学习的世界模型：感知编码器将观测映射到 latent，动作编码器嵌入动作，预测器根据过去的 latent 与动作预测下一步 latent。
- 在常规预测损失之外，引入**曲率正则项**：取连续三帧 latent，计算两段速度向量 $v_t=z_{t+1}-z_t$ 与 $v_{t+1}=z_{t+2}-z_{t+1}$ 的余弦相似度，并最小化 $1-\cos(v_t,v_{t+1})$。
- 直观上，这等价于鼓励轨迹局部少拐弯，让 latent 中“直线距离”更接近真实可行轨迹距离，从而让规划目标更好优化。
- 训练时总损失为预测误差加上加权曲率损失，并通过 stop-gradient 防止表示塌缩。
- 论文还给出线性动力学分析：若转移接近“straight”（$\|A-I\|_2\le \epsilon$），则规划 Hessian 条件数更好，意味着梯度下降收敛更快、更稳定。

## Results
- 论文声称在一组 goal-reaching 任务上，**open-loop 梯度规划成功率提升 20%–60%**，相对未直化表示有显著增益。
- 在 **MPC** 设置下，成功率也提升 **20%–30%**。
- 理论上，在线性动力学下，若转移满足 $\varepsilon$-straight，则规划 Hessian 的有效条件数满足：$\kappa_{\mathrm{eff}}(H)\le \kappa(B)^2\left(\frac{1+\varepsilon}{1-\varepsilon}\right)^{2(K-1)}$；当 $\varepsilon\le 1/2$ 时，进一步有 $\kappa_{\mathrm{eff}}(H)\le \kappa(B)^2 e^{6\varepsilon K}$。
- 实验覆盖 **Wall、PointMaze UMaze、Medium Maze、PushT**，并以 **DINO-WM / frozen DINOv2 features** 为主要比较基线。
- 文中定性结果显示：直化后 latent trajectory 更平滑，动作空间 loss landscape 更接近凸形，latent 欧氏距离与 A-star geodesic 更一致。
- 摘要与正文摘录未给出每个数据集的完整逐项数值表，但最明确的量化主张是上述 **20–60%（open-loop）** 和 **20–30%（MPC）** 的成功率提升。

## Link
- [http://arxiv.org/abs/2603.12231v1](http://arxiv.org/abs/2603.12231v1)
