---
source: arxiv
url: https://arxiv.org/abs/2606.29892v1
published_at: '2026-06-29T07:31:41'
authors:
- Siyao Chen
- Jiakang Yuan
- Jiaxin Wang
- Tao Chen
topics:
- vision-language-action
- test-time-rl
- self-rewarding
- robot-manipulation
- policy-optimization
- confidence-estimation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Trust Your Instincts: Confidence-Driven Test-Time RL for Vision-Language-Action Models

## Summary
T2VLA trains VLA policies at test time using the model's own confidence as the reward source, so RL updates do not need environment success labels. It reports higher success rates on LIBERO for OpenVLA-OFT, π0, and π0.5, with the largest average gain on π0.

## Problem
- Existing RL methods for VLA models usually need external rewards, such as simulator success flags, human labels, or auxiliary model scores.
- Robot trajectories are hard to self-check because many different action sequences can complete the same task, so majority-vote verification from math or code tasks does not transfer cleanly.
- The problem matters because reward labeling limits test-time improvement on new robot tasks and adds cost to robot data scaling.

## Approach
- The method scores each rollout with model-internal confidence: mean action log-probability for discrete-action VLAs and denoising transition log-likelihood for flow-based continuous-action VLAs.
- For each language instruction, it picks the highest-confidence rollout in the current batch as a local pseudo-expert.
- It keeps a task-conditioned global expert pool with the top K historical local experts, with K=5 in the implementation.
- It turns expert matching into a reward by computing Dynamic Time Warping similarity between a rollout and the local expert plus the best matching global expert.
- It updates the policy with GRPO using the self reward and a KL penalty against the initial SFT policy.

## Results
- The paper reports a confidence-success correlation analysis on 2,000 OpenVLA-OFT rollouts on LIBERO, where higher mean log-probability tracks higher execution success.
- On LIBERO, OpenVLA-OFT rises from 91.0% average success to 97.2% with T2VLA, a +6.2 point gain. Suite gains are +6.1 Spatial, +4.3 Object, +5.5 Goal, and +8.8 Long.
- On LIBERO, π0 rises from 57.7% average success to 81.9%, a +24.2 point gain. Suite gains are +21.0 Spatial, +26.6 Object, +32.2 Goal, and +16.8 Long.
- On LIBERO, π0.5 rises from 77.1% average success to 85.1%, a +8.0 point gain. Suite gains are +10.3 Spatial, +3.0 Object, +7.2 Goal, and +11.2 Long.
- The OpenVLA-OFT result, 97.2% average success, is below SimpleVLA-RL with environment success rewards at 99.1%, but above the OpenVLA-OFT SFT baseline at 91.0% and above EVOLVE-VLA at 95.8% on the reported LIBERO table.
- The abstract also claims gains above 20 absolute points on continuous-action and bimanual tasks, and says the method applies to both OpenVLA-OFT and the π series.

## Link
- [https://arxiv.org/abs/2606.29892v1](https://arxiv.org/abs/2606.29892v1)
