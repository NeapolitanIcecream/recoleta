---
source: arxiv
url: http://arxiv.org/abs/2603.10971v1
published_at: '2026-03-11T16:55:49'
authors:
- Zixuan Liu
- Ruoyi Qiao
- Chenrui Tie
- Xuanwei Liu
- Yunfan Lou
- Chongkai Gao
- Zhixuan Xu
- Lin Shao
topics:
- dexterous-manipulation
- reinforcement-learning
- intrinsic-exploration
- contact-modeling
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Contact Coverage-Guided Exploration for General-Purpose Dexterous Manipulation

## Summary
This paper proposes CCGE, a contact coverage-guided exploration method for general-purpose dexterous manipulation, which uses “which fingers contact which regions of the object” to generate task-agnostic exploration rewards. Its goal is to help dexterous hands learn meaningful contact strategies more efficiently when handcrafted reward design is unavailable, while also supporting transfer from simulation to real systems.

## Problem
- Dexterous manipulation lacks reusable default rewards like game scores or velocity tracking, and existing methods often rely on task-specific handcrafted shaping or priors.
- If general exploration methods reward only state novelty or dynamics prediction error, they often encourage behaviors unrelated to manipulation, such as flailing in the air or pushing objects away, rather than establishing effective contact.
- For dexterous hands, what truly matters is **contact pattern exploration**: different fingers contact different object regions at different stages of a task, which determines whether subsequent grasping, reorientation, or bimanual coordination is possible.

## Approach
- Represent the contact state as the “intersection between finger keypoints and object surface regions,” and count contacts for finger-region pairs under different object-state clusters; rarer contact patterns receive higher rewards.
- Use learned hashing to discretize current/target object states into state clusters, and maintain an independent contact counter for each cluster, preventing contact patterns learned in one state from suppressing exploration in another.
- Design two complementary rewards: after contact, use a count-based contact coverage reward to encourage novel finger-region contacts; before contact, use an energy-based reaching reward to guide fingers toward under-explored object regions.
- To avoid getting stuck in local trajectories early in training, the authors reward only contact/energy progress within a single episode that exceeds the historical best, thereby suppressing detachment and short-sighted oscillation.

## Results
- The paper claims to evaluate CCGE on four categories of simulated dexterous manipulation tasks: cluttered object singulation, constrained object retrieval, in-hand reorientation, and bimanual manipulation.
- The text’s explicit conclusion is that, compared with existing exploration methods, CCGE achieves **higher success rates** and **faster convergence / better sample efficiency** on these tasks; Figure 4 further specifically notes that on “hard exploration” tasks such as **Constrained Object Retrieval**, baseline methods fail while CCGE performs more strongly.
- The authors also claim that the contact patterns learned by CCGE can **transfer robustly to real robotic systems** and maintain effective contact behaviors in the real world.
- This abstract/excerpt **does not provide specific numerical metrics** (such as success rate percentages, training steps, or exact improvement margins over baselines), so it is not possible to list precise quantitative comparisons for metrics/datasets/baselines. The strongest concrete claim is that, in dexterous manipulation involving multiple tasks and rich multi-stage contact, CCGE consistently outperforms existing exploration methods and supports sim-to-real transfer.

## Link
- [http://arxiv.org/abs/2603.10971v1](http://arxiv.org/abs/2603.10971v1)
