---
source: arxiv
url: https://arxiv.org/abs/2606.26025v1
published_at: '2026-06-24T16:53:36'
authors:
- Siyin Wang
- Junhao Shi
- Senyu Fei
- Zhaoyang Fu
- Li Ji
- Jingjing Gong
- Xipeng Qiu
topics:
- vision-language-action
- world-modeling
- test-time-adaptation
- system-identification
- robot-control
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# In-Context World Modeling for Robotic Control

## Summary
ICWM lets a VLA robot policy adapt to a new camera view or body setup by first making a few safe random movements and using the observed visual changes as context. The paper claims this improves LIBERO and real-robot control under unseen viewpoints with no test-time weight updates or task demonstrations.

## Problem
- Standard VLA policies condition on the current image and language instruction, so camera viewpoint, mounting offset, and robot geometry are baked into training data rather than inferred at deployment.
- When the deployment setup changes, the same image-action mapping can become wrong, causing end-effector offsets, early gripper closure, and task failure.
- This matters because real robots often face camera moves, calibration drift, and tool or gripper changes after training.

## Approach
- The robot runs a short active probing phase before the task: it samples safe target poses, moves there, and records start image, action, and end image clips.
- These task-agnostic interaction clips are prepended to the VLA input as context, so the Transformer can infer the current action-to-observation mapping.
- Training uses the same format: context clips from diverse configurations are placed before the task query, and the model learns next-action prediction with the standard policy loss.
- The method uses Qwen2.5-VL-3B with FAST action tokenization, action chunks of 5, and 5 context clips in the main setup.
- At inference, the context hidden states can be cached because the system configuration stays fixed during a run.

## Results
- On LIBERO cross-view evaluation, training uses 8 azimuth angles and testing includes 6 unseen OOD viewpoints across 500 × 15 × 4 episodes; ICWM improves average OOD success by 13.0 percentage points over Multi-View BC and by 9.5 points over an explicit camera-angle input baseline.
- On LIBERO seen viewpoints, ICWM improves average success by 8.1 percentage points over Multi-View BC.
- On LIBERO-Long, ICWM has the largest reported gains: +29.9 points on seen viewpoints and +26.3 points on unseen viewpoints over Multi-View BC.
- Real-robot tests use a UR5e, 12 cameras split into 6 train and 6 held-out views, 4 tasks, and 600 total trials; the excerpt reports clear gains over Multi-View BC, but the exact average success rates are not readable in the provided figure text.
- Context ablations support the mechanism: removing images drops average success by 56.4 points, false context scores 18.9 versus 22.0 with no context, and a BC model trained without in-context supervision falls below 1% when given prepended interaction tokens.
- Extra stress tests show smaller gains under semantic shifts: distractor objects score 35.0 versus 27.5 for MV, and novel table textures score 41.2 versus 37.5; latency is 0.165 s per step with 3 context clips and 0.185 s with 5 clips on an RTX 4090.

## Link
- [https://arxiv.org/abs/2606.26025v1](https://arxiv.org/abs/2606.26025v1)
