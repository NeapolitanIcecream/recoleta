---
source: arxiv
url: https://arxiv.org/abs/2606.25215v1
published_at: '2026-06-23T22:23:35'
authors:
- Qing Lian
- Kent Yu
- Lei Zhang
topics:
- vision-language-action
- robot-foundation-model
- in-context-learning
- action-consequences
- robot-generalization
- manipulation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Reflective VLA: In-Context Action Consequences Make VLAs Generalize

## Summary
Reflective VLA adds past observation-action-consequence triplets to a vision-language-action policy so the robot can infer camera, calibration, and actuation effects during deployment. The paper reports higher success under LIBERO distribution shifts without test-time fine-tuning, while keeping strong standard benchmark performance.

## Problem
- Reactive VLAs predict the next action from the current instruction and observation, so one frame may not identify camera-to-robot geometry, robot calibration error, or actuation bias.
- These hidden embodiment factors matter because the same command can produce different visible motion in a new setup, which hurts deployment generalization.
- Plain temporal history can track task progress, but it may not bind an executed action to the scene change that followed it.

## Approach
- The model keeps a rolling context of triplets `(O_i, A_i, O'_i)`, where `O_i` is the pre-action observation, `A_i` is the executed action chunk, and `O'_i` is the observation after the full chunk horizon `C`.
- Previous action chunks are embedded as 8 tokens in the VLM token space, alongside third-person images, wrist images, proprioception, language, and time tokens.
- A continuous flow-matching action expert attends to the full shared VLM prompt and the current observation before predicting the next action chunk.
- A block-causal mask trains all `K` sampled frames in one forward pass while blocking access to each target's own future action and consequence.
- At inference, the system stores the policy's own executed chunks and observed outcomes, then reuses cached VLM keys and values for past triplets.

## Results
- On standard LIBERO, Reflective VLA reaches 97.6% average success, compared with 96.9% for the matched reactive `pi_0.5` baseline, a +0.7 point gain.
- On SimplerEnv-Bridge, it reaches 78.2% average success, compared with 72.9% for the matched reactive baseline, a +5.3 point gain.
- On LIBERO-Plus, it reaches 87.7% average success, compared with 82.3% for the matched reactive baseline, a +5.4 point gain. The largest listed gain is on the Robot shift: 72.9% vs 50.0%, or +22.9 points.
- On LIBERO-Plus-Hard, it reaches 68.8% average success, compared with 64.6% for the matched reactive baseline, a +4.2 point gain. Camera† is 76.3% vs 74.0%, and Robot Calibration† is 61.3% vs 55.2%.
- The context ablation on Camera, Camera†, and Robot Calibration† gives 77.8% average for full `(O,A,O')` context, compared with 73.1% reactive, 72.3% for `O` only, and 73.8% for `(O,A)`.
- The context-length ablation with full triplets improves average success from 73.1% at `K=1` to 75.3% at `K=2`, 76.7% at `K=4`, and 77.8% at `K=8`.

## Link
- [https://arxiv.org/abs/2606.25215v1](https://arxiv.org/abs/2606.25215v1)
