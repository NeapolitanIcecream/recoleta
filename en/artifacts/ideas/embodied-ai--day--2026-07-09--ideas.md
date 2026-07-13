---
kind: ideas
granularity: day
period_start: '2026-07-09T00:00:00'
period_end: '2026-07-10T00:00:00'
run_id: 3b516604-d66c-48bc-a1fa-bf9b2dc5385f
status: succeeded
topics:
- robot manipulation
- vision-language-action models
- policy adaptation
- temporal memory
- dexterous benchmarks
tags:
- recoleta/ideas
- topic/robot-manipulation
- topic/vision-language-action-models
- topic/policy-adaptation
- topic/temporal-memory
- topic/dexterous-benchmarks
language_code: en
pass_output_id: 345
pass_kind: trend_ideas
upstream_pass_output_id: 344
upstream_pass_kind: trend_synthesis
---

# Reliable Robot Policy Deployment

## Summary
Frozen robot policies can gain useful reliability through planner-controlled retries, event-sensitive task memory, and small adaptation modules trained from operator corrections. Deployment teams should also add dexterous contact tasks to acceptance testing, because high scores on standard manipulation suites leave force regulation and fine alignment largely untested.

## Planner-controlled retries and task-state memory for frozen VLA policies
Robot teams can wrap a frozen VLA with a planner that assigns free-space motion, grounding, staging, and release to analytic primitives, then invokes the VLA for short contact-rich actions. Each invocation should record the subgoal, elapsed time, contact or gripper event, observed outcome, and retry count. The planner can use this episode state to re-stage after an empty grasp, repeat a local action, or advance to the next subgoal.

Harness VLA reached 82.4% success on LIBERO-Pro, compared with 50.0% for direct use of the same frozen baseline. TFP provides complementary evidence for storing progress inside the policy: its event-sensitive memory raised real-robot object-swap success from 3/20 to 15/20. A focused pilot can use one multi-stage task with object-position changes and intermittent occlusion, then compare direct execution with the wrapper on completion rate, unnecessary repeated actions, recovery rate, and added latency.

### Evidence
- [Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents](../Inbox/2026-07-09--harness-vla-steering-frozen-vlas-into-reliable-manipulation-primitives-via-memory-guided-agents.md): Documents the fixed primitive library, retryable VLA calls, task memory, and the LIBERO-Pro improvement over direct frozen-policy execution.
- [TFP: Temporally Conditioned Memory-Fusion Policies for Visuomotor Learning](../Inbox/2026-07-09--tfp-temporally-conditioned-memory-fusion-policies-for-visuomotor-learning.md): Documents continuous-time task-progress memory and the real-robot gains on object swapping and counting pick-and-place.

## Latent-space adaptation from sparse operator corrections
Operators correcting a generative robot policy can supply training data for a small observation-to-noise adapter while the base flow-matching or diffusion policy remains frozen. The adaptation pipeline should capture the observation and corrective action at each intervention, invert the action into a latent noise target, and mix those targets with successful autonomous rollouts during training. This confines updates to a compact module and gives deployment teams a practical way to address a recurring object, dynamics, or embodiment failure.

FlowDAgger improved mean success across 12 MetaWorld tasks from 0.53 to 0.78 after 50 rollouts and trained its small noise policy in about 8 GB of VRAM. Its Hammer test also exposes the required safety check: adapted-task success rose from 0.40 to 0.84, while performance across five held-out tasks declined from 0.96 to 0.88. An initial deployment test should therefore pair one known failure case with a held-out skill suite and reject updates that cross a preset regression limit.

### Evidence
- [FlowDAgger: Human-in-the-Loop Adaptation of Generative Robot Policies in Latent Space](../Inbox/2026-07-09--flowdagger-human-in-the-loop-adaptation-of-generative-robot-policies-in-latent-space.md): Provides the action-inversion method, 50-rollout results, compute requirement, and held-out skill regression measurements.
- [FlowDAgger: Human-in-the-Loop Adaptation of Generative Robot Policies in Latent Space](../Inbox/2026-07-09--flowdagger-human-in-the-loop-adaptation-of-generative-robot-policies-in-latent-space.md): Explains how corrective actions are mapped into latent noise vectors for a small policy without changing base-policy weights.

## Dexterous contact tasks in robot policy acceptance testing
Robot policy evaluations should include insertion, pushing, tool sliding, articulated-object opening, and multi-stage hand use under controlled changes to camera pose, lighting, object pose, and dynamics. Report results by interaction type and embodiment, with separate measures for contact acquisition, force regulation, sub-centimeter alignment, and full-task completion. This test structure can reveal deployment blockers hidden by a single average from gripper-based suites.

DexVerse evaluated four representative policies on the same 19-task, 950-episode subset. The best mean success was 0.34, shared by 3D Diffusion Policy and pi0.5; every method scored zero on PushT, while InsertPen, SlideUtilityKnife, and OpenLaptop stayed at or near zero. A practical first pass can reproduce this 19-task subset for the target policy and require nonzero success on each critical interaction class before a hardware trial.

### Evidence
- [DexVerse: A Modular Benchmark for Multi-Task, Multi-Embodiment Dexterous Manipulation](../Inbox/2026-07-09--dexverse-a-modular-benchmark-for-multi-task-multi-embodiment-dexterous-manipulation.md): Reports the common 19-task evaluation, the 0.34 best mean success, and near-zero results on force- and alignment-sensitive tasks.
- [DexVerse: A Modular Benchmark for Multi-Task, Multi-Embodiment Dexterous Manipulation](../Inbox/2026-07-09--dexverse-a-modular-benchmark-for-multi-task-multi-embodiment-dexterous-manipulation.md): Describes the benchmark's task coverage, embodiments, synchronized observations, and demonstration set.
