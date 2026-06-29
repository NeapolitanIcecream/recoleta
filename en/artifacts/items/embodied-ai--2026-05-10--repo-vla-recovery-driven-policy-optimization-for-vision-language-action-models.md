---
source: arxiv
url: https://arxiv.org/abs/2605.09410v1
published_at: '2026-05-10T08:24:05'
authors:
- Weijia Liufu
- Xiaoyu Guo
- Ruiyi Chen
- Jingzhi Liu
- Kaidong Zhang
- Xiwen Liang
- Jianqi Lin
- Dawei Sun
- Yuze Wang
- Rongtao Xu
- Bingqian Lin
- Bowen Yang
- Tongtong Cao
- Bowen Peng
- Dongyu Zhang
- Guangrun Wang
- Min Wang
- Liang Lin
- Xiaodan Liang
topics:
- vision-language-action
- robot-recovery
- bimanual-manipulation
- robot-data-scaling
- generalist-robot-policy
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# RePO-VLA: Recovery-Driven Policy Optimization for Vision-Language-Action Models

## Summary
RePO-VLA trains VLA robot policies to recover after contact-rich manipulation drift by using success, failure, and recovery rollouts with different labels. It reports adversarial success rising from 20% to 75% on average, with up to 80% in scaled real-world trials.

## Problem
- Long-horizon bimanual tasks can fail after small grasp, contact, or timing errors, even when the robot could still recover.
- Success-only imitation gives weak supervision for drift and often discards failed rollouts that contain useful early behavior.
- Naive imitation of recovery episodes can mix the actions that caused drift with the actions that repaired it.

## Approach
- Recovery-Aware Initialization slices recovery segments out of full episodes and resets observation history, so the policy learns correction from the current adverse state.
- A Progress-Aware Semantic Value Function uses frozen V-JEPA trajectory features, language embeddings, and successful reference trajectories to assign dense progress labels.
- Failed trajectories keep useful prefixes through a reliability decay label, with alpha = 3.0, while terminal drift gets low value.
- Value-Conditioned Refinement trains a flow-matching pi_0.5 policy with a value token, using success, raw recovery, and failure data together.
- At deployment, the policy uses normal rolling history and a fixed value condition v = 1.0, with no online failure detector or hand-coded retry rule.

## Results
- The paper claims average adversarial success improves from 20% to 75%, with up to 80% success in scaled real-world trials.
- FRBench-Sim contains 23,453 simulated bimanual episodes across 46 tasks: 17,061 nominal success episodes and 6,392 verified failure-recovery episodes.
- FRBench uses 4 injected error types: premature close, grasp slip, grasp position offset, and grasp orientation mismatch.
- Error-injection coverage includes 8,022 premature-close cases, 3,516 grasp-slip cases, 4,686 position-offset cases, and 688 orientation-mismatch cases before final filtering.
- The simulation protocol runs 50 rollouts per task and injects a grasp disturbance by holding the gripper open for 30 frames, about 1 second.

## Link
- [https://arxiv.org/abs/2605.09410v1](https://arxiv.org/abs/2605.09410v1)
