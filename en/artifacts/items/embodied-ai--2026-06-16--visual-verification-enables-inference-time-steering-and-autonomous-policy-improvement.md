---
source: arxiv
url: https://arxiv.org/abs/2606.18247v1
published_at: '2026-06-16T17:59:04'
authors:
- Mingtong Zhang
- Dhruv Shah
topics:
- vision-language-action
- robot-policy-steering
- robot-self-improvement
- visual-verification
- robot-data-scaling
- manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Visual Verification Enables Inference-time Steering and Autonomous Policy Improvement

## Summary
VERITAS lets a robot policy sample several short action chunks, visually score them before execution, and then train later on successful verified rollouts. The paper claims higher success rates at test time and policy gains without new human demonstrations.

## Problem
- Robot foundation policies depend on expensive human demonstrations, so improving them after deployment is slow and costly.
- A deployed robot needs a way to choose safer, task-aligned actions at run time and turn its own successful trials into training data.

## Approach
- A pretrained stochastic robot policy, such as π0-Bridge, π0-DROID, or π0.5-DROID, generates N candidate action chunks for the current image and language instruction.
- A visual verifier scores each chunk, and the robot executes the highest-scoring candidate.
- In the main verifier, a VLM creates pixel-space waypoints once from the initial image and instruction; candidate end-effector motions are projected into the image and scored by distance to that trace.
- Successful verified rollouts are logged and used for behavior-cloning fine-tuning of the original policy.

## Results
- Across 3 policies and 1160 evaluation episodes, inference-time verification improved success rates by 12.6% on average in simulation and 35% in real-world deployment, with no policy fine-tuning.
- In simulation, VERITAS was tested on 4 manipulation tasks with π0-Bridge, averaged over 10 trials per task variation, and all verifier variants beat the base policy; the paper says they also outperformed V-GPS on average.
- In real-world DROID experiments, the paper evaluated 2 tasks per policy with 50 rollouts per task and reports gains across π0-DROID and π0.5-DROID.
- Offline fine-tuning on verified self-generated trajectories improved simulation performance by 10% on average over the base policy.
- The paper claims post-training on verified rollouts matched the efficiency of human expert demonstrations in the real world, with as few as 20 verified trajectories shifting behavior after 20,000 fine-tuning steps.
- Runtime settings include N = 5 sampled chunks, 15 Hz control, and less than 1 ms geometric verification overhead after the one-time VLM trace generation.

## Link
- [https://arxiv.org/abs/2606.18247v1](https://arxiv.org/abs/2606.18247v1)
