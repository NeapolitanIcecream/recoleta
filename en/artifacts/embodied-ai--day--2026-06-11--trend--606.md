---
kind: trend
trend_doc_id: 606
granularity: day
period_start: '2026-06-11T00:00:00'
period_end: '2026-06-12T00:00:00'
topics:
- robot manipulation
- VLA
- tactile sensing
- world models
- data annotation
- dexterous robotics
- real-time control
run_id: materialize-outputs
aliases:
- recoleta-trend-606
tags:
- recoleta/trend
- topic/robot-manipulation
- topic/vla
- topic/tactile-sensing
- topic/world-models
- topic/data-annotation
- topic/dexterous-robotics
- topic/real-time-control
language_code: en
pass_output_id: 280
pass_kind: trend_synthesis
---

# Robot learning is being judged by labels, contact, timing, and task context

## Overview
Robot learning papers in this period tie model gains to deployable constraints: reliable labels, contact control, latency, and task-specific grounding. SPARC, Mana, and LabVLA show the main emphasis: make the data and policy match the physical task before scaling the model.

## Findings

### Reliable grounding data
Several papers treat grounding errors as a data problem. SPARC auto-labels robot demonstrations with interacted-object boxes, trajectories, and phase labels, then filters them with a reliability score based on motion, gripper proximity, and robot-body overlap. On IA-Bench, it reports 80.2% interacted-object localization accuracy, compared with 58.1% for a detector-confidence baseline, and keeps 77.6% coverage at a 90% precision operating point.

LabVLA builds laboratory supervision in simulation because standard vision-language-action (VLA) policies rarely see lab instruments, liquids, and protocol workflows. Its RoboGenesis engine creates 2,947 annotated assets, more than 1,000 textures, 10,000 lab scenes, and demonstrations across 16 robot platforms. GIVE adds human gestures to VLA inputs for handover: skeleton overlays, fingertip rays, and short semantic gesture descriptions raise real-world handover success to 80.0%, compared with 0.0% for the base policy in the reported trials.

#### Sources
- [SPARC: Reliable Spatial Annotations from Robot Demonstrations at Scale](../Inbox/2026-06-11--sparc-reliable-spatial-annotations-from-robot-demonstrations-at-scale.md): SPARC summary gives the interaction-aware auto-labeling method and IA-Bench precision/coverage results.
- [LabVLA: Grounding Vision-Language-Action Models in Scientific Laboratories](../Inbox/2026-06-11--labvla-grounding-vision-language-action-models-in-scientific-laboratories.md): LabVLA summary gives the laboratory data engine scale and cross-embodiment setup.
- [GIVE: Grounding Human Gestures in Vision-Language-Action Models](../Inbox/2026-06-11--give-grounding-human-gestures-in-vision-language-action-models.md): GIVE summary gives the gesture augmentation method and real-world handover metrics.

### Contact-rich dexterity
Dexterous manipulation papers focus on the physical source of failure: thin tools slip, tactile sensors vary by hardware, and hand mechanics shape contact before software sees a stable state. Mana generates grasp keyframes for articulated tools, then fills contact-rich phases with short-horizon reinforcement learning. It reports zero-shot sim-to-real transfer on tongs, pliers, clothespins, and syringes, with many per-task success rates around 0.6 to 0.8 across 10 trials.

FTP-1 tackles tactile transfer by mapping heterogeneous tactile inputs into a shared morphology-aware token space. It pretrains on about 3,000 hours of data from 26 sources and 21 tactile sensors, then reports 66.66% average success on UniVTAC and 46.6% on unseen sensor setups, compared with 15.0% for its FTP-pi0.5 baseline. MCR-Bionic Hand adds a hardware-side argument: a musculoskeletal hand with 23 bones, 61 wrist ligaments, more than 103 soft-tissue constraints, and 46 muscle units can encode useful grasp pre-shaping and fingertip force paths in its structure.

