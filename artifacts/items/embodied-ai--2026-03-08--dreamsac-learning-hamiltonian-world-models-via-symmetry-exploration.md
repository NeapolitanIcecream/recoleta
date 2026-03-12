---
source: arxiv
url: http://arxiv.org/abs/2603.07545v1
published_at: '2026-03-08T09:09:57'
authors:
- Jinzhou Tang
- Fan Feng
- Minghao Fu
- Wenjun Lin
- Biwei Huang
- Keze Wang
topics:
- world-model
- hamiltonian-dynamics
- curiosity-driven-exploration
- ood-generalization
- model-based-rl
relevance_score: 0.34
run_id: materialize-outputs
---

# DreamSAC: Learning Hamiltonian World Models via Symmetry Exploration

## Summary
DreamSAC 试图让世界模型不只记住像素统计规律，而是主动去发现物理系统中的守恒律与对称性。它把哈密顿动力学世界模型与一种“基于能量变化的好奇心探索”结合起来，以提升对新物理条件的外推泛化能力。

## Problem
- 现有从像素学习的世界模型通常擅长**插值泛化**，但面对**未见过的物理参数或交互机制**时，外推能力很差。
- 根因是这类模型多在被动数据上学习**表面统计相关性**，而不是质量、摩擦、重力、能量守恒等更底层的物理规律。
- 这很重要，因为真实环境中的机器人/智能体经常会遇到训练分布外的动力学与接触情况，若不能外推，规划与控制会迅速失效。

## Approach
- 提出 **Hamiltonian World Model**：把潜状态按广义坐标 `q` 和动量 `p` 组织，用哈密顿方程描述内部动力学，并用辛积分器做状态推进，从结构上注入物理归纳偏置。
- 通过 **G-invariant** 架构（文中用 Lie Transformer）约束内部哈密顿量对 3D 对称群变换不变，目标是让模型学习与视角无关的物理规律。
- 为解决“重建像素需要视角信息，但物理规律应视角不变”的冲突，加入自监督**对比学习视角鲁棒损失**，对单视角图像做透视扰动/相机抖动增强，使编码器提取更接近物理状态的不变表示。
- 提出 **Symmetry Exploration**：智能体的内在奖励不再主要追求统计新奇性，而是奖励动作引起的哈密顿量变化 `|H(z_{t+1}) - H(z_t)|``，也就是主动“做功”去挑战当前物理模型最不确定的地方。
- 为训练稳定性，前期用 RND 奖励启动探索，随后线性退火到上述基于物理的奖励；整体框架建立在 DreamerV3 式的想象训练与后续下游微调之上。

## Results
- 论文声称在 **3D physics simulations** 上，相比 SOTA 基线实现 **22%–163% 更高性能**，并能更快适应未见物理参数（如摩擦、重力）。
- **OOD 下游任务（Table 2）**：DreamSAC 在 Reacher-hard unseen view 上达到 **321.90 ± 13.28**，高于 DreamerV3+RND 的 **313.97 ± 27.31** 和 DreamerV3+Policy 的 **265.33 ± 10.33**。
- **OOD 下游任务（Table 2）**：FetchReach unseen goal 上 DreamSAC 为 **967.64 ± 9.29**，优于 DreamerV3+RND 的 **927.36 ± 18.73** 与 DreamerV3+Policy 的 **919.73 ± 9.12**。
- **参数外推（Table 2）**：Walker-walk unseen gravity 上 DreamSAC 为 **499.91 ± 19.77**，显著高于 DreamerV3+Policy 的 **189.76 ± 23.27** 和 DreamerV3+RND 的 **167.52 ± 21.57**；在 unseen dist. 上为 **231.73 ± 67.08**，高于 **125.44 ± 35.70** 与 **113.40 ± 32.99**。
- **参数外推（Table 2）**：Cheetah-run unseen friction 上 DreamSAC 为 **120.23 ± 41.26**，高于 DreamerV3+Policy 的 **118.79 ± 62.23** 和 DreamerV3+RND 的 **97.43 ± 67.82**；unseen dist. 上为 **126.33 ± 56.59**，高于 **103.42 ± 27.91** 与 **80.38 ± 28.43**。
- **世界模型预测误差（Table 1）**：DreamSAC 在多环境上通常取得最低 MSE，例如 Acrobot 上 **H=16: 0.2064**、**H=100: 0.1806**；Walker 上 **H=16: 1.0044**、**H=100: 2.9118**；FetchPush 上 **H=8: 0.302**；FetchReach 上 **H=8: 0.313**、**H=16: 0.386**。文中还明确举例称 Acrobot H=16 相比 DreamerV3 基线有 **10x+** 误差改善。

## Link
- [http://arxiv.org/abs/2603.07545v1](http://arxiv.org/abs/2603.07545v1)
