---
kind: ideas
granularity: day
period_start: '2026-05-05T00:00:00'
period_end: '2026-05-06T00:00:00'
run_id: 3890871b-3905-41fd-851e-00cfbe491f9e
status: succeeded
topics:
- robotics
- VLA
- world models
- spatial reasoning
- benchmarks
- multimodal models
tags:
- recoleta/ideas
- topic/robotics
- topic/vla
- topic/world-models
- topic/spatial-reasoning
- topic/benchmarks
- topic/multimodal-models
language_code: en
pass_output_id: 133
pass_kind: trend_ideas
upstream_pass_output_id: 132
upstream_pass_kind: trend_synthesis
---

# Robot Policy Evaluation Gates

## Summary
Robotics teams can turn the new evaluation pressure into three concrete changes: release gates for VLA policies that test memory and contact, behavior-level rewards for robot video prediction, and a shared action-input harness for interactive world-model comparisons.

## Memory and contact tests for dexterous VLA release gates
Robot teams deploying VLA policies on hands, arms, or humanoid platforms should add release tests that isolate three failure modes: tracking moving objects, remembering earlier interactions, and sensing contact under occlusion. A compact bench can include a conveyor catch, an object-in-box selection task, and insertion or deformable grasping with tactile or joint-torque logs. Pass criteria should include task success, contact-event timing, memory-dependent choice accuracy, and per-step latency on the target GPU.

RLDX-1 gives a concrete template. The policy adds multi-frame motion processing, a memory module storing past cognition-feature chunks, and tactile or torque inputs in a separate physics stream. Its reported gains are largest on tasks where a current-image policy is likely to fail, including 91.7% success on ALLEX Object-in-Box Selection and over 87.5% on conveyor-belt fast-object catching. The report also treats inference speed as a deployment metric, cutting per-step latency on an RTX 5090 from 71.2 ms to 43.7 ms.

### Evidence
- [RLDX-1 Technical Report](../Inbox/2026-05-05--rldx-1-technical-report.md): Summarizes RLDX-1’s motion, memory, tactile/torque inputs, task results, and latency improvement.
- [RLDX-1 Technical Report](../Inbox/2026-05-05--rldx-1-technical-report.md): Describes why dynamic manipulation, physical sensing, and memory create failures for existing VLAs.

## Behavior-scored reward models for robot video prediction
Teams using robot video world models for planning should add a behavior-scored reward model to their training and evaluation loop. The useful check is simple: score generated rollouts for instruction following, manipulation success, action-outcome consistency, temporal consistency, contact realism, and physics adherence, then compare those scores against pixel metrics and downstream plan quality. A small distilled reward model is more practical for repeated training runs than an 8B judge.

RoboAlign-R1 shows the shape of the workflow. The authors fine-tune Qwen3-VL-8B-Thinking into a six-dimension judge, distill it into a 98M reward model, and use it for GRPO post-training. The same paper adds Sliding Window Re-encoding for long rollouts by decoding the last predicted frame, re-encoding it as fresh context, and continuing generation with a shorter active history. The reported result is higher RobotWorldBench score than iVideoGPT, better scores on all six behavior dimensions, and improved long-horizon pixel metrics with about 1% added latency.

### Evidence
- [RoboAlign-R1: Distilled Multimodal Reward Alignment for Robot Video World Models](../Inbox/2026-05-05--roboalign-r1-distilled-multimodal-reward-alignment-for-robot-video-world-models.md): Summarizes the six-dimension judge, 98M reward model, GRPO post-training, Sliding Window Re-encoding, and reported metrics.
- [RoboAlign-R1: Distilled Multimodal Reward Alignment for Robot Video World Models](../Inbox/2026-05-05--roboalign-r1-distilled-multimodal-reward-alignment-for-robot-video-world-models.md): Explains why robot video world models need action-conditioned dynamics, contacts, scene evolution, and physical plausibility for control.

## Shared action-input harness for interactive world-model comparisons
World-model teams comparing text-controlled, keyboard-like, and camera-parameter models should build a shared action-input harness before running leaderboards. The harness should map each evaluation action into text commands, one-hot controls, and camera intrinsic or extrinsic parameters, then run the same tasks for action response, trajectory following, memory, and camera following. This reduces ambiguity when one model accepts “move forward” and another expects low-level control IDs or camera poses.

iWorld-Bench supplies a ready specification for that harness. It defines 27 translational and 27 rotational action IDs, focuses evaluation on 81 common combined actions, and builds 4,900 test tasks across action-control difficulty, memory, and camera following. The paper also reports broad coverage across four viewpoints, nine outdoor weather types, five indoor lighting types, and 18 simulator environments, which is useful for finding models that pass a narrow scene test but fail under changed viewpoint or conditions.

### Evidence
- [iWorld-Bench: A Benchmark for Interactive World Models with a Unified Action Generation Framework](../Inbox/2026-05-05--iworld-bench-a-benchmark-for-interactive-world-models-with-a-unified-action-generation-framework.md): Summarizes iWorld-Bench’s action mapping, task types, dataset size, and coverage.
- [iWorld-Bench: A Benchmark for Interactive World Models with a Unified Action Generation Framework](../Inbox/2026-05-05--iworld-bench-a-benchmark-for-interactive-world-models-with-a-unified-action-generation-framework.md): Describes the lack of aligned action definitions across text, keyboard, and trajectory or camera-control inputs.
