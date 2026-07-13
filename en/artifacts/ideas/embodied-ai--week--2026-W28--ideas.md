---
kind: ideas
granularity: week
period_start: '2026-07-06T00:00:00'
period_end: '2026-07-13T00:00:00'
run_id: 019979c4-454c-4a53-b2a2-f92c075d7e44
status: succeeded
topics:
- robot manipulation
- vision-language-action models
- task memory
- sample efficiency
- action control
- dexterous benchmarks
tags:
- recoleta/ideas
- topic/robot-manipulation
- topic/vision-language-action-models
- topic/task-memory
- topic/sample-efficiency
- topic/action-control
- topic/dexterous-benchmarks
language_code: en
pass_output_id: 353
pass_kind: trend_ideas
upstream_pass_output_id: 352
upstream_pass_kind: trend_synthesis
---

# Reliable Robot Manipulation Systems

## Summary
Robot teams can improve deployed manipulation systems by adding task-progress state and retry control around existing policies, recovering supervision from failed rollouts, and testing action representations against completion time, contact force, and controller limits. These changes can be evaluated on small task sets before committing to new data collection or larger policy training runs.

## Task-progress memory and retry control for frozen VLA policies
Teams deploying a pretrained VLA can wrap it in a planner that records completed stages, contact outcomes, and retry history. The VLA handles short contact-rich actions; explicit primitives handle grounding, free-space motion, re-staging, and release. Harness VLA used this structure to raise LIBERO-Pro success from 50.0% for the direct frozen baseline to 82.4% without VLA fine-tuning. TFP also shows that episode-local task state can resolve visually similar scenes that require different actions: real-robot object-swap success increased from 3/20 to 15/20.

A practical trial can start with one multi-stage task that currently fails after an empty grasp, occlusion, or object swap. Log a compact state containing the current stage, elapsed time, last contact result, and retry count. Compare the wrapped policy with the unchanged controller across layout changes, measuring full-task success, repeated-action errors, retries, and added latency. This test will show whether execution state is a cheaper reliability gain than collecting another task-specific fine-tuning set.

### Evidence
- [Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents](../Inbox/2026-07-09--harness-vla-steering-frozen-vlas-into-reliable-manipulation-primitives-via-memory-guided-agents.md): Documents the fixed primitive library, task and global memory, retryable VLA calls, and the LIBERO-Pro comparison.
- [TFP: Temporally Conditioned Memory-Fusion Policies for Visuomotor Learning](../Inbox/2026-07-09--tfp-temporally-conditioned-memory-fusion-policies-for-visuomotor-learning.md): Provides the episode-local continuous-time belief design and real-robot gains on stage-dependent tasks.

## Hindsight relabeling for failed robot rollouts
Robot-learning teams can add a relabeling pass to their post-training pipeline so coherent failures produce usable supervision. A VLM watches a failed rollout, describes the behavior that actually occurred, and scores the rollout against that new instruction. Learning from Hindsight kept roughly 70% to 80% of rollout groups usable, reached standard GRPO performance in about five training steps compared with nearly 30, and achieved 56% real-robot success after 160 rollouts versus 22% for GRPO.

The cheapest check is an offline audit of a recent failed-rollout batch. Sample 100 failures, generate hindsight instructions, and have operators review whether each description is correct, specific, and safe to reinforce. If agreement is high, run a short post-training comparison using the same rollout budget and track usable-group rate, original-task success, and any increase in unintended behaviors. This workflow is most relevant where physical collection time and sparse rewards dominate training cost.

### Evidence
- [Learning More from Less: Reinforcement Learning from Hindsight](../Inbox/2026-07-10--learning-more-from-less-reinforcement-learning-from-hindsight.md): Reports the relabeling procedure, usable rollout rate, training-step reduction, and Franka results.
- [Learning More from Less: Reinforcement Learning from Hindsight](../Inbox/2026-07-10--learning-more-from-less-reinforcement-learning-from-hindsight.md): Explains how coherent behavior in a failed rollout becomes supervision for a different language-conditioned task.

## Action-control tests with completion time, force thresholds, and tracking limits
Policy evaluation for contact-rich manipulation should include execution time, force exceedances, and low-level tracking error alongside task success. B-spline Policy shows that continuous action curves can be retimed and sampled at high control frequency: table-cleaning time fell from 23.57 to 11.80 seconds while success moved from 13/20 to 14/20. Its 4× Speed Stacking result also fell to 0/20, exposing a controller-speed boundary. PAC-ACT reports a 46-fold reduction in force readings above 60 N after chunk-level reinforcement-learning post-training.

A useful test bench can replay the same demonstrations through discrete action chunks and continuous curves at several speed multipliers, then record success, completion time, peak force, time above the force limit, and joint-tracking error. Include at least one precision-contact task and one long-horizon task. DexVerse provides a warning against relying on easy pick-and-place checks: the top mean success across its 19-task subset was 0.34, and every tested policy scored zero on PushT. The resulting speed-force envelope gives deployment engineers an explicit operating limit for each controller and task.

### Evidence
- [B-spline Policy: Accelerating Manipulation Policies via B-spline Action Representations](../Inbox/2026-07-10--b-spline-policy-accelerating-manipulation-policies-via-b-spline-action-representations.md): Reports completion-time gains, success rates, continuous B-spline control, and failure at excessive speed.
- [PAC-ACT: Post-training Actor-Critic for Action Chunking Transformers](../Inbox/2026-07-10--pac-act-post-training-actor-critic-for-action-chunking-transformers.md): Provides the chunk-level post-training method and the reported reduction in force readings above 60 N.
- [DexVerse: A Modular Benchmark for Multi-Task, Multi-Embodiment Dexterous Manipulation](../Inbox/2026-07-09--dexverse-a-modular-benchmark-for-multi-task-multi-embodiment-dexterous-manipulation.md): Shows low aggregate dexterous-manipulation success and zero success on PushT across all evaluated policies.
