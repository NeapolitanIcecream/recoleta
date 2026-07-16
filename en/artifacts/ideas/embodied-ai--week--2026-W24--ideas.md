---
kind: ideas
granularity: week
period_start: '2026-06-08T00:00:00'
period_end: '2026-06-15T00:00:00'
run_id: c70dbe3b-0537-4f1c-baf5-4b76262753e2
status: succeeded
topics:
- robotics
- vision-language-action models
- manipulation
- real-robot evaluation
- temporal modeling
- contact control
- spatial grounding
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action-models
- topic/manipulation
- topic/real-robot-evaluation
- topic/temporal-modeling
- topic/contact-control
- topic/spatial-grounding
language_code: en
pass_output_id: 289
pass_kind: trend_ideas
upstream_pass_output_id: 288
upstream_pass_kind: trend_synthesis
---

# Robot VLA Evaluation Blind Spots

## Summary
Robot VLA teams can act on three near-term changes: standardize physical rollouts before comparing policies, separate sensor update rates for contact-heavy control, and score demonstration labels with interaction evidence. Each change addresses a failure mode that current aggregate success rates can hide.

## UMI-style real-robot evaluation protocol with reset JSON and progress scoring
Teams comparing wrist-view manipulation policies should add a shared physical evaluation pack before treating model scores as comparable. UMI-Bench 1.0 gives a concrete template: fix the workstation, wrist RGB observation setup, action interface, scene reset, rollout logging, and human scoring. Each episode carries a reset image plus scene JSON with task ID, object metadata, position, pose, target region, split, and task-specific factors.

This is useful for labs that see policy rankings move when camera placement, reset procedure, or object pose changes. UMI-Bench reports Full Success Rate and a 0–100 Progress Score across seen and unseen condition cells. Its results show why the split matters: average Progress Score falls from 59.62 in Seen/Seen episodes to 40.19 under combined shifts, and position, layout, pose, or dynamics shifts hurt more than object or appearance changes. Two long-horizon tasks reach 0% Full Success Rate for all three evaluated models, which gives evaluation teams a clear stress test for policies that look acceptable on shorter tasks.

### Sources
- [UMI-Bench 1.0: An Open and Reproducible Real-World Benchmark for Tabletop Robotic Manipulation with UMI Data](../Inbox/2026-06-09--umi-bench-1-0-an-open-and-reproducible-real-world-benchmark-for-tabletop-robotic-manipulation-with-umi-data.md): Summarizes the UMI-Bench protocol, episode metadata, scoring fields, condition splits, and reported model results.
- [UMI-Bench 1.0: An Open and Reproducible Real-World Benchmark for Tabletop Robotic Manipulation with UMI Data](../Inbox/2026-06-09--umi-bench-1-0-an-open-and-reproducible-real-world-benchmark-for-tabletop-robotic-manipulation-with-umi-data.md): Explains why hardware setup, camera placement, reset procedures, and action interfaces can confound real-world policy comparisons.
- [UMI-Bench 1.0: An Open and Reproducible Real-World Benchmark for Tabletop Robotic Manipulation with UMI Data](../Inbox/2026-06-09--umi-bench-1-0-an-open-and-reproducible-real-world-benchmark-for-tabletop-robotic-manipulation-with-umi-data.md): Describes the evaluation workflow: demonstration collection, episode specification, scene reset, policy execution, logging, scoring, and task-factor analysis.

## Asynchronous modality buffers for contact-rich VLA control
Contact-heavy manipulation systems should test a controller path where language, vision, force, and proprioception update on their own clocks. DAM-VLA shows the build pattern: encode language once, update vision sparsely, keep dense force and proprioception histories at the control rate, and let the action head read all latent buffers at every control step.

The operational pain is timing. Force-torque signals can carry contact transients at 100–500 Hz, while RGB changes useful for control may arrive closer to 3–10 Hz. A single-clock VLA can waste compute on repeated visual frames and miss fast contact changes. In DAM-VLA’s Franka tests, the asynchronous design reaches 95.2% average success across seven tasks, compared with 40.95% for the strongest synchronous baseline. A naive 100 Hz synchronous variant falls to 21.9%, so the first engineering check should compare timestamped force events, replanning rate, and task success against the current synchronous controller on socketing, button pressing, cleaning, or similar contact tasks.

### Sources
- [DAM-VLA: Decoupled Asynchronous Multimodal Vision Language Action model](../Inbox/2026-06-10--dam-vla-decoupled-asynchronous-multimodal-vision-language-action-model.md): Gives the DAM-VLA architecture, modality buffer design, 100 Hz control setup, and real-robot success comparisons.
- [DAM-VLA: Decoupled Asynchronous Multimodal Vision Language Action model](../Inbox/2026-06-10--dam-vla-decoupled-asynchronous-multimodal-vision-language-action-model.md): States the sensor-rate mismatch between force-torque signals and RGB observations.
- [DAM-VLA: Decoupled Asynchronous Multimodal Vision Language Action model](../Inbox/2026-06-10--dam-vla-decoupled-asynchronous-multimodal-vision-language-action-model.md): Describes the decoupled processing principle and per-modality temporal context.

## Interaction-evidence filtering for robot demonstration labels
Robot data teams should add an interaction-based reliability score to automatic labels before using large demonstration sets for spatial grounding. SPARC’s workflow is concrete enough to copy in a smaller pipeline: split demonstrations by gripper phase and language, propose candidate objects, track and lift them to 3D, then score candidates using motion during grasp, 3D proximity to the gripper, and overlap with the robot body.

The adoption blocker is label noise in cluttered scenes. Detector confidence can assign a high score to the wrong object because it measures recognition confidence, not whether the robot manipulated that object. SPARC reports 80.2% interacted-object localization accuracy on IA-Bench, compared with 58.1% for a detector-confidence baseline. At a 90% precision operating point, it keeps 77.6% coverage, while the strongest trajectory-filtering baseline keeps 33.1%. A practical rollout is to run the filter on a held-out slice of existing demonstrations, inspect low- and high-reliability buckets, and train one spatial-grounding model with the accepted labels.

### Sources
- [SPARC: Reliable Spatial Annotations from Robot Demonstrations at Scale](../Inbox/2026-06-11--sparc-reliable-spatial-annotations-from-robot-demonstrations-at-scale.md): Summarizes SPARC’s interaction-based scoring, IA-Bench, localization accuracy, coverage, and downstream spatial-grounding results.
- [SPARC: Reliable Spatial Annotations from Robot Demonstrations at Scale](../Inbox/2026-06-11--sparc-reliable-spatial-annotations-from-robot-demonstrations-at-scale.md): Describes SPARC as an automatic labeling system with bounding boxes, trajectories, phase labels, and reliability scores.
- [SPARC: Reliable Spatial Annotations from Robot Demonstrations at Scale](../Inbox/2026-06-11--sparc-reliable-spatial-annotations-from-robot-demonstrations-at-scale.md): Explains why detector confidence fails for interacted-object identity in cluttered robot demonstrations.
