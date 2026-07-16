---
kind: trend
trend_doc_id: 763
granularity: day
period_start: '2026-06-30T00:00:00'
period_end: '2026-07-01T00:00:00'
topics:
- robot learning
- vision-language-action models
- reinforcement learning
- humanoid manipulation
- tactile sensing
- world models
- robot safety
run_id: materialize-outputs
aliases:
- recoleta-trend-763
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/reinforcement-learning
- topic/humanoid-manipulation
- topic/tactile-sensing
- topic/world-models
- topic/robot-safety
language_code: en
pass_output_id: 324
pass_kind: trend_synthesis
---

# Robot VLA papers prioritize executable control and measured feedback

## Overview
The day’s robotics papers concentrate on making vision-language-action (VLA) policies executable: online adaptation, 3D/contact feedback, and cheaper planning models. SARL, 3D HAMSTER, and DVG-WM show the current emphasis on evidence that survives control loops, geometry, and physical interaction.

## Findings

### Online VLA adaptation
Several papers treat deployment as a learning loop. SARL trains over language prompts as semantic actions, then uses reward to learn which prompts produce useful robot behavior. On Libero-10 and four real WidowX tasks, it reports near-zero initial success under a single task prompt and about 80% success after 60 to 100 online episodes.

Z-1 applies reinforcement learning after supervised fine-tuning for flow-based VLA policies. On 24 RoboCasa tasks, its average success rises from 67.4% after supervised fine-tuning to 80.6% after group relative policy optimization. The strongest controlled claim is this 13.2-point gain over the authors’ own initialization, since some external comparisons use reported numbers from prior work.

A pruning study adds a deployment-cost angle. It uses weight changes during VLM-to-VLA adaptation to decide which OpenVLA and pi_0.5 components can be removed. The reported target is 12% to 30% parameter reduction while keeping about 90% of original LIBERO performance without post-pruning recovery.

#### Sources
- [Adapting Generalist Robot Policies with Semantic Reinforcement Learning](../Inbox/2026-06-30--adapting-generalist-robot-policies-with-semantic-reinforcement-learning.md): SARL prompt-level reinforcement learning and online adaptation results.
- [Z-1: Efficient Reinforcement Learning for Vision-Language-Action Models](../Inbox/2026-06-30--z-1-efficient-reinforcement-learning-for-vision-language-action-models.md): Z-1 RL post-training design and RoboCasa success-rate gains.
- [Revisiting Parameter Redundancy in Vision-Language-Action Models: Insights from VLM-to-VLA Adaptation](../Inbox/2026-06-30--revisiting-parameter-redundancy-in-vision-language-action-models-insights-from-vlm-to-vla-adaptation.md): VLA pruning results based on VLM-to-VLA weight divergence.

### 3D and tactile execution signals
Geometry and contact are treated as control inputs, not optional sensing. 3D HAMSTER predicts end-effector waypoints as 3D coordinates and feeds them to a point-cloud control policy. On DroidSpatial-Bench, it reaches 65.5% Both accuracy at 10 cm, ahead of RoboBrain-2.5-8B at 60.1% and far above general VLM baselines in the supplied results.

UniTacVLA adds tactile tokens, future tactile prediction, and a high-frequency correction controller for contact-rich tasks. Across eight real-robot subtasks with 50 trials per setting, it reports 64.0% clean success and 53.5% perturbed success. The perturbation result is the clearer signal: the reproduced tactile baseline pi0.5-TacVLA reaches 16.25% under perturbation.

The data side matches this emphasis. RoboTacDex contributes 6,000 humanoid trajectories with multi-view RGB-D, tactile signals, joint states, actions, and task labels on a Unitree G1. Human-as-Humanoid takes a different route by converting synchronized ego-exo human videos into executable 60-DoF humanoid labels, with a claimed 4.8× to 7.2× demonstration-throughput gain over humanoid teleoperation.

#### Sources
- [3D HAMSTER: Bridging Planning and Control in Hierarchical Vision Language Action Models through 3D Trajectory Guidance](../Inbox/2026-06-30--3d-hamster-bridging-planning-and-control-in-hierarchical-vision-language-action-models-through-3d-trajectory-guidance.md): 3D HAMSTER waypoint planning, depth encoding, and DroidSpatial-Bench results.
- [UniTacVLA: Unified Tactile Understanding and Prediction in Vision Language Action Models](../Inbox/2026-06-30--unitacvla-unified-tactile-understanding-and-prediction-in-vision-language-action-models.md): UniTacVLA tactile prediction, correction controller, and real-robot success rates.
- [RoboTacDex: A Dexterous Visual-Tactile-Action Dataset for Humanoid Manipulation](../Inbox/2026-06-30--robotacdex-a-dexterous-visual-tactile-action-dataset-for-humanoid-manipulation.md): RoboTacDex dataset size, modalities, and humanoid manipulation coverage.
- [Human-as-Humanoid: Enabling Zero-Shot Humanoid Learning from Ego-Exo Human Videos with Human-Aligned Embodiments](../Inbox/2026-06-30--human-as-humanoid-enabling-zero-shot-humanoid-learning-from-ego-exo-human-videos-with-human-aligned-embodiments.md): Human-as-Humanoid conversion pipeline and humanoid demonstration-throughput claim.

### World models and safety metrics
World-model work focuses on planning signals that are fast enough and action-sensitive enough to use inside control. DVG-WM splits video prediction into low-resolution dynamics and high-resolution refinement. On LIBERO video prediction, it reports 89% object-level accuracy and 88.7 seconds inference time, compared with 236.8 seconds for CogVideoX-5B and 354.2 seconds for LVP-14B.

AdaJEPA adapts a latent world model during model predictive control using the transition just observed after execution. The strongest supplied result is on unseen PointMaze layouts, where GD success improves from 53.3 ± 8.2 to 78.7 ± 5.0 and CEM success improves from 49.3 ± 6.2 to 70.7 ± 3.8.

Delta-JEPA targets action sensitivity without pixel reconstruction. Its latent displacement action decoder reconstructs the executed action from the change between latent states. Across four planning tasks, it reports the best success rate in the supplied table, including 89.07 ± 1.90 on Push-T and 79.27 ± 1.81 on OGB-Cube.

OopsieVerse adds a separate safety signal: explicit damage tracking for household manipulation. Its benchmark has 32 task instances across OmniGibson and RoboCasa, with mechanical, thermal, and fluid damage classes. The supplied text gives benchmark scope rather than quantitative policy gains, so its contribution is mainly evaluation design.

#### Sources
- [DVG-WM: Disentangled Video Generation Enables Efficient Embodied World Model for Robotic Manipulation](../Inbox/2026-06-30--dvg-wm-disentangled-video-generation-enables-efficient-embodied-world-model-for-robotic-manipulation.md): DVG-WM video world model design and LIBERO speed and quality results.
- [AdaJEPA: An Adaptive Latent World Model](../Inbox/2026-06-30--adajepa-an-adaptive-latent-world-model.md): AdaJEPA closed-loop test-time adaptation and PointMaze results.
- [Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding](../Inbox/2026-06-30--delta-jepa-learning-action-sensitive-world-models-via-latent-difference-decoding.md): Delta-JEPA latent displacement decoder and planning success rates.
- [OopsieVerse: A Safety Benchmark with Damage-Aware Simulation for Robot Manipulation](../Inbox/2026-06-30--oopsieverse-a-safety-benchmark-with-damage-aware-simulation-for-robot-manipulation.md): OopsieVerse damage-aware benchmark scope and damage classes.
