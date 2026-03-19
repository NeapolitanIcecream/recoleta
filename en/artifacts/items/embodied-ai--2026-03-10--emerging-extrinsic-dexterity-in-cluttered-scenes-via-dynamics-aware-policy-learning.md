---
source: arxiv
url: http://arxiv.org/abs/2603.09882v1
published_at: '2026-03-10T16:40:30'
authors:
- Yixin Zheng
- Jiangran Lyu
- Yifan Zhang
- Jiayi Chen
- Mi Yan
- Yuntian Deng
- Xuesong Shi
- Xiaoguang Zhao
- Yizhou Wang
- Zhizheng Zhang
- He Wang
topics:
- extrinsic-dexterity
- non-prehensile-manipulation
- world-model
- sim2real
- cluttered-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Emerging Extrinsic Dexterity in Cluttered Scenes via Dynamics-aware Policy Learning

## Summary
This paper proposes DAPL, which first learns a dynamics representation of “how objects move after contact,” and then uses it to condition a reinforcement learning policy, enabling the robot to naturally learn non-prehensile manipulation by leveraging environmental contact in crowded, cluttered scenes. The method targets extrinsic dexterity and demonstrates performance superior to geometric representations and grasping-based baselines in simulation, zero-shot real-world settings, and a practical grocery-picking deployment.

## Problem
- The task is **non-prehensile 6D object rearrangement in cluttered scenes**: the robot must not only move the target object, but also selectively exploit or avoid collisions amid coupled contact interactions among multiple objects.
- This matters because in crowded, occluded, hard-to-grasp real environments, grasping alone and collision-free planning often fail; success frequently depends on extrinsic dexterous actions such as pushing, sliding, and flipping.
- Most existing methods focus only on static geometry and lack explicit dynamics modeling, so they struggle in dense clutter to infer the outcomes of post-contact sliding, tipping, and momentum transfer.

## Approach
- The core method is **Dynamics-Aware Policy Learning (DAPL)**: it first trains a physics world model that takes as input the point clouds of the target object, surrounding scene, and end effector, augmented with physical properties such as **mass and velocity**, and predicts the positions and velocities of all points at the next time step after an action.
- This world model uses a **patch-based Transformer/ViT + MLP decoder** to learn latent dynamics features capturing “what consequences contact will bring”; these features are then provided as conditioning inputs to an Actor-Critic reinforcement learning policy.
- To avoid velocity prediction collapsing toward near-zero because most points are stationary, the authors add a **velocity variance regularization term**, allowing the model to preserve motion magnitude and spatial variation in dynamic regions.
- Training uses **alternating curriculum learning**: it first collects about **60k** steps of interaction data with the current policy, then updates the world model, then continues training the policy with the updated dynamics representation, repeating this cycle until convergence.
- The authors also build the **Clutter6D** benchmark: based on IsaacLab/PhysX, containing **10K** normalized object assets, and testing 6D rearrangement under **4/8/12** objects for sparse / moderate / dense clutter levels.

## Results
- On unseen simulated scenes in **Clutter6D**, DAPL achieves success rates of **Sparse 71.88% / Moderate 51.04% / Dense 44.56%**. The strong baseline **CORN** achieves **46.63% / 45.83% / 22.22%**, showing that in dense scenes DAPL improves by about **22.34 percentage points**, nearly doubling the strongest baseline; consistent with the paper abstract’s summary, it exceeds various baselines by **25%+** in success rate.
- Compared with grasping-based **GraspGen + CuRobo**, DAPL achieves **71.88 vs 26.6 / 51.04 vs 15.6 / 44.56 vs 3.13** on **Sparse/Moderate/Dense**, showing that non-prehensile extrinsic dexterity is clearly more effective in dense clutter.
- Compared with human teleoperation, DAPL is also stronger in simulation: humans achieve **50.0% / 40.0% / 20.0%**, while DAPL achieves **71.88% / 51.04% / 44.56%**; meanwhile, disturbance to non-target objects (M.O.) in Dense is **12.65 cm**, lower than CORN’s **17.43 cm**.
- In terms of training efficiency, the authors state that the method reaches about **70%** success rate early in training, while the geometric-representation baseline converges more slowly, indicating that the dynamics representation improves sample efficiency.
- Ablation experiments (Sparse) show that the full **point-level world model + velocity + physical properties** performs best, reaching **71.88%** success rate with **2.59 cm** disturbance; removing physical properties drops performance to **58.25%**, switching to an object-level world model yields only **16.88%**, and simple reconstruction pretraining yields only **29.63%** or **11.75%**, indicating that point-level dynamics supervision is the most critical factor.
- Curriculum learning is effective: success rate rises from **61.3%** to **71.8%** over iterations (after 3 rounds). In zero-shot real-world deployment across **10** cluttered scenes, success rate is about **50%**, comparable to human teleoperation, but with shorter average execution time: **42.6s vs 55.9s**. In addition, the paper also claims a practical **grocery picking** deployment, though the excerpt does not provide further quantitative details.

## Link
- [http://arxiv.org/abs/2603.09882v1](http://arxiv.org/abs/2603.09882v1)
