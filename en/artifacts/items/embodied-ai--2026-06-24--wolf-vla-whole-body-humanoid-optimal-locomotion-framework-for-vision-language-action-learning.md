---
source: arxiv
url: https://arxiv.org/abs/2606.25591v1
published_at: '2026-06-24T08:59:59'
authors:
- Melya Boukheddimi
- Omar Adjali
- Daniel Sontag
- Frank Kirchner
topics:
- vision-language-action
- humanoid-locomotion
- optimal-control
- synthetic-robot-data
- whole-body-control
- robot-foundation-models
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# WOLF-VLA: Whole-Body Humanoid Optimal Locomotion Framework for Vision-Language-Action Learning

## Summary
WOLF-VLA trains a vision-language-action policy for whole-body humanoid locomotion using optimal-control-generated demonstrations instead of teleoperation. The paper’s main claim is that optimal-control trajectories can give VLA training data that are dynamically feasible, contact-consistent, and scalable.

## Problem
- Existing VLA work mostly targets fixed-base manipulation or lower-complexity robot tasks, leaving contact-rich humanoid locomotion with limited VLA datasets and benchmarks.
- Teleoperated or motion-capture data are costly to collect and often lack explicit torque, joint-limit, contact, and energy criteria.
- Humanoid locomotion needs demonstrations that respect dynamics and safety constraints because falls, torque saturation, and contact errors can make learned policies unusable.

## Approach
- The system generates humanoid demonstrations by solving multi-phase optimal-control problems for walking, side-walking, stair ascent, stair ascent/descent, 180° turning, and squatting.
- Each trajectory minimizes costs such as center-of-mass tracking error, foot tracking error, torque, and posture deviation while enforcing joint, velocity, torque, and contact constraints.
- The demonstrations run in MuJoCo with RH5, a humanoid with a free-flyer and 25 actuated joints; the recorded inputs include proprioception, egocentric RGB frames, and natural-language task instructions.
- The VLA policy is initialized from GR00T-N1.5-3B; its language and vision encoders stay frozen while projector layers and the action diffusion module are trained with flow matching.
- Language instructions include structured distance and height tags so the model can connect task text to target placement and stair height.

## Results
- The excerpt gives no numeric success-rate table or direct policy performance numbers, although it says the trained model has competitive performance and tests modality ablations.
- WOLF-VLA-dataset contains 277 hours of humanoid motion across six locomotion task families.
- Table I reports 15,276 episodes with 28 s average episode length: WF 2,874 episodes at 13.5 s, WA 8,234 at 43.2 s, W.CS.U 2,358 at 21.6 s, and W.CS.U/D 1,810 at 33.6 s.
- Scene variation includes six target types, six colors, about 40 × 40 target placements, and random visual distractors.
- Visual data are captured at 33.33 Hz as 224 × 224 RGB frames from a 120° egocentric camera.
- Training uses 4 NVIDIA A100 GPUs, 200,000 gradient steps, effective batch size 128, 500 warmup steps, peak learning rate 1e-4, and final learning rate 1e-5.

## Link
- [https://arxiv.org/abs/2606.25591v1](https://arxiv.org/abs/2606.25591v1)
