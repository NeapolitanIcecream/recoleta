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
language_code: en
---

# DreamSAC: Learning Hamiltonian World Models via Symmetry Exploration

## Summary
DreamSAC aims to make world models do more than just memorize pixel-level statistical patterns; it seeks to actively discover conservation laws and symmetries in physical systems. It combines a Hamiltonian dynamics world model with an "energy-change-based curiosity exploration" mechanism to improve extrapolative generalization to novel physical conditions.

## Problem
- Existing pixel-based world models are usually good at **interpolative generalization**, but perform poorly at extrapolation when faced with **unseen physical parameters or interaction mechanisms**.
- The root cause is that such models mostly learn **superficial statistical correlations** from passive data, rather than deeper physical principles such as mass, friction, gravity, and energy conservation.
- This matters because robots/agents in real environments often encounter out-of-distribution dynamics and contact conditions; without extrapolation, planning and control can fail quickly.

## Approach
- Proposes a **Hamiltonian World Model**: it organizes latent states into generalized coordinates `q` and momenta `p`, uses Hamilton's equations to describe internal dynamics, and applies a symplectic integrator for state transitions, injecting physical inductive bias through structure.
- Uses a **G-invariant** architecture (the paper uses a Lie Transformer) to constrain the internal Hamiltonian to be invariant under 3D symmetry group transformations, with the goal of learning physical laws independent of viewpoint.
- To resolve the conflict that pixel reconstruction requires viewpoint information while physical laws should be viewpoint-invariant, it adds a self-supervised **contrastive view-robustness loss**. Perspective perturbation/camera jitter augmentation is applied to single-view images so the encoder extracts invariant representations closer to physical state.
- Proposes **Symmetry Exploration**: the agent's intrinsic reward no longer mainly pursues statistical novelty, but instead rewards Hamiltonian changes caused by actions, `|H(z_{t+1}) - H(z_t)|``, i.e., actively "doing work" to challenge the parts of the current physics model with the greatest uncertainty.
- For training stability, exploration is bootstrapped with RND reward in the early stage, then linearly annealed to the physics-based reward above; the overall framework is built on DreamerV3-style imagination training and subsequent downstream fine-tuning.

## Results
- The paper claims that on **3D physics simulations**, it achieves **22%–163% higher performance** than SOTA baselines and adapts faster to unseen physical parameters (such as friction and gravity).
- **OOD downstream tasks (Table 2)**: DreamSAC reaches **321.90 ± 13.28** on Reacher-hard unseen view, higher than DreamerV3+RND's **313.97 ± 27.31** and DreamerV3+Policy's **265.33 ± 10.33**.
- **OOD downstream tasks (Table 2)**: On FetchReach unseen goal, DreamSAC scores **967.64 ± 9.29**, outperforming DreamerV3+RND's **927.36 ± 18.73** and DreamerV3+Policy's **919.73 ± 9.12**.
- **Parameter extrapolation (Table 2)**: On Walker-walk unseen gravity, DreamSAC scores **499.91 ± 19.77**, significantly higher than DreamerV3+Policy's **189.76 ± 23.27** and DreamerV3+RND's **167.52 ± 21.57**; on unseen dist., it scores **231.73 ± 67.08**, higher than **125.44 ± 35.70** and **113.40 ± 32.99**.
- **Parameter extrapolation (Table 2)**: On Cheetah-run unseen friction, DreamSAC scores **120.23 ± 41.26**, higher than DreamerV3+Policy's **118.79 ± 62.23** and DreamerV3+RND's **97.43 ± 67.82**; on unseen dist., it scores **126.33 ± 56.59**, higher than **103.42 ± 27.91** and **80.38 ± 28.43**.
- **World model prediction error (Table 1)**: DreamSAC usually achieves the lowest MSE across multiple environments, e.g., on Acrobot **H=16: 0.2064** and **H=100: 0.1806**; on Walker **H=16: 1.0044** and **H=100: 2.9118**; on FetchPush **H=8: 0.302**; on FetchReach **H=8: 0.313** and **H=16: 0.386**. The paper also explicitly states, for example, that on Acrobot H=16 it achieves a **10x+** error improvement over the DreamerV3 baseline.

## Link
- [http://arxiv.org/abs/2603.07545v1](http://arxiv.org/abs/2603.07545v1)
