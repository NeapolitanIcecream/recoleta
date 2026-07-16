---
kind: ideas
granularity: week
period_start: '2026-05-11T00:00:00'
period_end: '2026-05-18T00:00:00'
run_id: 36b57fae-53b0-4afd-b8fd-803eb83400cb
status: succeeded
topics:
- robotics
- vision-language-action
- world models
- robot manipulation
- embodied AI
- safety evaluation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/robot-manipulation
- topic/embodied-ai
- topic/safety-evaluation
language_code: en
pass_output_id: 163
pass_kind: trend_ideas
upstream_pass_output_id: 162
upstream_pass_kind: trend_synthesis
---

# Rollout-Level Manipulation Evaluation

## Summary
Robot VLA teams can now test progress at the level of rollout behavior: temporal safety monitors for household manipulation, dataloader changes that protect contact and release frames, and small-data adaptation inside task-agnostic world models. Each path gives a concrete way to find failures that final success rates can hide.

## LTL_f monitors for manipulation rollout safety
Task success alone is a weak release gate for household manipulation policies. A deployment evaluation can add LTL_f monitors over rollout traces and report success-and-safe, success-but-unsafe, violation category, and unsafe-state exposure. SafeManip shows why this is needed: on 50 RoboCasa365 tasks, `pi_0.5` raised task success from 8.1% to 9.3% over `pi_0`, while its safety violation rate rose from 69.7% to 82.8%.

A practical first build is a trace logger that records contacts, object poses, gripper state, fixture state, and task events, then binds those signals to task-specific checks such as `Collision`, `StableGrasp`, `Sanitized`, `Contained`, and `FixOpen`. Kitchen and home-robot teams would use the output during model selection and regression testing, especially for contamination, release stability, and access-to-fixture tasks where unsafe behavior can occur before the final state looks correct.

### Sources
- [SafeManip: A Property-Driven Benchmark for Temporal Safety Evaluation in Robotic Manipulation](../Inbox/2026-05-12--safemanip-a-property-driven-benchmark-for-temporal-safety-evaluation-in-robotic-manipulation.md): SafeManip defines LTL_f temporal safety templates, rollout predicate traces, and metrics separating task success from safe execution, with reported pi_0 and pi_0.5 success and violation rates.
- [SafeManip: A Property-Driven Benchmark for Temporal Safety Evaluation in Robotic Manipulation](../Inbox/2026-05-12--safemanip-a-property-driven-benchmark-for-temporal-safety-evaluation-in-robotic-manipulation.md): The source text explains that temporal failures include contaminated contact and early release, and describes task-specific predicate bindings and evaluation metrics.

## Frame selection in VLA training dataloaders for contact-heavy tasks
Robot demonstration datasets need a training-data pass that preserves manipulation-critical frames before another model change is tried. FrameSkip reports that keeping 20% of unique frames, while protecting gripper transitions and high-action-change moments, raises macro-average success across RoboCasa-GR1, SimplerEnv, and LIBERO from 66.50% to 76.15%.

The workflow change is small enough for teams already training Open X-Embodiment-style policies: score frames by action variation, visual-action coherence, task progress, and gripper or end-effector transitions, then mix pruned minibatches with full-frame anchor minibatches after warmup. The first check should be tasks with sparse decisive moments, such as alignment, contact, grasp closure, and release. If success gains appear only on long approach segments, the scoring recipe is probably hiding the real manipulation bottleneck.

### Sources
- [FrameSkip: Learning from Fewer but More Informative Frames in VLA Training](../Inbox/2026-05-13--frameskip-learning-from-fewer-but-more-informative-frames-in-vla-training.md): FrameSkip describes the dense-demonstration imbalance, the dataloader-only frame selection method, protected transition frames, and the 66.50% to 76.15% macro-average gain.
- [FrameSkip: Learning from Fewer but More Informative Frames in VLA Training](../Inbox/2026-05-13--frameskip-learning-from-fewer-but-more-informative-frames-in-vla-training.md): The paper abstract states that FrameSkip operates in the dataloader and targets alignment, contact, grasping, and release frames while leaving the model and inference path unchanged.

## Small-data VLA adaptation inside task-agnostic video world models
New manipulation tasks can be tested with imagined RL before collecting hundreds of target rollouts. RAW-Dream trains OpenVLA-OFT with GRPO inside a task-agnostic action-conditioned video world model and uses Qwen3-VL for binary reward judgments on imagined videos. On LIBERO, it improves a 1-shot SFT baseline from 43.4% to 52.3% using 10 target demonstrations and no target rollouts for world-model training.

The adoption path is a limited adaptation loop for new objects, layouts, or instructions: pretrain the world model on broad play-style robot behavior, anchor the policy with a few demonstrations, run imagined rollouts, and filter unstable wins with dual-noise verification. Teams should compare this against short online RL or fresh world-model tuning on the same task budget. RAW-Dream’s reported in-domain world-model tuning result, 66.0% average success using 510 target data, gives a useful upper reference for deciding when the zero-shot world model is too far from the target scene.

### Sources
- [Reinforcing VLAs in Task-Agnostic World Models](../Inbox/2026-05-12--reinforcing-vlas-in-task-agnostic-world-models.md): RAW-Dream describes task-agnostic world-model RL, Qwen3-VL reward judgments, dual-noise verification, and LIBERO gains with 10 target demonstrations and no target rollouts for world-model training.
- [Reinforcing VLAs in Task-Agnostic World Models](../Inbox/2026-05-12--reinforcing-vlas-in-task-agnostic-world-models.md): The source text states the problem of prior methods requiring target-task rollout data for world and reward models before adaptation.
