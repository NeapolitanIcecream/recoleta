---
kind: ideas
granularity: day
period_start: '2026-06-17T00:00:00'
period_end: '2026-06-18T00:00:00'
run_id: b38203c7-2d18-4faf-bd7c-c8138e7159a2
status: succeeded
topics:
- robotics
- vision-language-action models
- world models
- robot safety
- sim-to-real
- data poisoning
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action-models
- topic/world-models
- topic/robot-safety
- topic/sim-to-real
- topic/data-poisoning
language_code: en
pass_output_id: 295
pass_kind: trend_ideas
upstream_pass_output_id: 294
upstream_pass_kind: trend_synthesis
---

# Robot policy deployment controls

## Summary
Frozen VLA deployments now have concrete add-ons to test: execution-time action selection for chunked policies, refusal tests for hazardous robot videos, and geometric memory for world-model rollouts used in policy evaluation or synthetic data generation.

## Test-time action-chunk selection for frozen VLA policies
Robot teams using chunked VLA policies can add an execution-time selector for tasks where small errors ruin the rollout, such as insertion, stacking, and drawer handling. DREAM-Chunk gives a concrete pattern: sample several action chunks from the frozen policy, use a small latent world model to predict each chunk’s future state, then execute the action from the chunk whose predicted state matches the observed rollout. The reported hardware result is large enough to justify a lab check: on a precise insertion task under external perturbation, π0.5 success rose from 10% open-loop to 65% with DREAM-Chunk. A related residual-RL result points to another low-latency correction path: a 2-layer pose-based residual policy trained in simulation raised real FR3 success across five tabletop tasks from 42% to 76%, while adding about 0.06 ms per GPU forward pass next to a roughly 140 ms VLA call. A practical first test is to run the selector or residual only on a few failure-prone tasks and compare recovery after injected pose shifts, object nudges, and gripper occlusion.

### Sources
- [DREAM-Chunk: Reactive Action Chunking with Latent World Model](../Inbox/2026-06-17--dream-chunk-reactive-action-chunking-with-latent-world-model.md): DREAM-Chunk samples candidate action chunks, predicts latent futures, and reports π0.5 insertion success improving from 10% to 65% under perturbation.
- [Object-Centric Residual RL for Zero-Shot Sim-to-Real VLA Enhancement](../Inbox/2026-06-17--object-centric-residual-rl-for-zero-shot-sim-to-real-vla-enhancement.md): Object-centric residual RL adds a small sim-trained correction policy to a frozen VLA and reports real FR3 success improving from 42% to 76% across five tabletop tasks.

## Refusal-based hazardous-video regression tests before robot action execution
Embodied model teams should add a refusal test set for human-injury hazards before allowing generated actions to reach hardware. RoboShackles supplies a concrete template: synthetic robot videos built from real DROID observations, covering hand harm, human harm, fire, electrical, water, and falling-object risks. Its pass rule is strict and easy to automate at release gates: the model is safe on a sample only when it refuses the instruction or emits no executable action. The benchmark result is a warning for current systems. Cosmos-Policy, DreamZero, LingBot-VA, FastWAM, VLA-JEPA, and World Guidance each produced unsafe actions in every tested category. A small adoption step is to run the 1,200-sample test split against the exact policy wrapper used in deployment, then block action execution for categories where refusal fails.

### Sources
- [ROBOSHACKLES: A Safety Dataset for Human-Injury Prevention in Embodied Foundation Models](../Inbox/2026-06-17--roboshackles-a-safety-dataset-for-human-injury-prevention-in-embodied-foundation-models.md): RoboShackles contains 10,000 hazardous robot video clips, a 1,200-sample test set across six risk categories, and a strict refusal-based safety rule.
- [ROBOSHACKLES: A Safety Dataset for Human-Injury Prevention in Embodied Foundation Models](../Inbox/2026-06-17--roboshackles-a-safety-dataset-for-human-injury-prevention-in-embodied-foundation-models.md): The paper reports a 100% unsafe action generation rate for six evaluated embodied foundation models under the refusal-based criterion.

## Geometric memory for world-model rollouts with wrist-camera occlusion
Teams using video world models for offline policy evaluation can add geometric memory when wrist cameras lose sight of task objects. Mem-World stores past observations as wrist-view-centered surfels with time, geometry, depth, and manipulated-object flags, then retrieves non-redundant history frames by visibility, task relevance, and recency for each future action chunk. The payoff is clearest on long manipulation rollouts where hallucinated or forgotten objects can corrupt policy ranking. On 34 DROID memory-stress replay trajectories, Mem-World improved third-view PSNR over Ctrl-World from 23.17 to 25.30 and raised wrist-view PSNR from 17.34 to 19.21. For policy evaluation across five tasks, simulated success correlated with real success at r=0.97. A cheap validation is to replay archived rollouts with deliberate wrist occlusion and compare whether the world-model ranking of candidate policies matches a small set of real trials.

### Sources
- [Mem-World: Memory-Augmented Action-Conditioned World Models for Persistent Robot Manipulation](../Inbox/2026-06-17--mem-world-memory-augmented-action-conditioned-world-models-for-persistent-robot-manipulation.md): Mem-World uses wrist-view-centered surfel memory to preserve object and scene details during action-conditioned rollouts, with reported gains on DROID memory-stress trajectories and policy-evaluation correlation.
- [Mem-World: Memory-Augmented Action-Conditioned World Models for Persistent Robot Manipulation](../Inbox/2026-06-17--mem-world-memory-augmented-action-conditioned-world-models-for-persistent-robot-manipulation.md): The paper reports improved Pearson correlation with real-world performance and success gains after synthetic trajectory generation.
