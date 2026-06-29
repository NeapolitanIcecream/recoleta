---
kind: trend
trend_doc_id: 140
granularity: day
period_start: '2026-04-16T00:00:00'
period_end: '2026-04-17T00:00:00'
topics:
- robotics
- vision-language-action
- data generation
- dexterous manipulation
- sim2real
run_id: materialize-outputs
aliases:
- recoleta-trend-140
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/data-generation
- topic/dexterous-manipulation
- topic/sim2real
language_code: en
pass_output_id: 74
pass_kind: trend_synthesis
---

# Robotics papers put structure into control and data collection

## Overview
This day’s robotics set is strongest on one point: researchers are putting task structure into the data path and decision path. The clearest examples are $\pi_{0.7}$, WAV, and ShapeGen. One line adds richer prompts and latent planning to VLA control. Another line builds narrower, geometry-aware data generation and capture systems so policies see the right variation in the first place.

## Clusters

### Structured VLA control
Generalist robot models now add more structure to the prompt and the rollout, not just more data. $\pi_{0.7}$ conditions action generation on task text, subtask text, episode metadata, control mode, and optional subgoal images from a world model. The paper ties that prompt design to zero-shot behavior on long dexterous tasks such as espresso making, folding laundry, and trash handling, plus cross-embodiment transfer. WAV pushes the same theme on the planning side. It combines a future predictor, a value model, and an action decoder, then searches in latent space rather than raw actions. The evidence here is stronger on mechanism than on exact margins, because the excerpt does not include full task tables for either paper.

#### Evidence
- [$π_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities](../Inbox/2026-04-16--p-0-7-a-steerable-generalist-robotic-foundation-model-with-emergent-capabilities.md): Prompt-conditioned VLA design, model scale, and claimed zero-shot dexterous generalization.
- [World-Value-Action Model: Implicit Planning for Vision-Language-Action Systems](../Inbox/2026-04-16--world-value-action-model-implicit-planning-for-vision-language-action-systems.md): World-value-action decomposition and latent-space planning claims for long-horizon VLA control.

### Data generation targets the gap directly
Several papers attack generalization by generating better robot data around the failure mode they care about. ShapeGen creates new real-to-real demonstrations by swapping objects within a category using learned 3D warps. The gains are concrete: hang_mug rises from 5% to 45%, hang_mug_hard from 5% to 50%, and serve_kettle from 35% to 75% on unseen instances. DockAnywhere does the same for mobile manipulation under docking error. It reuses the contact-rich part of a demo, replans only the approach segments, and edits RGB-D observations in 3D. In ManiSkill with five docking points, it reaches 78.9% overall success, versus 17.8% for plain DP3 and 74.2% for DP3+DemoGen. The common pattern is narrow augmentation with task geometry kept intact.

#### Evidence
- [ShapeGen: Robotic Data Generation for Category-Level Manipulation](../Inbox/2026-04-16--shapegen-robotic-data-generation-for-category-level-manipulation.md): Real-to-real shape augmentation and task-level gains on unseen object instances.
- [DockAnywhere: Data-Efficient Visuomotor Policy Learning for Mobile Manipulation via Novel Demonstration Generation](../Inbox/2026-04-16--dockanywhere-data-efficient-visuomotor-policy-learning-for-mobile-manipulation-via-novel-demonstration-generation.md): Docking-pose augmentation method and benchmark results under viewpoint variation.

### Dexterous data collection gets more practical
Dexterous manipulation work in this window puts weight on how data is captured, not only on model design. DEX-Mouse is a portable hand-held interface built from off-the-shelf parts for under USD 150. In its attached forearm setup, it reaches 86.67% overall success and 10.05 s average completion time, ahead of two glove baselines in the reported study. HRDexDB tackles the same bottleneck at dataset scale. It pairs human and robot grasps on the same 100 objects, with 1.4K trials, 12.8M frames, 23 video views, object pose, tactile signals, and success labels across four embodiments. That gives the field more grounded material for cross-embodiment learning and grasp analysis.

#### Evidence
- [DEX-Mouse: A Low-cost Portable and Universal Interface with Force Feedback for Data Collection of Dexterous Robotic Hands](../Inbox/2026-04-16--dex-mouse-a-low-cost-portable-and-universal-interface-with-force-feedback-for-data-collection-of-dexterous-robotic-hands.md): Low-cost dexterous data collection interface with attached-mode user study results.
- [HRDexDB: A Large-Scale Dataset of Dexterous Human and Robotic Hand Grasps](../Inbox/2026-04-16--hrdexdb-a-large-scale-dataset-of-dexterous-human-and-robotic-hand-grasps.md): Large paired human-robot grasp dataset with synchronized tactile and motion data.

### Abstract simulators get a grounded transfer recipe
Sim2real work here focuses on the case where the simulator is missing real state, not just mis-tuned physics. ASTRA treats that as a history-dependent grounding problem. It learns a recurrent latent state from abstracted real trajectories, then corrects the simulator with transition, reward, and next-state losses. The reported evidence is selective but useful: in a morphology-shift AntMaze test with 1.25× leg length, success reaches 65% on U-Maze versus 21% for direct transfer. This matters because many practical simulators stay coarse on purpose, and the paper gives a concrete recipe for training in that setting with limited real data.

#### Evidence
- [Abstract Sim2Real through Approximate Information States](../Inbox/2026-04-16--abstract-sim2real-through-approximate-information-states.md): Formalization of abstract sim2real and reported morphology-shift result for ASTRA.
