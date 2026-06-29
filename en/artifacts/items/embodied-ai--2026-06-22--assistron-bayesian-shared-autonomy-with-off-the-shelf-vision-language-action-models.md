---
source: arxiv
url: https://arxiv.org/abs/2606.23147v1
published_at: '2026-06-22T10:47:12'
authors:
- Pinhao Song
- Ze Fu
- Yutong Hu
- Renaud Detry
topics:
- vision-language-action
- shared-autonomy
- assistive-robotics
- flow-matching
- human-in-the-loop
- manipulation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Assistron: Bayesian Shared Autonomy with Off-the-shelf Vision-Language-Action Models

## Summary
Assistron is a shared-autonomy system that keeps a VLA policy frozen and asks the user for joystick help near contact-rich steps. It raises task success in a long-horizon assistive manipulation benchmark while cutting active user control time compared with direct teleoperation.

## Problem
- Assistive robots need to handle varied home tasks, but task-specific controllers cover only narrow skills such as grasping, insertion, or pouring.
- Frozen VLAs can interpret language and handle macro-reaching, yet they often fail at grasping, insertion, and release because of spatial and contact precision errors. The excerpt cites RoboArena success rates of 46.95% for pi_0.5 and 35.25% for pi_0.
- Retraining or fine-tuning a VLA can require large robot datasets and can narrow the policy, so the paper targets assistive control without changing VLA weights.

## Approach
- Assistron uses pi_0.5 as a frozen flow-matching VLA. Whisper transcribes user speech into natural-language prompts for the VLA.
- The system switches between autonomous VLA control and shared control through a binary intervention signal.
- A ResNet-18 detector reads 224x224 wrist-camera images and predicts interaction confidence. It triggers intervention only when confidence passes a threshold and the VLA predicts a gripper-state change; the user can also trigger intervention with joystick input.
- During intervention, the joystick command is treated as a Gaussian measurement. A guidance term is added inside the VLA flow-matching denoising process so sampled actions follow the user command while staying near the VLA action distribution.
- The user handles fine contact steps such as grasping or releasing, then control returns to the VLA for macro movement.

## Results
- In a scene-recovery benchmark with 17 novice users, 5 subtasks, and a 7-minute timeout, Assistron reached 91.3% partial success. Direct joystick reached 96.3%, while the autonomous VLA reached 13.7% and consistently timed out.
- Completion time was 324.5 seconds for Assistron and 305.9 seconds for Direct joystick. Assistron needed active user input for 56.5% of the run, split into 41.7% joystick and 14.8% voice, and ran autonomously for 43.5%.
- User ratings favored Assistron over Direct joystick on Quick, Easy to Use, Low Workload, and Reuse (p<0.05), while Direct joystick scored higher on Wanted and Trust (p<0.05). NASA-TLX mental and physical effort were lower for Assistron than Direct joystick (p<0.001).
- Less proficient joystick users benefited more: completion-time improvement correlated with baseline Direct joystick performance at r=0.762, p=0.001. Frustration reduction also correlated with weaker baseline performance at r=-0.564, p=0.023.
- In the grape-into-drawer ablation, posterior blending reduced completion time against Direct teleoperation (p<0.05) and shortened trajectory length against both Direct and Linear blending (p<0.05). The excerpt does not give exact time or length values.
- The interaction detector was trained on more than 12,000 wrist-camera frames and reached 81.2% test accuracy and 84.5% average precision.

## Link
- [https://arxiv.org/abs/2606.23147v1](https://arxiv.org/abs/2606.23147v1)
