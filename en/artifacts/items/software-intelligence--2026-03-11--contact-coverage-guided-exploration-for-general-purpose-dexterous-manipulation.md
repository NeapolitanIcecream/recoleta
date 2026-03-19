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
- contact-aware-learning
- robot-learning
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Contact Coverage-Guided Exploration for General-Purpose Dexterous Manipulation

## Summary
This paper proposes CCGE, a contact coverage-guided exploration method for general-purpose dexterous manipulation, using “which fingers contact which regions of the object” to drive reinforcement learning exploration. It aims to replace highly task-customized reward design, enabling dexterous hands to learn meaningful contact strategies more efficiently across multiple manipulation tasks.

## Problem
- Dexterous manipulation lacks a general, reusable default reward like Atari scores or walking speed; existing methods often rely on task-specific handcrafted rewards and priors, making cross-task generalization difficult.
- Traditional intrinsic rewards often encourage state novelty or dynamics prediction error, but in dexterous manipulation they frequently ignore the core factor of “contact,” which can lead to irrelevant behaviors such as flailing in the air or pushing objects away.
- Rewarding only after contact occurs is too sparse to provide effective guidance before contact, so a general exploration signal is needed that both focuses on contact and continuously guides behavior before contact happens.

## Approach
- CCGE represents contact as the relationship between predefined keypoints on the fingers and discretized regions on the object surface; in essence, it counts “which finger touched which object region.”
- The method maintains a contact counter `C[s,f,k]` conditioned on object-state clusters, where `s` is a discrete object-state cluster obtained through an autoencoder + binarization + SimHash, `f` is a finger, and `k` is an object surface region, preventing counts from interfering across different task stages or poses.
- It uses two kinds of rewards simultaneously: a post-contact count-based reward that encourages rare finger-region contacts, and a pre-contact energy-based reaching reward that guides fingers toward object regions that have not yet been sufficiently explored.
- To avoid getting trapped in local paths early in training, the authors modify both rewards to “only reward progress that exceeds the historical maximum within the current episode,” thereby mitigating detachment and short-sighted behavior.
- Overall training is still based on PPO, with exploration rewards added to task rewards, and the counter accumulates continuously during training without resetting.

## Results
- The paper claims to validate the method on four categories of simulated dexterous manipulation tasks: cluttered object singulation, constrained object retrieval, in-hand reorientation, and bimanual manipulation.
- The authors explicitly claim that CCGE “consistently achieves higher success rates and faster convergence” on these tasks, and that on hard exploration tasks (such as constrained object retrieval) baseline methods fail while CCGE remains strong.
- The paper also claims that the contact patterns learned by CCGE transfer robustly to real robotic systems; the experimental platform includes xArm + 16-DOF LEAP Hand.
- The provided text excerpt does not include specific numeric metrics, so it is not possible to accurately list success rates, sample efficiency gains, percentage improvements on datasets, or quantitative gaps versus each baseline.
- More specific experimental scope mentioned includes: in-hand reorientation uses ContactDB objects, and bimanual manipulation involves box-opening / lid-opening tasks from the ARCTIC dataset.

## Link
- [http://arxiv.org/abs/2603.10971v1](http://arxiv.org/abs/2603.10971v1)
