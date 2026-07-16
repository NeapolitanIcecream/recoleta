---
kind: ideas
granularity: day
period_start: '2026-06-24T00:00:00'
period_end: '2026-06-25T00:00:00'
run_id: 32cb6a51-fc46-4fa9-a7e2-7c84832cfa5e
status: succeeded
topics:
- robotics
- vision-language-action models
- online adaptation
- reinforcement learning
- world action models
- humanoid locomotion
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action-models
- topic/online-adaptation
- topic/reinforcement-learning
- topic/world-action-models
- topic/humanoid-locomotion
language_code: en
pass_output_id: 311
pass_kind: trend_ideas
upstream_pass_output_id: 310
upstream_pass_kind: trend_synthesis
---

# VLA deployment hardening

## Summary
VLA robot teams now have concrete test targets for failures that appear after lab training: moved cameras, weak demonstrations, and action chunk latency. The most practical changes are small deployment routines around existing policies: a short probing pass before task execution, a critic-calibrated online fine-tuning loop after imitation learning, and a delay-conditioned adapter for asynchronous control.

## Safe pre-task probing for camera and robot setup drift
Manipulation cells using VLA policies can add a short calibration pass before the first task after a camera move, gripper change, or mounting adjustment. The robot samples safe target poses, records start image, action, and end image clips, then prepends those clips as context for the policy during task execution. ICWM reports this pattern with Qwen2.5-VL-3B, FAST action tokenization, action chunks of 5, and 5 context clips in the main setup.

A cheap validation is a cross-view acceptance test: move the camera to held-out angles, run the same tasks with and without probing context, and track success, end-effector offsets, and early gripper closure. ICWM’s LIBERO cross-view result gives a useful target: average out-of-distribution success improved by 13.0 percentage points over Multi-View BC and by 9.5 points over an explicit camera-angle baseline. The ablations make the operational check clear, since removing images dropped average success by 56.4 points and false context performed worse than no context.

### Sources
- [In-Context World Modeling for Robotic Control](../Inbox/2026-06-24--in-context-world-modeling-for-robotic-control.md): Summarizes the ICWM probing routine, deployment failure modes, LIBERO cross-view gains, latency, and ablation results.
- [In-Context World Modeling for Robotic Control](../Inbox/2026-06-24--in-context-world-modeling-for-robotic-control.md): Describes task-agnostic random movements as context for implicit system identification across simulation and real robots.

## Critic-calibrated online fine-tuning after behavior cloning
Teams with imitation-trained VLA policies can test an online fine-tuning job that starts with critic calibration before actor updates. FORCE uses offline Cal-QL on demonstrations, mixes a small on-policy rollout batch into a warm-up stage, then keeps separate expert and rollout buffers during online training. Its self-distillation step samples candidate actions, scores them with the critic, and trains toward actions above a state-level mean Q baseline.

This is a concrete fit for repeated station tasks where the robot already has demonstrations but stalls on inconsistent actions or slow completions. FORCE reports 82.3% average success on six ManiSkill tasks with an Octo backbone and 98.3% average success on six real Franka tasks after online fine-tuning, up from 45.0% behavior cloning. A small pilot should compare success rate, execution steps, and early training drops against the current behavior-cloned policy, with conservative rollout limits and stop conditions.

### Sources
- [FORCE: Efficient VLA Reinforcement Fine-Tuning via Value-Calibrated Warm-up and Self-Distillation](../Inbox/2026-06-24--force-efficient-vla-reinforcement-fine-tuning-via-value-calibrated-warm-up-and-self-distillation.md): Gives the FORCE training stages, the critic warm-up mechanism, buffer design, self-distillation method, and reported ManiSkill and Franka results.
- [FORCE: Efficient VLA Reinforcement Fine-Tuning via Value-Calibrated Warm-up and Self-Distillation](../Inbox/2026-06-24--force-efficient-vla-reinforcement-fine-tuning-via-value-calibrated-warm-up-and-self-distillation.md): Describes the initial unlearning and low-quality exploration problems that motivate critic calibration before online actor updates.

## Delay-conditioned action adapter for asynchronous chunked VLA control
Robots running chunked VLA policies can test a small adapter that conditions the next action chunk on the motion already executed while inference was running. ACNet encodes the executed suffix of the previous chunk, pads it to the action horizon, and injects it as a residual into a mostly frozen action head. The perception-language backbone stays frozen, which keeps the change focused on the handoff between chunks.

This is most relevant for contact-rich or precision tasks where asynchronous execution removes idle waiting but creates action jumps at chunk boundaries. ACNet reports 0.79 average success on delayed Kinetix settings, compared with 0.61 for Naïve Async, and matches full delay-conditioned retraining at 0.74 average success on Meta-World MT50 while training about 20% of parameters on Kinetix. A deployment test should log handoff discontinuities, task success, control frequency, and contact failures before committing to full policy retraining.

### Sources
- [Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models](../Inbox/2026-06-24--action-controlnet-a-lightweight-delay-aware-adapter-for-smooth-asynchronous-control-in-vision-language-action-models.md): Summarizes the ACNet adapter design, asynchronous control failure mode, parameter-efficiency claim, and Kinetix, Meta-World, and real SO-ARM101 results.
- [Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models](../Inbox/2026-06-24--action-controlnet-a-lightweight-delay-aware-adapter-for-smooth-asynchronous-control-in-vision-language-action-models.md): Explains how stale observations during overlapped inference cause discontinuities, jitter, and failures at action chunk boundaries.
