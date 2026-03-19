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
language_code: en
---

# DreamSAC: Learning Hamiltonian World Models via Symmetry Exploration

## Summary
DreamSAC aims to enable world models to do more than just memorize pixel-level statistical patterns; instead, it seeks to actively discover conservation laws and symmetries in physical systems, thereby improving extrapolation to novel physical conditions. It combines a Hamiltonian dynamics world model with an active exploration mechanism based on "energy change," and achieves significantly better results than existing methods in 3D physics simulations.

## Problem
- Existing world models learned from pixels are typically good at **interpolative generalization**, but **extrapolative generalization** often fails when faced with unseen physical parameters or interaction rules.
- The root cause is that they mainly learn visual/statistical correlations rather than more stable **physical generative rules**, such as symmetries, conservation laws, and relationships between energy and momentum.
- This matters because agents in real open environments must still be able to predict and make decisions under changes in **gravity, friction, number of objects, and viewpoint**.

## Approach
- Proposes a **Hamiltonian World Model**: explicitly decomposes latent variables into generalized coordinates `q` and momentum `p`, models internal dynamics with a group-invariant Hamiltonian `Hϕ`, and advances states using a symplectic integrator.
- Proposes **Symmetry Exploration**: the agent’s intrinsic reward is not "novelty," but the predicted Hamiltonian change `|Hϕ(Zt+1)-Hϕ(Zt)|`, i.e., it is encouraged to perform interactions that most expose errors in its current physical understanding.
- To extract physically invariant states from viewpoint-dependent pixels, it adds a **self-supervised contrastive loss** that pulls together different viewpoint augmentations of the same observation, forcing the encoder to remove camera/viewpoint factors.
- The overall framework is built on DreamerV3: it first performs unsupervised pretraining, then fine-tunes on downstream tasks; the exploration reward is gradually annealed from RND to physics-driven reward to stabilize early training.

## Results
- The paper claims that on 3D physics simulations, it achieves **22%–163%** performance improvements over SOTA baselines, and can adapt more quickly to unseen physical parameters (such as gravity and friction).
- **Overall OOD task performance (Table 2)**: DreamSAC reaches **321.90±13.28** on Reacher-hard unseen view, higher than **313.97±27.31** for DreamerV3+RND and **265.33±10.33** for DreamerV3+Policy.
- **Structural generalization**: On FetchReach unseen goal, DreamSAC reaches **967.64±9.29**, outperforming **927.36±18.73** for DreamerV3+RND and **919.73±9.12** for DreamerV3+Policy; on Walker-walk unseen object it scores **0.80±0.09**, better than **0.70±0.07** and **0.65±0.12**; on Walker-walk unseen goal it scores **0.91±0.04**, better than **0.72±0.13** and **0.76±0.11**.
- **Parameter extrapolation**: On Walker-walk unseen gravity, DreamSAC scores **499.91±19.77**, significantly higher than **189.76±23.27** for DreamerV3+Policy and **167.52±21.57** for DreamerV3+RND; on Walker-walk unseen distribution it scores **231.73±67.08**, higher than **125.44±35.70** and **113.40±32.99**.
- **More parameter changes**: On Cheetah-run unseen friction, DreamSAC scores **120.23±41.26**, higher than **118.79±62.23** for DreamerV3+Policy and **97.43±67.82** for DreamerV3+RND; on unseen distribution it scores **126.33±56.59**, higher than **103.42±27.91** and **80.38±28.43**.
- **World model prediction error (Table 1)**: For example, on Acrobot, DreamSAC achieves an MSE of **0.2064** at **H=16**, outperforming **0.7723** for DreamerV3+Policy, **0.8423** for DreamerV3+Random, and slightly outperforming **0.2109** for DreamerV3+RND; at **H=100** it achieves **0.1806**, significantly better than **0.9392 / 1.7547 / 0.5628**. On FetchPush, **H=8** is **0.302**, better than **1.275 / 1.048 / 0.976**; on FetchReach, **H=16** is **0.313**, better than **0.855 / 0.962 / 0.574**.

## Link
- [http://arxiv.org/abs/2603.07545v1](http://arxiv.org/abs/2603.07545v1)
