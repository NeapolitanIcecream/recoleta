---
kind: ideas
granularity: day
period_start: '2026-06-08T00:00:00'
period_end: '2026-06-09T00:00:00'
run_id: 2cda84c4-86c2-42b4-9d6b-c62cdec04806
status: succeeded
topics:
- robot learning
- vision-language-action models
- world models
- failure recovery
- humanoid control
- robot data collection
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-models
- topic/world-models
- topic/failure-recovery
- topic/humanoid-control
- topic/robot-data-collection
language_code: en
pass_output_id: 269
pass_kind: trend_ideas
upstream_pass_output_id: 268
upstream_pass_kind: trend_synthesis
---

# Practical VLA Deployment Controls

## Summary
Robot teams can make concrete changes around frozen VLA policies: add failure-specific recovery layers, expose low-latency steering and safety filters during execution, and collect bimanual data with lighter handheld grippers. The common adoption pressure is practical deployment friction: a policy can know the task and still miss a grasp, collide with nearby objects, or lack enough varied demonstrations for contact-rich work.

## Failure-specific recovery wrappers for frozen VLA manipulation policies
A useful next build is a recovery layer that sits around an existing VLA policy and handles common off-trajectory states such as empty grasps, dropped objects, wrong placements, and unfinished contact steps. The base policy can stay fixed while the recovery system detects the failure type, selects a corrective target or residual action, and returns control once the task is back on track.

ReCoVLA shows one heavier version of this pattern: Qwen3-VL-8B-Instruct classifies the failure and recovery stage, a compiler creates stage-gated rewards, and residual policies are trained in simulation. It reports Fetch-task simulation success rising from 36.7% to 66.7%, with 61.7% average success in zero-shot physical tests. B2FF shows a lighter route for foresight-driven VLAs by pre-generating 12 future-image milestones and selecting one after a perturbation; on failure-injected LIBERO, UD-VLA average success rises from 56.3% to 74.0%. ProbeAct gives a runtime-only option using hidden-state probes, a kinematic failure detector, and Control Barrier Function zones after repeated failures, raising LIBERO-plus success from 69.6% to 74.1%.

A robotics group could start by replaying its own failed manipulation logs into a small taxonomy of grasp, transport, placement, and articulation failures. The first test should compare the frozen policy against a wrapper on injected failures and on a small physical rerun set, measuring task success, recovery success, and extra steps per recovery.

### Sources
- [ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies](../Inbox/2026-06-08--recovla-vlm-guided-reward-compilation-for-failure-recovery-in-vision-language-action-policies.md): ReCoVLA keeps the base VLA frozen, classifies failure state, compiles stage-gated rewards, and reports simulation and physical recovery gains.
- [Back to the Familiar Future: Failure Recovery for VLA Policies via Pre-Imagined Milestone Selection](../Inbox/2026-06-08--back-to-the-familiar-future-failure-recovery-for-vla-policies-via-pre-imagined-milestone-selection.md): B2FF selects pre-generated future-image milestones for recovery and reports a 56.3% to 74.0% gain on failure-injected LIBERO.
- [ProbeAct: Probe-Guided Training-Free Failure Recovery in Vision-Language-Action Models](../Inbox/2026-06-08--probeact-probe-guided-training-free-failure-recovery-in-vision-language-action-models.md): ProbeAct uses hidden-state probes, kinematic failure detection, and CBF zones to improve LIBERO-plus success for a frozen VLA.

## Per-step steering and collision filtering inside the VLA control loop
VLA deployment needs control-loop hooks for people and safety logic because a high-level language command often leaves ambiguity during execution. Two practical additions are now worth testing together: a simple directional input for a human supervisor, and a per-step safety filter that reads the model’s own target signal before projecting unsafe actions away from obstacles.

Flow Control applies the human input side to flow-matching VLAs. A keyboard command gives one of six Cartesian directions, the system converts it to joint-velocity initialization, and the flow head maps that crude signal into an action chunk. In the Two-Block task, pi_0.5-DROID chose the right block 85% of the time under an ambiguous instruction, while steering toward the left block made left-block acquisition nearly perfect at longer steering horizons, with pick-and-place success reported near 100% in that setup. The attention-guided safety filter paper handles the safety side by reading selected attention heads inside a frozen VLA, assigning the active target online, and using a CBF-QP filter to keep the end effector away from other objects. On dynamic SafeLIBERO Level III, collision rate falls from 70.75% for an init-only filter to 26.88%, and safe-success rises from 25.5% to 55.75%.

The adoption test is direct: run ambiguous two-object tasks and moving-obstacle tasks with the same frozen policy, then compare no wrapper, steering only, safety filtering only, and both together. The key measurements are correction latency, collision rate, safe-success, and how often the wrapper changes a successful baseline action.

### Sources
- [Flow Control: Steering Vision-Language-Action Models with Simple Real-Time Inputs](../Inbox/2026-06-08--flow-control-steering-vision-language-action-models-with-simple-real-time-inputs.md): Flow Control describes keyboard-direction steering by modifying the initial condition of a flow-matching VLA action sampler and reports Two-Block steering results.
- [Your Model Already Knows: Attention-Guided Safety Filter for Vision-Language-Action Models](../Inbox/2026-06-08--your-model-already-knows-attention-guided-safety-filter-for-vision-language-action-models.md): The attention-guided safety filter reads VLA attention online, applies a CBF-QP filter, and reports large collision-rate and safe-success gains on dynamic SafeLIBERO.

## Finger-aligned handheld grippers for higher-throughput bimanual data collection
Open robot-learning labs that rely on UMI-style collection can test a hardware change before buying more robots: move data collection to a lighter finger-aligned handheld gripper with fixed-rig VR tracking and a standard export path such as LeRobot. The operational target is longer collection sessions with better fine manipulation and less operator fatigue.

YUBI replaces the pistol grip with a pinch-aligned design where the thumb drives one jaw and the index and middle fingers drive the other. The gripper weighs 319 g including the VR controller, compared with 780 g for original UMI and at least 905 g for VR-integrated pistol-grip systems, and the paper says each unit can be built for under $200 excluding the Quest 3S tracking setup. The reported collection scale is 8,434 hours, 1.20 million episodes, 6.80 million video-language-action triplets, 119 tasks, 179 operators, and 22 desks over two months. A single pi_0.5-based policy trained on YUBI wrist data transfers across UR, Franka, and Toyota ELEY arms when the same YUBI end effector is used.

A cheap validation is a side-by-side operator study before a full collection run: ten novice operators, repeated small-object pickup trials, an hour-long fatigue check, and throughput measured as usable episodes per operator-hour. If the lighter gripper improves small-object control and session length, the next build is a fixed-desk collection rig with synchronized wrist cameras, top-view RGB-D, 6-DoF gripper poses, jaw angles, task text, and sub-action labels.

### Sources
- [YUBI: Yielding Universal Bidigital Interface for Bimanual Dexterous Manipulation at Scale](../Inbox/2026-06-08--yubi-yielding-universal-bidigital-interface-for-bimanual-dexterous-manipulation-at-scale.md): YUBI reports the finger-aligned gripper design, weight and cost comparisons, dataset scale, LeRobot conversion, and cross-arm policy transfer results.
