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
- world-models
- model-based-rl
- hamiltonian-dynamics
- curiosity-driven-exploration
- ood-generalization
relevance_score: 0.28
run_id: materialize-outputs
language_code: zh-CN
---

# DreamSAC: Learning Hamiltonian World Models via Symmetry Exploration

## Summary
DreamSAC 试图让世界模型不只记住像素统计规律，而是主动发现物理系统中的守恒律与对称性，从而提升对新物理条件的外推能力。它把哈密顿动力学世界模型与一种基于“能量变化”的主动探索机制结合起来，在3D物理仿真中取得了显著优于现有方法的结果。

## Problem
- 现有从像素学习的世界模型通常擅长**插值泛化**，但面对未见过的物理参数或交互规律时，**外推泛化**容易失效。
- 根因是它们主要学习了视觉/统计相关性，而不是更稳定的**物理生成规则**，如对称性、守恒律、能量与动量关系。
- 这很重要，因为真实开放环境中的智能体必须在**新重力、摩擦、物体数量、视角**等变化下仍能预测和决策。

## Approach
- 提出 **Hamiltonian World Model**：把潜变量显式分成广义坐标 `q` 和动量 `p`，并用满足群不变性的哈密顿量 `Hϕ` 建模内部动力学，用辛积分器推进状态。
- 提出 **Symmetry Exploration**：智能体的内在奖励不是“新奇度”，而是预测的哈密顿量变化 `|Hϕ(Zt+1)-Hϕ(Zt)|`，即鼓励去做最能暴露当前物理理解错误的交互。
- 为了从视角相关的像素中提取物理不变状态，加入**自监督对比损失**，对同一观测的不同视角增强进行拉近，逼迫编码器去掉相机/视角因素。
- 整体框架建立在 DreamerV3 上：先进行无监督预训练，再针对下游任务微调；探索奖励从 RND 逐步退火到物理驱动奖励，以稳定早期训练。

## Results
- 论文声称在 3D physics simulations 上，相比 SOTA 基线取得 **22%–163%** 的性能提升，并且能更快适应未见物理参数（如重力、摩擦）。
- **OOD任务总体表现（表2）**：DreamSAC 在 Reacher-hard unseen view 达到 **321.90±13.28**，高于 DreamerV3+RND 的 **313.97±27.31** 和 DreamerV3+Policy 的 **265.33±10.33**。
- **结构泛化**：FetchReach unseen goal 上，DreamSAC 达到 **967.64±9.29**，优于 DreamerV3+RND 的 **927.36±18.73** 和 DreamerV3+Policy 的 **919.73±9.12**；Walker-walk unseen object 上为 **0.80±0.09**，优于 **0.70±0.07** 与 **0.65±0.12**；Walker-walk unseen goal 上为 **0.91±0.04**，优于 **0.72±0.13** 与 **0.76±0.11**。
- **参数外推**：Walker-walk unseen gravity 上，DreamSAC 为 **499.91±19.77**，显著高于 DreamerV3+Policy 的 **189.76±23.27** 和 DreamerV3+RND 的 **167.52±21.57**；Walker-walk unseen distribution 为 **231.73±67.08**，高于 **125.44±35.70** 与 **113.40±32.99**。
- **更多参数变化**：Cheetah-run unseen friction 上，DreamSAC 为 **120.23±41.26**，高于 DreamerV3+Policy 的 **118.79±62.23** 和 DreamerV3+RND 的 **97.43±67.82**；unseen distribution 上为 **126.33±56.59**，高于 **103.42±27.91** 与 **80.38±28.43**。
- **世界模型预测误差（表1）**：例如 Acrobot，DreamSAC 在 **H=16** 时 MSE 为 **0.2064**，优于 DreamerV3+Policy 的 **0.7723**、DreamerV3+Random 的 **0.8423**，也略优于 DreamerV3+RND 的 **0.2109**；在 **H=100** 时为 **0.1806**，显著优于 **0.9392 / 1.7547 / 0.5628**。FetchPush 上 **H=8** 为 **0.302**，优于 **1.275 / 1.048 / 0.976**；FetchReach 上 **H=16** 为 **0.313**，优于 **0.855 / 0.962 / 0.574**。

## Link
- [http://arxiv.org/abs/2603.07545v1](http://arxiv.org/abs/2603.07545v1)
