---
kind: trend
trend_doc_id: 811
granularity: day
period_start: '2026-07-06T00:00:00'
period_end: '2026-07-07T00:00:00'
topics:
- robot manipulation
- vision-language-action models
- world models
- long-horizon control
- sim-to-real
- deformable objects
run_id: materialize-outputs
aliases:
- recoleta-trend-811
tags:
- recoleta/trend
- topic/robot-manipulation
- topic/vision-language-action-models
- topic/world-models
- topic/long-horizon-control
- topic/sim-to-real
- topic/deformable-objects
language_code: en
pass_output_id: 338
pass_kind: trend_synthesis
---

# Robot policies are adding explicit foresight, geometry, and task memory

## Overview
The day is dominated by robot-manipulation work that makes policy internals more explicit: future states, latent actions, camera pose, and subtask memory. InternVLA-A1.5, Cortex, and CamVLA show the current emphasis: keep language-conditioned control fast, then add the physical or temporal signal needed for longer, messier tasks.

## Findings

### Latent foresight and action codes
Several papers train Vision-Language-Action models, or VLAs, to carry a compact action-related signal inside the policy. InternVLA-A1.5 uses 50 foresight tokens that condition a frozen video generator during training, then removes the video branch at inference and outputs 50-step continuous action chunks. CAC-VLA predicts latent actions from image and language tokens, using them to condition the continuous action expert through gated cross-attention. GeoMoLa takes a more geometric route: it learns discrete motion codes by predicting future point-cloud changes, then uses those codes for 6-DoF manipulation.

The reported gains are strongest where the task requires generalization rather than only imitation. CAC-VLA reports 98.3% average success on LIBERO and 89.5% on LIBERO-Plus supervised fine-tuning. GeoMoLa reports 84.7% average success on single-view RLBench across 10 tasks and 166 variations, ahead of RVT2 at 80.4%. InternVLA-A1.5 claims the best overall results across six simulation benchmarks, although the available excerpt does not include exact benchmark tables.

### Long-horizon control with constrained subtasks
Long tasks are being handled with explicit subtask state and bounded skill vocabularies. Cortex uses a high-level vision-language model to maintain text memory and emit subtasks for a lower-level VLA. Its planner is restricted to 32 canonical manipulation primitives, with templates and reachability-aware annotations so the low-level policy receives executable commands.

DSWAM uses a related split. Its default path is a World Action Model executor that predicts dual-arm action chunks. A vision-language planner is activated when coarse household commands need decomposition. In real folding tests under the matched DeMaVLA setup, DSWAM raises success from 92.5% to 96.3% and reduces average completion time from 2'18" to 1'44". Cortex reports 65% success on 14-step real-world chemistry tasks and 55% on 14-step washing tasks, where the cited end-to-end baselines score 0%.

### Deployment gaps: camera pose and scene-specific data
Two papers target failures that appear after a trained policy leaves its original setup. CamVLA addresses camera movement. It predicts the end-effector action in the camera frame, estimates a 6-DoF hand-eye transform from one RGB image, and converts the action into the robot base frame. On RLBench unseen viewpoints, π0 improves from 33.2% to 51.4% mean success with CamVLA. In real Franka tests, π0 + CamVLA also keeps higher success at 5°, 10°, and 15° camera offsets.

PRISM addresses the lack of scene-matched demonstrations. From one target-scene image and an instruction, it builds varied simulated “digital cousin” scenes, plans trajectories, and trains policies on the generated data. In sim-to-sim tests with 400 trajectories per task, PRISM reaches 98.0% on LIBERO for “Put milk in basket” with π0.5, compared with 48.0% for X-Sim and 14.0% for RoboTwin 2.0.

### Deformable-object world models need touch and dense 3D tracking
Deform360 adds a data-heavy line of work to the same control problem. It collects 198 deformable objects across 1,980 interaction sequences with 41 synchronized cameras and tactile-equipped grippers. The dataset includes cloth-like, rope-like, and volumetric objects, with 13 manipulation primitive types across 17 categories.

The key contribution is the paired sensing. The pipeline reconstructs per-frame geometry, tracks up to 1,600 points per view, lifts tracks into 3D, and refines them with tactile contact consistency. The summary reports a Chamfer distance error of 2.71×10^-5 m² for visuotactile tracking, versus 1.41×10^-4 m² for visual-only tracking. Visual-to-contact prediction reaches 88.67% mean accuracy across 36 filtered views. This gives future robot world models a concrete benchmark for contact-rich deformable manipulation.
