---
source: arxiv
url: https://arxiv.org/abs/2606.18953v1
published_at: '2026-06-17T11:36:54'
authors:
- Kinam Kim
- Namiko Saito
- Heecheol Kim
- Katsushi Ikeuchi
- Jaegul Choo
- Yasuyuki Matsushita
topics:
- vision-language-action
- residual-rl
- sim2real
- robot-manipulation
- object-pose
- vla-self-improvement
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Object-Centric Residual RL for Zero-Shot Sim-to-Real VLA Enhancement

## Summary
This paper adds a pose-based residual RL policy to a frozen VLA so a sim-trained correction can run on a real FR3 robot with no real-world RL. On five tabletop tasks, it raises real-robot success from 42% to 76% on average.

## Problem
- Imitation-trained VLAs can fail in precise manipulation because small action errors accumulate over a rollout.
- Prior residual RL options have deployment costs: privileged simulator state needs distillation, image observations suffer a visual sim-to-real gap, and real-world RL is costly and risky.
- The problem matters because better recovery can improve deployed robot policies without collecting more teleoperation data or running RL on hardware.

## Approach
- The method trains paired sim and real VLAs by replaying the same teleoperation actions in MuJoCo and on the real setup, using 30 demonstrations per task for GR00T-N1.5 fine-tuning.
- A frozen sim VLA supplies base actions during residual RL training; the frozen real VLA supplies base actions at deployment.
- The residual policy is a 2-layer MLP trained with TD3 in simulation. Its input is 6-DoF task-object poses, robot proprioception, and the current base VLA action.
- The residual output is composed with the base action: position and gripper commands are added, and rotations use quaternion multiplication.
- Training injects pose noise and sometimes drops the object-pose vector to zero, so the policy can handle pose-estimator error or tracking loss from FoundationPose plus SAM2.

## Results
- Real FR3 average success improves from 8.4/20 trials to 15.2/20 trials, or 42% to 76%, across five tasks with zero-shot sim-to-real transfer.
- Per-task real success improves on all tasks: Cube Lift 7/20 to 17/20, Pick-and-Place 9/20 to 16/20, Stack Cube 7/20 to 15/20, Close Drawer 14/20 to 20/20, and Stand Cup Up 5/20 to 8/20.
- Simulation average success improves from 7.6/20 ± 1.7 to 17.2/20 ± 0.9 over 3 seeds.
- Ablations show the full pose-based residual beats image-based and distillation-based residuals on the real robot; for example, Pick-and-Place reaches 16/20 versus 10/20 for image-based and 4/20 for distillation-based.
- Removing pose dropout lowers real success across tasks, with Stack Cube falling from 15/20 to 10/20 and Close Drawer from 20/20 to 16/20.
- The residual actor adds little compute: about 0.06 ms per GPU forward pass, less than 0.05% of the VLA's roughly 140 ms inference time; FoundationPose tracking runs at about 18 ms per frame asynchronously.

## Link
- [https://arxiv.org/abs/2606.18953v1](https://arxiv.org/abs/2606.18953v1)
