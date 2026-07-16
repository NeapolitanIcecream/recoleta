---
kind: trend
trend_doc_id: 566
granularity: day
period_start: '2026-06-08T00:00:00'
period_end: '2026-06-09T00:00:00'
topics:
- robot learning
- vision-language-action models
- world models
- failure recovery
- humanoid control
- robot data collection
run_id: materialize-outputs
aliases:
- recoleta-trend-566
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/world-models
- topic/failure-recovery
- topic/humanoid-control
- topic/robot-data-collection
language_code: en
pass_output_id: 268
pass_kind: trend_synthesis
---

# Robot papers are concentrating on temporal memory, recovery, and usable control loops

## Overview
Vision-language-action (VLA) robot work is strongest where policies keep temporal state, recover after mistakes, or accept low-latency human input. MemoryVLA++, MotionWAM, and YUBI show the day’s emphasis: make policies act over longer horizons, collect bigger real data, and keep corrections close to execution.

## Findings

### Temporal memory and world models for robot policies
Several papers treat time as a first-class input to robot control. MemoryVLA++ stores past perceptual and task tokens, then combines them with latent future prediction before action generation. Its reported gains are largest on tasks that need remembering a prior interaction or anticipating motion, including +26 and +28 percentage points on real-robot memory- and imagination-dependent task groups.

iMaC uses robot kinematics and contact heatmaps to make action-conditioned video rollouts more spatially precise. Its world-model estimates correlate with real policy success on six of eight long-horizon real-robot tasks. Echo-Memory adds a useful warning: replay metrics alone can miss whether a world model preserves object identity after the camera leaves and returns.

#### Sources
- [MemoryVLA++: Temporal Modeling via Memory and Imagination in Vision-Language-Action Models](../Inbox/2026-06-08--memoryvla-temporal-modeling-via-memory-and-imagination-in-vision-language-action-models.md): MemoryVLA++ summary, method, and reported simulation and real-robot gains.
- [iMaC: Translating Actions into Motion and Contact Images for Embodied World Models](../Inbox/2026-06-08--imac-translating-actions-into-motion-and-contact-images-for-embodied-world-models.md): iMaC action-to-motion/contact conditioning and policy-evaluation correlations.
- [Echo-Memory: A Controlled Study of Memory in Action World Models](../Inbox/2026-06-08--echo-memory-a-controlled-study-of-memory-in-action-world-models.md): Controlled memory study showing replay quality and revisit memory can rank methods differently.

### Failure recovery around frozen VLA policies
Recovery work keeps the base VLA fixed and adds targeted correction at runtime or through residual training. ReCoVLA uses a vision-language model to identify failure type and recovery stage, compiles stage-gated rewards, and trains residual policies in simulation. It raises average Fetch-task simulation success from 36.7% to 66.7%, with zero-shot physical success at 61.7%.

B2FF pre-generates future-image milestones and selects a recovery goal when execution drifts. On failure-injected LIBERO, it improves UD-VLA average success from 56.3% to 74.0%. ProbeAct is lighter weight: it reads hidden-state probes to track objects and uses control-barrier zones after repeated failures, improving LIBERO-plus success from 69.6% to 74.1%.

#### Sources
- [ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies](../Inbox/2026-06-08--recovla-vlm-guided-reward-compilation-for-failure-recovery-in-vision-language-action-policies.md): ReCoVLA frozen-policy residual recovery, reward compilation, and success metrics.
- [Back to the Familiar Future: Failure Recovery for VLA Policies via Pre-Imagined Milestone Selection](../Inbox/2026-06-08--back-to-the-familiar-future-failure-recovery-for-vla-policies-via-pre-imagined-milestone-selection.md): B2FF milestone-selection recovery and LIBERO results.
- [ProbeAct: Probe-Guided Training-Free Failure Recovery in Vision-Language-Action Models](../Inbox/2026-06-08--probeact-probe-guided-training-free-failure-recovery-in-vision-language-action-models.md): ProbeAct runtime probing, control-barrier correction, and LIBERO-plus gains.

### Execution-time steering and safety filters
The execution loop is getting more explicit user and safety channels. Flow Control modifies the initial condition of a flow-matching action sampler with a simple keyboard direction. In the Two-Block task, steering the initial condition made left-block acquisition nearly perfect at longer steering horizons while pick-and-place success stayed near 100% in the reported setup.

A separate safety-filter paper reads attention heads inside a frozen VLA to identify the current target object during control. On dynamic SafeLIBERO Level III, it cuts average collision rate from 70.75% for an init-only filter to 26.88%, and raises safe-success from 25.5% to 55.75%. The common point is practical: small runtime signals can constrain a large policy without retraining it.

#### Sources
- [Flow Control: Steering Vision-Language-Action Models with Simple Real-Time Inputs](../Inbox/2026-06-08--flow-control-steering-vision-language-action-models-with-simple-real-time-inputs.md): Flow Control mechanism and Two-Block steering results.
- [Your Model Already Knows: Attention-Guided Safety Filter for Vision-Language-Action Models](../Inbox/2026-06-08--your-model-already-knows-attention-guided-safety-filter-for-vision-language-action-models.md): Attention-guided safety filter, dynamic SafeLIBERO collision and safe-success results.

### Real-world data and whole-body control are getting concrete scale tests
YUBI attacks the data bottleneck with a lighter finger-aligned gripper and fixed-rig VR tracking. The reported dataset is unusually large for an open UMI-style setup: 8,434 hours, 1.20 million episodes, 6.80 million video-language-action triplets, and 119 tasks collected by 179 operators. A single π0.5-based policy trained on YUBI wrist data transfers across UR, Franka, and Toyota ELEY arms with the same end effector.

MotionWAM extends world-action modeling to Unitree G1 humanoid loco-manipulation. It uses one egocentric camera and unified whole-body motion latents, reaching 76.1% average success across nine real tasks versus 43.9% for the strongest listed baseline. TORL-VLA adds tactile online reinforcement learning for contact-rich tasks, reaching 30/30 cup, 29/30 latch, and 30/30 egg successes in real-robot subtask trials.

#### Sources
- [YUBI: Yielding Universal Bidigital Interface for Bimanual Dexterous Manipulation at Scale](../Inbox/2026-06-08--yubi-yielding-universal-bidigital-interface-for-bimanual-dexterous-manipulation-at-scale.md): YUBI dataset scale, interface design, and cross-robot rollout results.
- [MotionWAM: Towards Foundation World Action Models for Real-Time Humanoid Loco-Manipulation](../Inbox/2026-06-08--motionwam-towards-foundation-world-action-models-for-real-time-humanoid-loco-manipulation.md): MotionWAM whole-body humanoid action design and nine-task real-robot results.
- [TORL-VLA: Tactile Guided Online Reinforcement Learning for Contact-Rich Manipulation](../Inbox/2026-06-08--torl-vla-tactile-guided-online-reinforcement-learning-for-contact-rich-manipulation.md): TORL-VLA tactile online RL design and contact-rich real-robot results.
