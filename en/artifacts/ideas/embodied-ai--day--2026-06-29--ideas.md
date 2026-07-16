---
kind: ideas
granularity: day
period_start: '2026-06-29T00:00:00'
period_end: '2026-06-30T00:00:00'
run_id: 63bd1f61-2d69-4692-971b-fb90cd4e0810
status: succeeded
topics:
- robot learning
- vision-language-action models
- manipulation
- test-time RL
- tactile sensing
- navigation
- autonomous driving
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-models
- topic/manipulation
- topic/test-time-rl
- topic/tactile-sensing
- topic/navigation
- topic/autonomous-driving
language_code: en
pass_output_id: 323
pass_kind: trend_ideas
upstream_pass_output_id: 322
upstream_pass_kind: trend_synthesis
---

# Robot manipulation rollout checks

## Summary
Robot policy teams can get more value from the current work by adding execution-facing checks around evaluation, deployment, and geometry. The practical thread is clear: rank model variants on task-critical motion segments, verify the perception-action loop before closed-loop trials, and store object-relative poses for contact phases where small errors break the task.

## Critical-interval validation before robot rollouts
Manipulation teams should add a validation pass that scores policy errors only during grasp, contact, insertion, fine alignment, and similar task-critical segments. Critical Interval MSE shows a concrete recipe: label the critical timesteps, apply the same action execution procedure used at rollout time, align predicted and expert action sequences with local dynamic time warping, and compare model variants on that filtered error.

This is useful for teams training many nearby checkpoints where physical rollouts are too slow or too variable to run for every change. On LBM-Eval, CI-MSE reached Spearman ρ = -0.87 against rollout success, compared with -0.61 for raw MSE. The cheap adoption test is to take a past set of checkpoints with known rollout outcomes, annotate the contact-heavy intervals in held-out demonstrations, and check whether the new ranking matches the hardware ranking better than raw validation loss.

### Sources
- [Critical Interval MSE: Toward Reliable Offline Validation for Robot Manipulation Policies](../Inbox/2026-06-29--critical-interval-mse-toward-reliable-offline-validation-for-robot-manipulation-policies.md): Defines CI-MSE, its critical-interval scoring and rollout-time alignment steps, and reports stronger correlation with rollout success than raw MSE.

## VLA deployment preflight checks for action semantics, frames, and timing
Teams moving OpenVLA-style policies onto a local arm should run a deployment preflight before treating model quality as the main failure source. The UR5e case study points to a concrete checklist: action units and gripper semantics, coordinate-frame conventions, camera preprocessing, modality timing, inference rate, dataset coverage, and the control interface used to execute action chunks.

The same study reports original OpenVLA inference at about 3 Hz on an A100 and unstable closed-loop behavior when integration details were misaligned. A useful preflight is a logged open-loop replay on the robot client: feed recorded camera observations through the server, decode actions, transform them through the intended frames, and compare timing and end-effector motion against the demonstration before enabling autonomous execution.

### Sources
- [Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform](../Inbox/2026-06-29--vision-language-action-models-experimental-insights-from-a-real-world-ur5-platform.md): Reports the UR5e OpenVLA deployment pipeline, about 3 Hz inference on an A100, and failures linked to action semantics, frames, timing, preprocessing, and data coverage.

## Object-relative key-pose memory for tabletop manipulation
For repeated tabletop tasks, a small object-relative key-pose library is a practical way to make demonstrations reusable across scenes. OpenSPM stores phase poses such as approach, grasp, lift, pre-place, and release as SE(3) transforms between the end effector and an object frame. At inference time, the system estimates the current 6D object pose, transfers the stored relative poses, checks feasibility, and generates short action chunks between them.

This is a good fit for teams whose failures cluster around grasp alignment, placement accuracy, or collisions after a semantic planner has chosen the right object. OpenSPM reports 85.6% success on 10 LIBERO-GOAL tasks, 4.8 ms action-chunk generation latency, and a 0.24M-parameter action model. A low-cost check is to extract object-relative poses from a few successful demonstrations for one pick-place family, replay them under changed object positions, and measure pose error near grasp and placement.

### Sources
- [OpenSPM: An Environment-Transferable Robotic Key Spatial Pose Memory and Closed-Loop High-Frequency Flow-Matching Action Generation Model](../Inbox/2026-06-29--openspm-an-environment-transferable-robotic-key-spatial-pose-memory-and-closed-loop-high-frequency-flow-matching-action-generation-model.md): Describes storing object-relative SE(3) key poses from demonstrations, transferring them with 6D object pose estimates, and reports LIBERO-GOAL success and latency results.
