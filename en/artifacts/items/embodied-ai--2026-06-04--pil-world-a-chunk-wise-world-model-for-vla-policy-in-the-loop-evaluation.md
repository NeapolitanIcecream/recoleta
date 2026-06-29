---
source: arxiv
url: https://arxiv.org/abs/2606.05773v1
published_at: '2026-06-04T06:57:25'
authors:
- Chong Ma
- Taiyi Su
- Jian Zhu
- Jianjun Zhang
- Zitai Huang
- Yi Xu
- Hanli Wang
topics:
- vision-language-action
- world-model
- policy-in-the-loop
- robot-evaluation
- dual-arm-manipulation
- closed-loop-rollout
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# PiL-World: A Chunk-Wise World Model for VLA Policy-in-the-Loop Evaluation

## Summary
PiL-World evaluates VLA policies with closed-loop imagined rollouts instead of running every action chunk on a real robot. It predicts the next multi-view observations from each VLA action chunk, feeds the final generated observation back into the policy, and better matches real robot success rates than Ctrl-World.

## Problem
- VLA policies run in a feedback loop: observe the scene, execute an action chunk, then choose the next action from the new observation. Many robot world models only predict along fixed, pre-collected action trajectories.
- Real robot evaluation is slow and costly because it needs safe hardware execution, scene resets, and repeated trials.
- A poor imagined observation can change the next policy action, so closed-loop evaluation needs process-consistent multi-view rollouts, not only plausible short videos.

## Approach
- PiL-World alternates a frozen VLA policy with a world model: the policy predicts an action chunk, and the world model predicts the next observation segment.
- It converts absolute dual-arm joint commands into head-view gripper-marker control frames using kinematics and camera projection.
- It generates synchronized multi-view future observations using the current frame, task instruction, visual control, and latent history memory from recent multi-view frames.
- Each prediction step generates K=15 future frames with stride Δ=3; the terminal generated observation becomes the next policy input.
- Training uses Wan2.1-14B initialization, pretraining on RealSource World with over 14 million frames from 11,428 episodes across 35 tasks, then LoRA fine-tuning on successful and failed target-task trajectories.

## Results
- On three real dual-arm manipulation tasks, PiL-World reduces the average real-imagined success-rate gap from 63.2% with Ctrl-World to 12.0%.
- For the 40k-step VLA checkpoint, Sort Cubes real success is 83.3%; PiL-World estimates 68.3% with a 15.0-point gap, while Ctrl-World estimates 11.5% with a 71.8-point gap.
- For Stack Bowls, real success is 96.7%; PiL-World estimates 92.5% with a 4.2-point gap, while Ctrl-World estimates 24.1% with a 72.6-point gap.
- For Stack Blocks, real success is 50.0%; PiL-World estimates 33.3% with a 16.7-point gap, while Ctrl-World estimates 4.9% with a 45.1-point gap.
- Average hallucination-free ratio rises from 41.5% with Ctrl-World to 70.1% with PiL-World.
- PiL-World reports Pearson correlation 0.94 between real and imagined success rates across task-checkpoint settings, and lowers overall LPIPS versus Ctrl-World on Sort Cubes from 0.1454 to 0.0965, Stack Bowls from 0.1366 to 0.1100, and Stack Blocks from 0.1277 to 0.1208.

## Link
- [https://arxiv.org/abs/2606.05773v1](https://arxiv.org/abs/2606.05773v1)
