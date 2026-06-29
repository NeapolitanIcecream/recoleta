---
source: arxiv
url: https://arxiv.org/abs/2606.12403v1
published_at: '2026-06-10T17:59:08'
authors:
- Zefu Lin
- Rongxu Cui
- Junjia Xu
- Xiaojuan Jin
- Wenling Li
- Lue Fan
- Zhaoxiang Zhang
topics:
- vision-language-action
- world-action-models
- generalist-robot-policy
- robot-manipulation
- ood-generalization
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# World Pilot: Steering Vision-Language-Action Models with World-Action Priors

## Summary
World Pilot adds a frozen World-Action Model to a Vision-Language-Action policy so the policy receives both language grounding and predicted scene dynamics. It targets OOD robot manipulation where static image-text pretraining leaves VLA action heads without contact and motion cues.

## Problem
- Current VLAs encode images and instructions well, but their pretraining comes from static image-text pairs, so the action generator lacks a direct model of how objects move, collide, deform, or change under robot actions.
- This matters because manipulation policies often fail when camera pose, object geometry, lighting, layout, deformable state, or contact tolerance shifts away from training data.
- The paper asks how to add world-model signals to a VLA without forcing the policy to depend on noisy generated pixels or inaccurate step-by-step action guesses.

## Approach
- World Pilot keeps a World-Action Model frozen and uses it as a prior source. In the reported setup, ABot-M0 is the VLA base, Qwen3-VL is the VLM backbone, and Cosmos Policy is the WAM.
- Latent Steering takes the WAM scene-evolution latent, projects it into the VLA hidden-state space, adds a future-scene tag, and injects it into VLM hidden states through residual cross-attention.
- Action Steering takes the WAM anticipated action trajectory, resamples it to the VLA horizon, encodes it into one prefix token, and feeds that token to the flow-matching action generator.
- The WAM outputs can be cached during training; at inference the WAM runs online at each decision step. Gradients update the VLA, action head, and fusion modules, not the WAM.

## Results
- On LIBERO-Plus zero-shot OOD, World Pilot reports 84.7% Total success, compared with Being-H0.7 at 82.1%, ABot-M0 at 80.5%, and Cosmos Policy at 79.7%.
- On LIBERO-Plus axes, it leads on Camera at 82.8% versus Cosmos Policy at 69.6%, Light at 98.6% versus Cosmos Policy at 97.7%, Background at 96.4% versus ABot-M0 and RIPT-VLA at 91.6%, and Noise at 93.6% versus Cosmos Policy at 87.3%.
- On RoboCasa, World Pilot reports 65.5% success. This is below Cosmos Policy at 67.1%, but above Being-H0.7 at 62.1% and ABot-M0 at 54.0%.
- In real-robot tests across 4 tasks, 12 settings, 100 demonstrations per task, and 20 trials per setting, World Pilot has the highest success rate in every table cell. Examples include Fold Towel ID at 85% versus the best baseline at 55%, Fruit-to-Plate ID at 90% versus 70%, and Container-Lid Alignment lid-pose OOD at 65% versus 15%.
- Real-robot OOD drops for World Pilot stay within 20 absolute points from the matching ID setting, while the listed baselines drop by 25 to 50 points.
- Ablations on LIBERO-Plus show Latent Steering alone at 83.7%, Action Steering alone at 83.1%, and both together at 84.7%, compared with the ABot-M0 baseline at 80.5%.

## Link
- [https://arxiv.org/abs/2606.12403v1](https://arxiv.org/abs/2606.12403v1)
