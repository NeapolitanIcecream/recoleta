---
source: arxiv
url: https://arxiv.org/abs/2606.06491v1
published_at: '2026-06-04T17:59:40'
authors:
- Dong Jing
- Jingchen Nie
- Tianqi Zhang
- Jiaqi Liu
- Huaxiu Yao
- Zhiwu Lu
- Mingyu Ding
topics:
- vision-language-action
- robot-manipulation
- speed-control
- trajectory-augmentation
- generalist-robot-policy
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# TempoVLA: Learning Speed-Controllable Vision-Language-Action Policies

## Summary
TempoVLA trains one Vision-Language-Action policy to run robot manipulation tasks at commanded speeds instead of a fixed demonstration speed. It does this by re-timing demonstrations and feeding a scalar speed value into the policy.

## Problem
- Existing VLAs inherit one execution speed from teleoperated demonstrations, so the same policy cannot speed up during safe transit and slow down during contact-heavy steps.
- This matters because manipulation needs different speeds within one task: fast free-space motion saves time, while slow insertion, grasping, and handover reduce failure risk.
- Prior acceleration work changes inference speed or produces a faster fixed policy, but the paper targets explicit bidirectional control over robot motion speed.

## Approach
- Variable-Speed Trajectory Augmentation (VSTA) re-times demonstrations online. For speedup, it merges consecutive actions into fewer larger actions; for slowdown, it splits actions into more smaller actions.
- VSTA segments trajectories by motion mode, direction changes, and gripper state changes so that resampling does not blur rotations, translations, or gripper switches.
- The target speed is written as a ratio s = q/p. VSTA maps q source frames into p output frames while preserving the summed motion over each chunk.
- TempoVLA conditions the VLA on speed using one of three light mechanisms: a text prefix, speed-modulated RMSNorm, or soft prompt tokens tied to speed anchors.
- A VLM scheduler can choose speeds at deployment, sending low speeds for risky contact phases and higher speeds for free-space phases.

## Results
- On LIBERO, VSTA replayed re-timed demonstrations close to requested speeds: data ratios were 0.50 at 0.5x, 0.76 at 0.75x, 1.20 at 1.25x, 1.43 at 1.5x, and 1.90 at 2x.
- VSTA preserved integrated motion with very small error: 2.8E-10 at 0.5x, 4.4E-9 at 0.75x, 1.1E-8 at 1.25x, 2.2E-8 at 1.5x, and 4.8E-8 at 2x.
- Re-timed demonstration replay success on LIBERO was 97.6% at 1x, 92.9% at 0.75x, 92.4% at 1.25x, 83.0% at 0.5x, 81.6% at 1.5x, and 67.5% at 2x.
- The three speed-conditioning methods performed similarly on LIBERO: Text averaged 96.8% success, Modulation averaged 96.8%, and Soft Prompt-8 averaged 96.5% over 0.75x, 1x, 1.25x, and 1.5x.
- Variable-speed training improved or preserved default 1x LIBERO success versus the single-speed baseline of 96.7%; the seven-speed policy reached 96.9% at 1x, 97.4% at 1.25x, and 97.3% at 1.5x.
- The policy controlled speed in both directions but under-shot large speedups: in the seven-speed setting, commanded 2x produced a 1.58x model speed ratio while VSTA data reached 1.90x. The excerpt mentions real-world evaluation on five Franka tasks with 50 demonstrations per task and 10 rollouts per speed, but it does not include the real-world success-rate table.

## Link
- [https://arxiv.org/abs/2606.06491v1](https://arxiv.org/abs/2606.06491v1)
