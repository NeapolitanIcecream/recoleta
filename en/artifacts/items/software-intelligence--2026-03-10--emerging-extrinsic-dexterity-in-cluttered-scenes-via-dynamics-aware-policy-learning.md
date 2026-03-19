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
- robot-manipulation
- extrinsic-dexterity
- dynamics-aware-rl
- world-model
- sim-to-real
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Emerging Extrinsic Dexterity in Cluttered Scenes via Dynamics-aware Policy Learning

## Summary
This paper proposes DAPL, which first learns a dynamics representation of “how objects move after contact,” and then uses it to condition a reinforcement learning policy, enabling the robot to naturally learn non-prehensile manipulation by leveraging environmental contact in cluttered scenes. The method targets extrinsic dexterous manipulation in cluttered environments and demonstrates clear advantages in simulation, zero-shot real-world deployment, and grocery retrieval tasks.

## Problem
- Target problem: performing non-prehensile 6D object rearrangement in **cluttered, crowded scenes**, which requires the robot to selectively exploit or avoid multi-object contact. This form of “extrinsic dexterity” is more difficult than pure grasping.
- The challenge is that success depends not only on geometry, but also on coupled dynamics after contact, such as whether objects **slide, topple, or transfer momentum**. Most existing methods focus only on static geometry or rely on hand-crafted contact heuristics.
- This matters because in real environments, grasping often fails due to occlusion, clutter, or the lack of collision-free paths, while non-prehensile contact-based manipulation can compensate for the limitations of grasping.

## Approach
- The core mechanism is a two-stage learning process: first, train a **physics world model** that predicts the future positions and velocities of points in a point cloud under robot actions; then feed the model’s learned **dynamics features** into a reinforcement learning policy.
- The world model input includes not only point-cloud geometry, but also physical attributes such as **mass and velocity**; it uses a patch-based Transformer to encode coupled multi-object contact, and then an MLP predicts future motion at the point level.
- To avoid velocity prediction collapse caused by the fact that most points are nearly stationary, the authors add a **variance regularization term** to constrain the overall variation magnitude of the predicted velocity field to match the true distribution.
- In the policy learning stage, the dynamics representation, robot proprioceptive state, and target pose are jointly input into an actor-critic network, which outputs continuous joint control; the reward design remains simple and does not rely on complex reward shaping.
- The method also introduces **curriculum-style alternating training**: first use the current policy to collect about 60k steps of interaction data to update the world model, then continue training the policy with the improved dynamics representation, allowing the model and policy to improve jointly through iteration.

## Results
- On the newly proposed **Clutter6D** benchmark, DAPL significantly outperforms all baselines in unseen simulated scenes. Success rates are: Sparse **71.88%**, Moderate **51.04%**, Dense **44.56%**; the strongest representation-learning baseline, CORN, achieves **46.63% / 45.83% / 22.22%**, meaning DAPL delivers about a **2x** improvement in Dense scenes (44.56 vs. 22.22).
- Compared with the grasping baseline GraspGen + CuRobo, DAPL reaches **71.88/51.04/44.56%** on Sparse/Moderate/Dense, while the baseline reaches only **26.6/15.6/3.13%**; the paper abstract also summarizes this as a **more than 25%** success-rate improvement over grasping, human teleoperation, and prior representation-based policies on unseen cluttered simulated scenes.
- On the environment disturbance metric M.O., DAPL scores **12.65** in Dense scenes, lower than CORN’s **17.43**, indicating that it reduces disturbance to non-target objects while achieving higher success rates; in Moderate scenes, DAPL scores **2.7**, also better than CORN’s **5.51**.
- In terms of training efficiency, the authors state that DAPL reaches about **70%** success rate within the first few thousand iterations, clearly faster than methods based on static geometric representations.
- Ablation experiments (Sparse) show that the full configuration (point-level world model + velocity + physical features) achieves **71.88%** success rate with M.O. **2.59**; removing physical features while keeping velocity drops performance to **58.25%**, and removing both velocity and physical features drops it further to **42.00%**; if replaced with simple reconstruction pretraining, performance is only **11.75%** or **29.63%**, showing that dynamics modeling is the key.
- During curriculum learning iterations, the success rate improves from **61.3%** to **71.8%** (after 3 iterations). In zero-shot real-world deployment across **10** cluttered scenes, the success rate is about **50%**, comparable to human teleoperation, but with shorter average execution time: **42.6s vs. 55.9s**.

## Link
- [http://arxiv.org/abs/2603.09882v1](http://arxiv.org/abs/2603.09882v1)
