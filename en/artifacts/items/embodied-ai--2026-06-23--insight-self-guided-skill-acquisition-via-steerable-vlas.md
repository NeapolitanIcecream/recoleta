---
source: arxiv
url: https://arxiv.org/abs/2606.24884v1
published_at: '2026-06-23T17:59:01'
authors:
- Maggie Wang
- Lars Osterberg
- Stephen Tian
- Ola Shorinwa
- Jiajun Wu
- Mac Schwager
topics:
- vision-language-action
- robot-skill-acquisition
- steerable-policies
- continual-learning
- manipulation-primitives
- robot-data-scaling
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# InSight: Self-Guided Skill Acquisition via Steerable VLAs

## Summary
InSight trains a VLA to execute named manipulation primitives and then adds missing primitives through VLM-guided robot rollouts, with no human demonstrations for the target skills. This helps a robot extend its learned policy after deployment instead of relying only on its original demonstration set.

## Problem
- VLAs learn the manipulation behaviors present in their demonstration data, so a robot trained on pick-and-place, drawer opening, or scooping can fail at flipping, closing, pouring, twisting, or sweeping.
- Collecting human demonstrations for every new target skill is costly, and reinforcement learning can require too many trials for real robot use.

## Approach
- InSight first splits teleoperated demonstrations into labeled primitive segments using a VLM plan, gripper-state transitions, end-effector motion, and dominant motion axes.
- Each primitive segment becomes a separate training episode, and the VLA is fine-tuned with the primitive label as the language prompt plus a learned progress signal for termination.
- For a new task, a VLM writes a primitive plan and flags any primitive label missing from the VLA vocabulary.
- Known primitives run through the steerable VLA. Missing primitives run through a low-level controller using a VLM-chosen single-axis translation or rotation and signed magnitude.
- A VLM oracle checks task success, successful new primitive segments are added to the dataset, and the VLA is retrained so those primitives become reusable policy actions.

## Results
- In simulation block flipping, the method used 150 pick-and-place demonstrations split into more than 700 primitive episodes across 7 primitive types. It reached 75% flip success after 246 acquired rotate-block primitive rollouts over 479 total attempts; SAC reached 0% full flips with the same rollout budget, while reaching 23% reach and 10% grasp.
- In simulation drawer closing, it started from 50 drawer-opening demonstrations split into 3 primitives. It collected 70 successful close-drawer primitives from 82 episodes, then closed the drawer with 100% success over 25 evaluation trials while retaining drawer opening.
- On real xArm twist and pour tasks, the base VLA was trained on 50 pick-and-place demonstrations and InSight added 20 successful acquired primitive episodes. It reached 92% twist success and 96% pour success, compared with 32% and 16% for CaP-X and 0% for the pi_0.5 baseline without new primitives.
- On the real long-horizon twist-then-pour task, it chained 14 primitives with no end-to-end demonstrations and reached 80% success, compared with 4% for CaP-X.
- Real-world acquisition needed 23 trials and 39.7 minutes wall time to get 20 successful twist primitives, and 31 trials and 85.3 minutes wall time to get 20 successful pour primitives.
- After adding twist and pour, the unified VLA retained 100% success on the original top- and side-pick-and-place skills over 15 trials, and the sweeping task succeeded in 5/5 evaluation trials from scooping-only demonstrations.

## Link
- [https://arxiv.org/abs/2606.24884v1](https://arxiv.org/abs/2606.24884v1)
