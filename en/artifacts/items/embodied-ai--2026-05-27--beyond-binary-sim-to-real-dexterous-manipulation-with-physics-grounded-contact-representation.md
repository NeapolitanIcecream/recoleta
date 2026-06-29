---
source: arxiv
url: https://arxiv.org/abs/2605.28812v1
published_at: '2026-05-27T17:59:02'
authors:
- Jiahe Pan
- Stelian Coros
- Jitendra Malik
- Toru Lin
topics:
- sim2real
- dexterous-manipulation
- tactile-sensing
- contact-representation
- robot-hands
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Beyond Binary: Sim-to-Real Dexterous Manipulation with Physics-Grounded Contact Representation

## Summary
CoP is a tactile contact representation for zero-shot sim-to-real dexterous manipulation. It turns dense taxel readings into a compact contact force and contact location so policies can use touch without training on real task data.

## Problem
- Contact-rich dexterous manipulation needs tactile feedback, but real robot data is expensive to collect.
- Raw tactile signals are hard to simulate and align with hardware, while binary contact signals drop force and location information needed for precise control.
- The paper targets blind manipulation tasks where vision gives little help: peg-in-hole insertion and ball balancing on a 16-DOF Allegro hand with XELA uSkin sensors.

## Approach
- The method uses Center-of-Pressure (CoP): a 3D contact force vector plus a 3D contact position for each tactile sensing region.
- Raw taxel forces are mapped to CoP with a differentiable stress-distribution model that accounts for force spread through the compliant sensor surface.
- The inverse mapping estimates CoP force by solving a regularized least-squares problem over active taxels.
- Taxel orientations are calibrated without ground-truth force labels by matching tactile-inferred external wrench to measured joint torques under static equilibrium.
- Policies are trained in IsaacLab with asymmetric actor-critic PPO, recurrent networks, domain randomization, actuator system identification, and measured tactile sensor delay.

## Results
- On real peg-in-hole insertion, CoP reached 0.78 overall success across six shapes, compared with 0.67 for force-vector-only, 0.55 for force magnitude, 0.53 for binary contact, 0.50 for contact-position-only, 0.48 for raw taxels, and 0.43 for proprioception-only.
- Under out-of-distribution initialization in peg-in-hole, CoP reached 0.63 success, compared with 0.42 for force-vector-only, 0.28 for position-only, 0.27 for raw taxels, 0.27 for magnitude, 0.20 for binary contact, and 0.17 for proprioception-only.
- In masked peg-in-hole trials, CoP reached 0.62 success, compared with 0.57 for force-vector-only, 0.52 for binary contact, 0.48 for magnitude, 0.48 for position-only, and 0.30 for raw taxels.
- By shape, CoP success was 1.0 circle, 0.6 diamond, 0.6 ellipse, 1.0 hexagon, 0.9 square, and 0.6 triangle, with 10 trials per condition.
- The paper claims zero-shot sim-to-real transfer on both peg-in-hole insertion and ball balancing, and says CoP outperforms binary-contact and raw-taxel baselines on both tasks; the excerpt does not provide ball-balancing numbers.
- The learned CoP-conditioned policy states are reported to encode task-relevant physical properties such as object mass, but the excerpt does not include a numeric mass-estimation result.

## Link
- [https://arxiv.org/abs/2605.28812v1](https://arxiv.org/abs/2605.28812v1)