#### Sources
- [Mana: Dexterous Manipulation of Articulated Tools](../Inbox/2026-06-11--mana-dexterous-manipulation-of-articulated-tools.md): Mana summary gives the articulated-tool pipeline and sim-to-real success ranges.
- [FTP-1: A Generalist Foundation Tactile Policy Across Tactile Sensors for Contact-Rich Manipulation](../Inbox/2026-06-11--ftp-1-a-generalist-foundation-tactile-policy-across-tactile-sensors-for-contact-rich-manipulation.md): FTP-1 summary gives tactile pretraining scale and seen/unseen sensor results.
- [MCR-Bionic Hand: Anatomical Structural Priors for Dexterous Manipulation](../Inbox/2026-06-11--mcr-bionic-hand-anatomical-structural-priors-for-dexterous-manipulation.md): MCR-Bionic Hand summary gives the anatomical design details and hardware claims.

### Policy structure for real execution
Execution papers add structure around when a robot sees, how two arms act, and how action tokens are decoded under latency limits. The real-time autoregressive policy paper changes action-token chunking and uses constrained decoding so inference stays within a fixed latency budget. On LIBERO, pi0-REALFAST reaches 95.7% average task success, compared with 89.4% for pi0 plus real-time control and 94.7% for pi0.5 plus real-time control.

The bimanual manipulation paper separates visual routing from action routing. A View-Selective Visual Router reweights left and right wrist-camera tokens, and an Interaction-Aware Action Mixture-of-Experts chooses coordinated or arm-wise action pathways. On six RoboTwin 2.0 tasks, the full model reaches 69.6% average success, compared with 41.9% for the monolithic baseline. In three long-horizon real-world tasks, the reported gain over the same baseline is 43.3 percentage points.

#### Sources
- [Real-Time Execution with Autoregressive Policies](../Inbox/2026-06-11--real-time-execution-with-autoregressive-policies.md): Real-time autoregressive policy summary gives the constrained decoding method and LIBERO results.
- [See Selectively, Act Adaptively: Dual-Level Structural Decomposition for Bimanual Robot Manipulation](../Inbox/2026-06-11--see-selectively-act-adaptively-dual-level-structural-decomposition-for-bimanual-robot-manipulation.md): Bimanual manipulation summary gives the visual/action routing design and simulation plus real-world gains.

### World models with action scores
World-model papers make prediction useful by adding action values, events, or direct control outputs. WEAVER predicts future latent states, rewards, and decoded observations from multiview inputs and action chunks. It reports FID 10.20 and FVD 27.83 on DROID exterior-view validation at 16 NFE, a 0.870 correlation with real-world success rate for policy evaluation, and a 38% real-world success-rate improvement for pi0.5 without extra real-world interaction.

EA-WM adds event prediction and verification to feature rollouts. Its verifier scores imagined futures by task progress, semantic consistency, physical feasibility, and uncertainty; on the LIBERO wine-rack task, an online hybrid setup reaches 97/100 success at horizon 20. NavWAM applies the same action-centered idea to goal-conditioned visual navigation by learning future views, action chunks, and goal-progress values together. In real-robot tests, it reaches the goal in 19 of 24 episodes, compared with 14 of 24 for OmniVLA and 4 of 24 for NWM.

#### Sources
- [$\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation](../Inbox/2026-06-11--texttt-weaver-better-faster-longer-an-effective-world-model-for-robotic-manipulation.md): WEAVER summary gives multiview world-model design, prediction metrics, and policy improvement results.
- [EA-WM: Event-Aware World Models with Task-Specification Grounding for Long-Horizon Manipulation](../Inbox/2026-06-11--ea-wm-event-aware-world-models-with-task-specification-grounding-for-long-horizon-manipulation.md): EA-WM summary gives task-event verification and LIBERO wine-rack success.
- [NavWAM: A Navigation World Action Model for Goal-Conditioned Visual Navigation](../Inbox/2026-06-11--navwam-a-navigation-world-action-model-for-goal-conditioned-visual-navigation.md): NavWAM summary gives joint prediction/action/value training and real-robot navigation results.
