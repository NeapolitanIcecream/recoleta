---
source: arxiv
url: https://arxiv.org/abs/2606.27146v1
published_at: '2026-06-25T15:18:10'
authors:
- Jiayu Yang
- Tao Yang
- Weijun Li
- Xiang Chang
- Fei Chao
- Changjing Shang
- Qiang Shen
topics:
- vision-language-action
- robot-policy
- physical-feasibility
- self-reflection
- closed-loop-control
- manipulation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# PhysReflect-VLA: Physical Feasibility and Self-Reflective Regulation for Reliable Vision-Language-Action Policies

## Summary
PhysReflect-VLA adds runtime physical-feasibility checks and execution-error reflection to Vision-Language-Action robot policies. It improves real-robot long-horizon manipulation success by filtering bad action candidates and resampling after detected state mismatches.

## Problem
- VLA policies often execute sampled actions feed-forward, so they may choose motions that violate contact, geometry, or dynamic constraints.
- Small action errors can build up during long-horizon, contact-rich manipulation and cause task failure.
- Existing VLA policies usually do not compare predicted outcomes with observed outcomes during execution, so they have little basis for online correction.

## Approach
- The base VLA policy samples several candidate action segments for the current observation and language instruction.
- A forward model predicts the next abstract state for each action, and an inverse model tries to reconstruct the action from that predicted state change.
- The method scores each candidate with a cycle-consistency energy; low energy means the action produces a transition that the learned dynamics can predict and explain.
- After execution, the system compares the predicted next state with the observed next state. If the gap passes a threshold, a reflector generates a corrective guidance token such as reducing contact force or changing approach direction.
- Training has two stages: calibrate the forward/inverse feasibility models on real-robot transition data, then train the reflector and policy on teacher-labeled failure cases and corrective actions.

## Results
- On five real-robot manipulation tasks, Phys-OVLA reaches 79.6% average success versus 74.2% for OVLA-FT, a +5.4 point gain.
- Phys-OFT reaches 85.0% average success versus 82.0% for OVLA-OFT, a +3.0 point gain.
- Best task result in the table is Phys-OFT at 91.0% on Drawer-Cycle, compared with 89.0% for OVLA-OFT and 86.0% for ACT-S.
- Phys-OVLA improves over OVLA-FT on every listed task: Table-Bussy 75.0% vs 73.0%, Drawer-Cycle 84.0% vs 79.0%, Lid-Open 83.0% vs 77.0%, Shelf-Insert 76.0% vs 70.0%, Part-Assembly 80.0% vs 72.0%.
- Phys-OFT improves over OVLA-OFT on every listed task: Table-Bussy 86.0% vs 84.0%, Drawer-Cycle 91.0% vs 89.0%, Lid-Open 84.0% vs 80.0%, Shelf-Insert 79.0% vs 77.0%, Part-Assembly 85.0% vs 80.0%.
- The paper states that ablations show both feasibility checking and reflection-based correction contribute to execution reliability, but the excerpt does not include the ablation numbers.

## Link
- [https://arxiv.org/abs/2606.27146v1](https://arxiv.org/abs/2606.27146v1)
