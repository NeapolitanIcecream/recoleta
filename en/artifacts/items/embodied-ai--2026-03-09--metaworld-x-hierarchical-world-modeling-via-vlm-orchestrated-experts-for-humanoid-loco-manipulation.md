---
source: arxiv
url: http://arxiv.org/abs/2603.08572v1
published_at: '2026-03-09T16:28:26'
authors:
- Yutong Shen
- Hangxu Liu
- Penghui Liu
- Jiashuo Luo
- Yongkang Zhang
- Rex Morvley
- Chen Jiang
- Jianwei Zhang
- Lei Zhang
topics:
- humanoid-control
- world-model
- mixture-of-experts
- vision-language-models
- loco-manipulation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# MetaWorld-X: Hierarchical World Modeling via VLM-Orchestrated Experts for Humanoid Loco-Manipulation

## Summary
MetaWorld-X is a hierarchical world model framework for humanoid loco-manipulation. It decomposes complex control into multiple expert policies with human motion priors, and uses a VLM-supervised router to compose these experts according to task semantics, thereby improving naturalness, stability, and compositional generalization.

## Problem
- The paper aims to solve the following issue: when a single monolithic policy learns locomotion and manipulation simultaneously on high-degree-of-freedom humanoid robots, it is prone to cross-skill gradient interference, motion pattern conflicts, jitter, falls, and unnatural movements.
- This matters because if humanoid robots are to execute real-world multi-stage tasks, they must maintain balance, move, and perform fine manipulation at the same time; optimizing only task return often sacrifices motion naturalness and stability.
- Existing world model or MoE methods either suffer from long-horizon rollout bias and policy mismatch, or lack explicit semantic guidance, making it difficult to achieve stable and composable skill orchestration.

## Approach
- The core method is “divide and conquer”: first train a **Specialized Expert Pool (SEP)**, learning basic skills such as standing, walking, running, sitting, carrying, and reaching as separate experts, thereby avoiding conflicts among different skills within a single policy.
- Each expert is trained with **human motion data + imitation-constrained reinforcement learning**: motion retargeting maps MoCap/SMPL movements to the robot, then an energy-based reward based on joint position/velocity error is used to match human motion, making the resulting behavior more natural and biomechanically consistent.
- The framework retains **world model / latent planning**: imitation alignment rewards are incorporated into the world model’s reward head and value function, and MPPI/CEM planning is performed in latent space to improve sample efficiency and anticipatory control.
- Then an **Intelligent Routing Mechanism (IRM)** is trained: it takes the current observation and task semantics as input, outputs mixture weights for each expert, and the final action is the weighted sum of expert actions.
- This router is trained through **VLM-supervised distillation**: it first uses task-level semantic relevance for coarse alignment, then refines with few-shot demonstrations, enabling a transition from reliance on VLM guidance to autonomous routing, while supporting zero-shot/few-shot compositional generalization.

## Results
- On the basic skill evaluations in **Humanoid-bench**, IRM is stronger than strong baselines in both return and convergence speed: for example, on **Walk**, Ours reaches **1118.7±7.1**, higher than **TD-MPC2 644.2±162.3** and **DreamerV3 428.2±14.5**; convergence takes only **0.5M** steps, better than TD-MPC2’s **1.8M** and DreamerV3’s **6.0M**.
- The advantage is especially large on **Run**: Ours achieves **2056.9±13.6**, compared with **TD-MPC2 66.1±4.7** and **DreamerV3 298.5±84.5**; convergence takes **1.0M** steps, better than TD-MPC2’s **2.0M** and DreamerV3’s **6.0M**.
- Other basic skills also lead: **Stand 815.9±0.3 vs TD-MPC2 749.8±63.1**; **Sit 862.2±2.1 vs 733.9±120.6**; **Carry 963.5±5.1 vs 438.0±72.9**; and convergence is typically within **0.5–0.6M**, significantly faster than the baselines’ **1.1–6.0M**.
- In success rate over 10 independent trials, Ours reaches **9/10** on **Stand/Walk/Run/Carry**, and **Sit 8/10**; compared with **TD-MPC2** at only **3/10、3/10、2/10、3/10、4/10**, while PPO is mostly **0/10**.
- On complex manipulation tasks, MetaWorld-X also outperforms baselines: **Door 470.0±2.2 vs TD-MPC2 285.0±12.0**, **Basketball 250.0±11.9 vs 148.4±3.3**, **Push 70.0±2.1 vs -113.8±6.8**, **Truck 1500.0±15.6 vs 1213.2±1.1**, **Package -5200.0±47.2 vs -6788.5±552.7**.
- Ablations show that both key components are important: on the **Door** task, the **Full Model** achieves a return of **303.95** with **12.64w** training steps; removing the Router drops performance to **296.57 / 20.36w**; removing VLM or IL causes task failure (among them, **w/o IL** has return **193.61**, but cannot converge/adapt effectively).

## Link
- [http://arxiv.org/abs/2603.08572v1](http://arxiv.org/abs/2603.08572v1)
