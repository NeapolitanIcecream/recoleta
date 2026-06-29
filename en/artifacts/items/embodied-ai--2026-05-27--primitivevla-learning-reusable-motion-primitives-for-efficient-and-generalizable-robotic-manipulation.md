---
source: arxiv
url: https://arxiv.org/abs/2605.28634v1
published_at: '2026-05-27T15:41:18'
authors:
- Yutai Li
- Shaohui Peng
- Jiaming Guo
- Di Huang
- Zihao Zhang
- Yuxuan Guo
- Yunkai Gao
- Siming Lan
- Ling Li
- Xing Hu
- Yunji Chen
topics:
- vision-language-action
- robot-foundation-model
- motion-primitives
- generalist-robot-policy
- robot-data-scaling
- robot-manipulation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# PrimitiveVLA: Learning Reusable Motion Primitives for Efficient and Generalizable Robotic Manipulation

## Summary
PrimitiveVLA fine-tunes VLA robot policies on reusable motion primitives cut from whole task demonstrations. The paper claims better data efficiency and stronger zero-shot transfer on LIBERO through training-time segmentation and test-time primitive sequencing.

## Problem
- Standard VLA fine-tuning maps a full language instruction directly to low-level robot actions, which encourages memorization of task-specific trajectories and visual cues.
- This matters because each new object-skill pair or long-horizon task can require more robot demonstrations, which slows robot data scaling.
- Public robot datasets usually provide task-level instructions only, so primitive labels and segment boundaries are missing.

## Approach
- The method defines 11 primitives: Grasp, Place, Lift, Move, Push, Pull, Insert, Press, Twist, Tilt, and Rotate.
- During fine-tuning, a VLM infers the primitive sequence from the task instruction, RGB trajectory, and primitive library.
- An LLM writes Python rules over robot state to detect primitive boundaries, such as gripper closure followed by upward motion for Grasp.
- The VLA is trained with canonical primitive instructions and object-centric masks tracked with SAM and Cutie, so different tasks share the same primitive input format.
- During inference, the system retrieves the top-3 similar task-sequence examples, uses a VLM to plan primitives, and uses LLM-generated switch code over a sliding state history while the VLA outputs continuous actions.

## Results
- On LIBERO-90, OpenVLA + PrimitiveVLA reaches 79.80% success versus 70.60% for OpenVLA, a +9.20 point gain.
- On LIBERO-90-Novel, OpenVLA rises from 7.38% to 45.50%, about a 6.2x gain on unseen tasks.
- OpenVLA-OFT + PrimitiveVLA reaches 71.00% on LIBERO-90-Novel versus 13.50%, and 66.50% on LIBERO-Long versus 3.75%.
- pi0.5 + PrimitiveVLA reaches 75.50% on LIBERO-90-Novel versus 56.00%, and 80.25% on LIBERO-Long versus 30.50%.
- Small-scale LIBERO mean improves from 82.40% to 88.00% for OpenVLA and from 97.60% to 98.53% for OpenVLA-OFT; pi0.5 changes from 97.53% to 97.33%.
- The excerpt says simulation uses 50 trials and real-world/RLBench use 20 trials, but it does not include the real-world or RLBench result tables.

## Link
- [https://arxiv.org/abs/2605.28634v1](https://arxiv.org/abs/2605.28634v1)
