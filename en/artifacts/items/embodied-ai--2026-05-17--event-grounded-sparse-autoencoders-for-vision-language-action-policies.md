---
source: arxiv
url: https://arxiv.org/abs/2605.17204v1
published_at: '2026-05-17T00:20:17'
authors:
- Xinchen Jin
- Aditya Chatterjee
- Pranav Kumar
- Rohan Paleja
topics:
- vision-language-action
- mechanistic-interpretability
- sparse-autoencoders
- robot-policy
- closed-loop-evaluation
- libero
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Event-Grounded Sparse Autoencoders for Vision-Language-Action Policies

## Summary
The paper proposes an event-grounded SAE pipeline for interpreting Vision-Language-Action policies by tying SAE features to recurring robot events and testing them with closed-loop interventions.

## Problem
- VLA hidden states drive robot actions, so unclear internal features can lead to different trajectories, contacts, or failures.
- LLM and VLM interpretability tools do not transfer cleanly because VLA outputs are actions, not readable tokens.
- Causal validation is costly because feature edits must be judged through closed-loop robot rollouts.

## Approach
- Train BatchTopK sparse autoencoders on per-token residual-stream activations from closed-loop rollouts.
- Use Automatic Waypoint Extraction on end-effector trajectories to find keyframes that act as behavior anchors.
- Cluster keyframes within each task using visual embeddings, robot state, and temporal progress; optional VLM labels give short semantic names to clusters.
- Rank SAE features by event-aligned temporal templates, event-window means, task means, and a random-alive control.
- Test selected features with residual-preserving latent edits that scale chosen SAE latents while keeping SAE reconstruction error in the hidden state.

## Results
- On OpenVLA over LIBERO, raw success rate was 68.0±14.3%; SAE reconstruction hooks failed at layers 0 and 16 with 0.0% Hooked SR, reached 0.2±0.5% at layer 24, and reached 34.8±24.5% at layer 31.
- On π_0.5, reconstruction hooks preserved behavior: PaliGemma backbone Hooked SR stayed between 95.8% and 97.8%, and the action expert stayed between 95.8% and 97.2%.
- Keyframe extraction found about 3.86 to 6.91 keyframes per rollout. Recurring event clusters ranged from 35 to 61 per suite after a 50% episode-coverage filter.
- OpenVLA layer 31 single-feature zero-out showed the strongest causal effect for event-aligned ranking: baseline SR 70.0%, event-aligned SR 48.8% (-21.2 points), window-mean 63.8% (-6.2), task-mean 63.5% (-6.5), random-alive 68.7% (-1.3).
- π_0.5 PaliGemma backbone edits had small effects: the largest listed drop was -2.8 points at layer 11 for task-mean features, compared with -1.0 for random-alive at that layer.
- π_0.5 action expert edits were unstable: zeroing top ranked features often drove SR to 0.0% to 0.8%, while random-alive features caused smaller but nonzero drops at deeper layers, such as -23.4 points at layer 5 and -8.1 at layer 11.

## Link
- [https://arxiv.org/abs/2605.17204v1](https://arxiv.org/abs/2605.17204v1)
