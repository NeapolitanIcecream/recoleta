---
source: arxiv
url: https://arxiv.org/abs/2606.30290v1
published_at: '2026-06-29T13:31:27'
authors:
- Ritwik Sharma
- Shivam Sood
- Arhaan Jain
- Shyam Charan Kesavamoorthi
- Chengyang He
- Guillaume Sartoretti
topics:
- cross-morphology-retargeting
- robot-motion-priors
- legged-robot-learning
- human-motion-data
- sim2sim-tracking
- video-teleoperation
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# X-Morph: Human Motion Priors for Scalable Robot Learning Across Morphologies

## Summary
X-Morph converts human motion into executable legged-robot behaviors for quadrupeds, hexapods, and quadruped-manipulator systems. It uses human motion as reusable training data when robot-specific motion datasets are scarce.

## Problem
- Non-humanoid legged robots lack large motion datasets, so each new morphology often needs robot-specific demonstrations, hand-built rewards, or small skill libraries.
- Direct human-to-robot retargeting can look plausible while producing foot slip, ground penetration, floating contacts, joint-limit issues, or references that a robot cannot track.
- The problem matters because scalable robot learning needs reusable behavior data across bodies that do not share a human skeleton.

## Approach
- X-Morph first maps human or G1 humanoid motion into a target robot reference using morphology-aware body-part correspondences, such as human legs to quadruped legs or human arms to front legs.
- A physics-aware temporal corrector edits the retargeted clip to reduce foot skating, penetration, floating feet, root drift, and end-effector errors.
- A privileged reinforcement-learning teacher tracks the corrected references using full-state information and tracking rewards.
- A causal student policy is distilled from the teacher and runs with deployable proprioception plus a compact current and one-step-future reference stream.
- For interactive use, a causal retargeting model maps recent G1 motion to cleaned robot references for video teleoperation; text prompts can also generate or retrieve human motion that is retargeted and tracked.

## Results
- The system is evaluated on 3 target morphologies: a Go2 quadruped, a Yuna hexapod, and a B2-Z1 quadruped with a manipulator.
- In a Go2 ablation on 33 matched locomotion clips, the physics corrector reduces foot slip from 58.76 cm/s to 42.76 cm/s, a 27.2% drop.
- The same Go2 ablation reduces penetration p95 from 11.34 cm to 6.02 cm, a 46.9% drop; contact-height error falls from 6.45 cm to 3.60 cm, a 44.2% drop.
- For Yuna hexapod sim2sim tracking under live video reference streaming, corrected references reduce joint MAE from 6.57 degrees to 5.45 degrees, a 17.4% improvement.
- The Yuna tracking test also reduces root velocity RMSE from 0.479 m/s to 0.413 m/s, yaw-rate RMSE from 0.896 rad/s to 0.651 rad/s, and mean foot slip from 29.29 cm/s to 24.30 cm/s.
- The live video pipeline publishes retargeted robot references at up to 28.9 Hz from a 30 Hz camera stream; text-conditioned execution and a hexapod door-opening prior are shown as qualitative demonstrations, without a controlled sample-efficiency comparison.

## Link
- [https://arxiv.org/abs/2606.30290v1](https://arxiv.org/abs/2606.30290v1)
