---
kind: ideas
granularity: day
period_start: '2026-04-28T00:00:00'
period_end: '2026-04-29T00:00:00'
run_id: 81e6e7e1-5ab2-429a-89bf-31d72f3afc85
status: succeeded
topics:
- robot learning
- photorealistic simulation
- 3D Gaussian Splatting
- dexterous manipulation
- contact-rich robotics
tags:
- recoleta/ideas
- topic/robot-learning
- topic/photorealistic-simulation
- topic/3d-gaussian-splatting
- topic/dexterous-manipulation
- topic/contact-rich-robotics
language_code: en
pass_output_id: 119
pass_kind: trend_ideas
upstream_pass_output_id: 118
upstream_pass_kind: trend_synthesis
---

# Contact-ready manipulation training

## Summary
Two practical changes stand out: validate real-capture simulation scenes before long visual RL runs, and score dexterous grasps by the fingers they leave available for the next action. Both target a common source of wasted training time: policies that look stable before contact and fail when the task needs physical follow-through.

## Capture-to-simulation checks for contact-rich visual RL scenes
Robotics teams training camera-conditioned manipulation policies can add a short validation step before long RL runs: capture RGB views, generate 3DGS assets with meshes, poses, scales, and collision elements, then run a fixed contact test and a rendered-image throughput test.

GS-Playground gives this workflow a concrete shape. Its Real2Sim pipeline turns RGB captures into simulation-ready scene parts, while its renderer binds Gaussian assets to rigid bodies so rendered objects move with the physics state during contact. The reported scale is high enough for a practical smoke test: about 10,000 FPS 3DGS rendering at 640×480 on an RTX 4090-class setup, up to 2048 rendered scenes at that resolution, and more than 90% Gaussian pruning with PSNR loss below 0.05.

A useful first build is a scene intake script for a manipulation lab: accept a captured object set, create the visual and collision assets, prune the Gaussians, then run a small set of pushes, stacks, or grasps while checking image quality, rigid-body attachment, contact stability, and GPU memory. Scenes that fail these checks can be fixed before they consume RL training time.

### Evidence
- [GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning](../Inbox/2026-04-28--gs-playground-a-high-throughput-photorealistic-simulator-for-vision-informed-robot-learning.md): Summarizes GS-Playground's batched 3DGS renderer, Real2Sim pipeline, rigid-body Gaussian binding, rendering throughput, pruning result, and contact-oriented physics details.
- [GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning](../Inbox/2026-04-28--gs-playground-a-high-throughput-photorealistic-simulator-for-vision-informed-robot-learning.md): Describes the bottleneck in high-resolution rendering, out-of-memory failures, and the manual work of creating simulation-ready assets.
- [GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning](../Inbox/2026-04-28--gs-playground-a-high-throughput-photorealistic-simulator-for-vision-informed-robot-learning.md): States that the workflow converts real-world scenes into functional digital twins with visual realism and physical consistency.

## Finger reservation tests for two-step LEAP Hand tasks
Teams building multi-finger hand policies can add a grasp evaluation that measures which fingers remain usable after the first object is held. The test is simple: train or sample first-stage grasps, label the fingers assigned to the held object, penalize force from fingers reserved for the next action, and evaluate each grasp as a starting state for the second task.

HANDFUL shows why this matters for table-clearing and workspace-organization tasks where a hand must hold one object and then push a button, pull a drawer, twist a knob, or pick up another object. In simulation, the method reached 69.90% success on Push Object, 77.75% on Press Button, 61.52% on Twist Knob, 78.94% on Pull Drawer, and 76.54% on Pick Second. Removing finger constraints dropped Pick Second to 0.00% and cut several other tasks.

A practical adoption change is to treat first grasps as candidates for a task sequence, then keep only the ones that support the next action. HANDFUL’s curriculum kept similar final success while reducing second-stage training from 90 million to 54 million steps, which gives teams a concrete training-budget check for this workflow.

### Evidence
- [HANDFUL: Sequential Grasp-Conditioned Dexterous Manipulation with Resource Awareness](../Inbox/2026-04-28--handful-sequential-grasp-conditioned-dexterous-manipulation-with-resource-awareness.md): Summarizes the two-step task setup, finger-level contact rewards and penalties, curriculum, simulation success rates, and ablation results.
- [HANDFUL: Sequential Grasp-Conditioned Dexterous Manipulation with Resource Awareness](../Inbox/2026-04-28--handful-sequential-grasp-conditioned-dexterous-manipulation-with-resource-awareness.md): Explains the failure mode where stable grasps occupy fingers or contact regions needed for later actions.
- [HANDFUL: Sequential Grasp-Conditioned Dexterous Manipulation with Resource Awareness](../Inbox/2026-04-28--handful-sequential-grasp-conditioned-dexterous-manipulation-with-resource-awareness.md): Describes preserving unused fingers and contact regions, selecting grasps for downstream subtasks, and the LEAP Hand benchmark tasks.
