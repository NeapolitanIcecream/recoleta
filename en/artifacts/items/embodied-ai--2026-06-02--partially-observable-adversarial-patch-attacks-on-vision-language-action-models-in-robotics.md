---
source: arxiv
url: https://arxiv.org/abs/2606.03556v1
published_at: '2026-06-02T12:19:28'
authors:
- Xiaofei Wang
- Mingliang Han
- Tianyu Hao
- Yi Yang
- Yun-Bo Zhao
- Keke Tang
topics:
- vision-language-action
- adversarial-patch
- robot-security
- partial-observability
- openvla
- libero
relevance_score: 0.83
run_id: materialize-outputs
language_code: en
---

# Partially Observable Adversarial Patch Attacks on Vision-Language-Action Models in Robotics

## Summary
This paper shows that a static adversarial patch can disrupt robotic vision-language-action policies even when the attacker only sees the first part of a rollout. The attack targets both object grounding and action smoothness, then carries the same patch into the unseen future of the task.

## Problem
- Prior VLA patch attacks assume the attacker can optimize on the full robot trajectory, which gives the attacker information that a real deployment would rarely expose.
- The paper studies a stricter threat model: the attacker observes only the first K frames, then must place one fixed patch for the rest of the execution.
- This matters because a short-observation physical patch can cause long-horizon failures in VLA-controlled robots without changing model weights, commands, or the controller.

## Approach
- The attacker uses the VLA model in a gray-box setting, with query access and model-side signals needed for patch optimization, but no access to model parameters or direct robot control.
- Patch placement uses cross-modal attention from the last prefix frame. The method finds the image region with the highest instruction-related attention and restricts the patch to that region.
- Patch content is optimized with two losses: one shifts attention-derived grounding for task nouns, and one pushes predicted actions toward directions that increase end-effector trajectory curvature.
- The patch is learned only on the observed prefix of length K, then applied unchanged to later frames.
- Default settings include K=40, a 3x3 token patch equal to 42x42 pixels, 50 SGD iterations, 100 sampled target directions, and loss weights lambda_sem=1.0 and lambda_traj=12.0.

## Results
- On LIBERO with OpenVLA victims, the method reports the best ASR in almost all listed settings across Spatial, Object, Goal, and Long suites, compared with UADA, UPA, and TMA.
- At K=30, ASR is 73.8% on Spatial, 90.7% on Object, 72.8% on Goal, and 86.6% on Long. The best baseline ASRs in those same columns are 59.1%, 63.8%, 59.5%, and 57.2%.
- At K=40, ASR is 72.4% on Spatial, 89.7% on Object, 71.7% on Goal, and 89.1% on Long. The best baseline ASRs are 52.6%, 61.9%, 59.4%, and 59.1%.
- For nASR at K=30, the method scores 87.5% on Spatial, 96.0% on Object, 79.6% on Goal, and 93.9% on Long. The best baseline nASRs are 77.7%, 82.3%, 74.4%, and 84.9%.
- Attention localization helps: averaged over four LIBERO suites, last-frame localization gets 81.0% ASR and 89.3% nASR at K=30, compared with 77.7% ASR and 86.6% nASR for prefix-mean localization.
- The excerpt says the attack was tested in simulation and on real robots, but it provides quantitative tables only for LIBERO results in the shown text.

## Link
- [https://arxiv.org/abs/2606.03556v1](https://arxiv.org/abs/2606.03556v1)
