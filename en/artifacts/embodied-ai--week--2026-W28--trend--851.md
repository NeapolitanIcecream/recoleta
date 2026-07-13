---
kind: trend
trend_doc_id: 851
granularity: week
period_start: '2026-07-06T00:00:00'
period_end: '2026-07-13T00:00:00'
topics:
- robot manipulation
- vision-language-action models
- task memory
- sample efficiency
- action control
- dexterous benchmarks
run_id: materialize-outputs
aliases:
- recoleta-trend-851
tags:
- recoleta/trend
- topic/robot-manipulation
- topic/vision-language-action-models
- topic/task-memory
- topic/sample-efficiency
- topic/action-control
- topic/dexterous-benchmarks
language_code: en
pass_output_id: 352
pass_kind: trend_synthesis
---

# Robot policy progress depends on memory, reusable failures, and executable action control

## Overview
Robot learning this week concentrates on execution bottlenecks inside vision-language-action (VLA) policies. Task memory supports retries and stage tracking. Failed rollouts and unlabeled video yield more useful supervision. Continuous trajectories and force-aware post-training improve speed and contact safety. DexVerse keeps the gains in perspective: the best tested methods average only 34% success across its 19-task evaluation subset.

## Clusters

### Task memory and future-state reasoning
Policies are being given explicit state about task progress. TFP maintains a continuous-time latent belief and raises LIBERO Long-10 success from 92.4% to 97.0%; on a real object-swap task, success rises from 3/20 to 15/20. Harness VLA places a memory-guided planner around a frozen controller, using stored traces, re-grounding, staging, and retries. It reaches 82.4% on LIBERO-Pro, compared with 50.0% for the direct frozen baseline. LEEVLA adds task-relevant region weighting and latent future-feature prediction during training, reaching 98.2% average success on LIBERO without extra inference-time memory or computation.

#### Evidence
- [TFP: Temporally Conditioned Memory-Fusion Policies for Visuomotor Learning](../Inbox/2026-07-09--tfp-temporally-conditioned-memory-fusion-policies-for-visuomotor-learning.md): Documents TFP's continuous-time task memory and benchmark and real-robot gains.
- [Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents](../Inbox/2026-07-09--harness-vla-steering-frozen-vlas-into-reliable-manipulation-primitives-via-memory-guided-agents.md): Details Harness VLA's planner, memory, retries, and perturbation results.
- [LEEVLA: Seeing What Matters in Latent Environment Evolution for Vision-Language-Action](../Inbox/2026-07-09--leevla-seeing-what-matters-in-latent-environment-evolution-for-vision-language-action.md): Supports latent future-feature prediction and LIBERO results without added inference cost.

### More supervision from scarce experience
Collected experience is being reused more aggressively. Learning from Hindsight relabels failed rollouts with the behavior the robot actually completed. On out-of-distribution LIBERO-Pro tasks, it reaches standard reinforcement-learning performance in about 5 training steps versus nearly 30, and records 56% real-robot success after 160 rollouts versus 22% for the baseline. CD-LAM removes backgrounds, camera motion, and unrelated objects from latent action codes learned from video. It matches its reference with more than 12 times fewer robot-action adaptation updates, making unlabeled video a cleaner source of action supervision.

#### Evidence
- [Learning More from Less: Reinforcement Learning from Hindsight](../Inbox/2026-07-10--learning-more-from-less-reinforcement-learning-from-hindsight.md): Provides the hindsight relabeling mechanism, sample-efficiency result, and physical-robot comparison.
- [Causally Debiased Latent Action Model for Embodied Action Conditioned World Models](../Inbox/2026-07-10--causally-debiased-latent-action-model-for-embodied-action-conditioned-world-models.md): Provides latent-action debiasing methods and adaptation-efficiency measurements.

### Speed, force safety, and harder dexterity tests
Action representations are being evaluated as control interfaces with measurable timing and safety limits. B-spline Policy predicts continuous curves that can run at different speeds; on long-horizon table cleaning, it cuts average completion time from 23.57 to 11.80 seconds while success changes from 13/20 to 14/20. PAC-ACT aligns reinforcement learning with eight-step action chunks and reduces force readings above 60 N by 46 times on its Contour task. DexVerse exposes the remaining ceiling: across 19 tasks, the top mean success rate is 0.34, and all four tested policies score zero on PushT.

#### Evidence
- [B-spline Policy: Accelerating Manipulation Policies via B-spline Action Representations](../Inbox/2026-07-10--b-spline-policy-accelerating-manipulation-policies-via-b-spline-action-representations.md): Reports continuous B-spline actions, completion-time reductions, success rates, and controller limits.
- [PAC-ACT: Post-training Actor-Critic for Action Chunking Transformers](../Inbox/2026-07-10--pac-act-post-training-actor-critic-for-action-chunking-transformers.md): Reports chunk-level post-training and the reduction in unsafe contact-force readings.
- [DexVerse: A Modular Benchmark for Multi-Task, Multi-Embodiment Dexterous Manipulation](../Inbox/2026-07-09--dexverse-a-modular-benchmark-for-multi-task-multi-embodiment-dexterous-manipulation.md): Grounds the dexterity benchmark scope and the 0.34 best mean online success rate.
