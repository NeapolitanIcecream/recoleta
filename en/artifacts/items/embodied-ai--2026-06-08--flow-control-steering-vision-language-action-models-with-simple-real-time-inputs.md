---
source: arxiv
url: https://arxiv.org/abs/2606.10180v1
published_at: '2026-06-08T21:16:37'
authors:
- Jonathan C. Kao
- Jason Chan
- Andy Wang
topics:
- vision-language-action
- robot-policy-steering
- flow-matching
- shared-autonomy
- robot-data-scaling
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Flow Control: Steering Vision-Language-Action Models with Simple Real-Time Inputs

## Summary
Flow Control steers a frozen flow-matching VLA by replacing the action sampler’s initial condition with a simple user command, such as a keyboard direction. The paper claims this lets users guide \(\pi_{0.5}\)-DROID in real time while the model still maps the crude command into actions shaped by its learned action distribution.

## Problem
- VLAs can fail on language following, novel objects, novel scenes, and out-of-distribution states, so users need a low-latency way to correct robot behavior during execution.
- Existing steering methods use mid-episode language, sketches, goal images, or extra trained interfaces; these signals can be too coarse, too high-bandwidth, or require new data and fine-tuning.
- The problem matters because a small user input should help a high-DOF robot act safely and usefully without asking the user to teleoperate every joint.

## Approach
- The method targets VLAs with flow-matching action heads, especially \(\pi_{0.5}\)-DROID, whose action expert integrates a deterministic ODE over 10 Euler steps with \(\Delta t=0.1\).
- A keyboard command gives one of six Cartesian directions: up, down, left, right, forward, or backward.
- The system converts that direction into end-effector velocity, uses inverse kinematics to compute joint velocities, normalizes them, and writes them into the initial condition of the flow model for the first \(\tau\) action steps.
- The flow head then transforms the user-provided initial condition into an action chunk under the VLA’s learned action distribution, conditioned on cameras, language, and robot state.
- The paper’s mechanism relies on a key property of flow matching: the deterministic ODE preserves information about the initial condition, unlike diffusion sampling with injected noise at each step.

## Results
- In the Two-Block task, \(\pi_{0.5}\)-DROID picked the right block 85% of the time under the ambiguous instruction “put the block in the hole”; setting the joint-1 initial condition toward the left block made left-block acquisition reach nearly 100% when \(\tau=6\) or \(\tau=8\).
- In that same Two-Block setup, the blocks were 2 cm wide and spaced 10 cm from the hole; the paper reports pick and place success stayed near 100% even while the steering input was applied throughout the episode.
- The VLA action chunk has 16 time steps, with 8 executed in the environment; each action is 8-dimensional, covering 7 Franka Panda joint angles plus gripper width.
- The user study used 16 participants. Each performed 10 Flow Control trials for Marker-in-Bowl and 10 for Cup-Stacking, plus 10 teleoperation trials for each task, with up to 5 practice trials.
- The excerpt claims Flow Control increased user-steered task success and completion speed, and that fine-tuning on Flow Control trajectories improved autonomous policy performance, but it does not provide the exact success-rate or timing values for those claims.

## Link
- [https://arxiv.org/abs/2606.10180v1](https://arxiv.org/abs/2606.10180v1)
