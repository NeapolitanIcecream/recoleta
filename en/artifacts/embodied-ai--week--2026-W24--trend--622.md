---
kind: trend
trend_doc_id: 622
granularity: week
period_start: '2026-06-08T00:00:00'
period_end: '2026-06-15T00:00:00'
topics:
- robotics
- vision-language-action models
- manipulation
- real-robot evaluation
- temporal modeling
- contact control
- spatial grounding
run_id: materialize-outputs
aliases:
- recoleta-trend-622
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action-models
- topic/manipulation
- topic/real-robot-evaluation
- topic/temporal-modeling
- topic/contact-control
- topic/spatial-grounding
language_code: en
pass_output_id: 288
pass_kind: trend_synthesis
---

# Robot VLA work is being tested against time, contact, and missing evidence

## Overview
Robot vision-language-action (VLA) work this week is judged by execution details: memory, recovery, occlusion, contact timing, and task-specific labels. MemoryVLA++, UMI-Bench 1.0, and DAM-VLA anchor the strongest evidence.

## Clusters

### Temporal state and recovery
Several papers treat robot policy failure as a timing problem. MemoryVLA++ adds long-term memory and latent future prediction so the policy can remember earlier interactions and anticipate object motion. It reports real-robot gains of 9, 26, and 28 percentage points across general, memory-dependent, and imagination-dependent task groups.

B2FF handles a narrower case: a frozen VLA policy drifts off a nominal trajectory after perturbation. It pre-generates future visual milestones, then selects a recovery target at execution time. On failure-injected LIBERO, average success rises from 56.3% to 74.0%. The shared lesson is practical: policies need access to past state and plausible near-future state when the current camera view is incomplete.

#### Evidence
- [MemoryVLA++: Temporal Modeling via Memory and Imagination in Vision-Language-Action Models](../Inbox/2026-06-08--memoryvla-temporal-modeling-via-memory-and-imagination-in-vision-language-action-models.md): MemoryVLA++ summary provides method details and reported simulation and real-robot gains.
- [Back to the Familiar Future: Failure Recovery for VLA Policies via Pre-Imagined Milestone Selection](../Inbox/2026-06-08--back-to-the-familiar-future-failure-recovery-for-vla-policies-via-pre-imagined-milestone-selection.md): B2FF summary provides the failure-recovery setup and LIBERO success-rate gains.

### Occlusion and physical benchmarks
Evaluation work focuses on cases where standard manipulation benchmarks can hide the real difficulty. LIBERO-Occ adds scene-induced occluders to LIBERO and shows large drops for existing VLA policies when objects or goal regions are hidden. Its Viewpoint Imagination method reaches 65.05% average success without a real complementary view, compared with 57.10% for the strongest listed baseline.

UMI-Bench 1.0 addresses another source of weak claims: physical rollout differences. It fixes the wrist-view observation setup, reset procedure, action interface, logging, and scoring for 10 tabletop tasks. The reported results show that layout, pose, and dynamics shifts hurt more than appearance and object shifts, and two long-horizon tasks reach 0% full success for all three evaluated models.

#### Evidence
- [LIBERO-Occ: Evaluating and Improving Vision-Language-Action Models under Scene-Induced Occlusion via Viewpoint Imagination](../Inbox/2026-06-09--libero-occ-evaluating-and-improving-vision-language-action-models-under-scene-induced-occlusion-via-viewpoint-imagination.md): LIBERO-Occ summary gives benchmark design, occlusion types, and VIM results.
- [UMI-Bench 1.0: An Open and Reproducible Real-World Benchmark for Tabletop Robotic Manipulation with UMI Data](../Inbox/2026-06-09--umi-bench-1-0-an-open-and-reproducible-real-world-benchmark-for-tabletop-robotic-manipulation-with-umi-data.md): UMI-Bench summary gives the real-robot protocol, task coverage, and reported model results.

### Contact and sensor timing
Contact-rich manipulation papers put pressure on the single-clock design used by many VLA policies. DAM-VLA keeps separate latent buffers for language, vision, force, and proprioception, then lets the action head read them at every control step. This matches slow language and visual updates with faster force and state signals.

The reported numbers are unusually concrete for this week. On seven real Franka tasks, DAM-VLA reaches 95.2% average success, compared with 40.95% for the strongest synchronous baseline. A naive 100 Hz synchronous setup falls to 21.9%, which supports the paper’s claim that update timing matters as much as sensor choice in contact-heavy tasks.

#### Evidence
- [DAM-VLA: Decoupled Asynchronous Multimodal Vision Language Action model](../Inbox/2026-06-10--dam-vla-decoupled-asynchronous-multimodal-vision-language-action-model.md): DAM-VLA summary gives the asynchronous modality design and real-robot success rates.

### Grounding data for specific tasks
The week also adds infrastructure for making robot data match the task. SPARC auto-labels robot demonstrations with object boxes, trajectories, and manipulation phases, then scores annotation reliability using interaction evidence. On IA-Bench, it reaches 80.2% interacted-object localization accuracy, compared with 58.1% for a detector-confidence baseline.

LabVLA and GIVE show two specialized forms of grounding. LabVLA builds synthetic laboratory scenes and workflows so a VLA policy can execute written bench protocols across robot embodiments. GIVE adds gesture cues for handover tasks; in real-world trials it reports 80.0% handover success, while the baseline reaches 0.0%. These papers make the same demand of data: labels, instructions, and observations must carry the cues the robot actually needs at execution time.

#### Evidence
- [SPARC: Reliable Spatial Annotations from Robot Demonstrations at Scale](../Inbox/2026-06-11--sparc-reliable-spatial-annotations-from-robot-demonstrations-at-scale.md): SPARC summary gives the annotation method, IA-Bench scale, and localization results.
- [LabVLA: Grounding Vision-Language-Action Models in Scientific Laboratories](../Inbox/2026-06-11--labvla-grounding-vision-language-action-models-in-scientific-laboratories.md): LabVLA summary gives the lab-specific data engine, supported robots, and benchmark claim.
- [GIVE: Grounding Human Gestures in Vision-Language-Action Models](../Inbox/2026-06-11--give-grounding-human-gestures-in-vision-language-action-models.md): GIVE summary gives the gesture-grounding method and real-world handover results.
