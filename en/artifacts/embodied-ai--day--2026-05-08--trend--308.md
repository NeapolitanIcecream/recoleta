---
kind: trend
trend_doc_id: 308
granularity: day
period_start: '2026-05-08T00:00:00'
period_end: '2026-05-09T00:00:00'
topics:
- robotics
- vision-language-action
- world models
- tactile control
- federated learning
- policy adaptation
run_id: materialize-outputs
aliases:
- recoleta-trend-308
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/tactile-control
- topic/federated-learning
- topic/policy-adaptation
language_code: en
pass_output_id: 138
pass_kind: trend_synthesis
---

# Robot VLA papers are optimizing for deployable foresight

## Overview
Robot papers in this window treat Vision-Language-Action (VLA) policies as deployable control systems. Compact world state, contact feedback, failure data, and low-budget adaptation all receive concrete tests. OneWM-VLA, AT-VLA, and ForgeVLA give the clearest measured signal.

## Clusters

### Compact and plannable world models
World-model work centers on smaller latent state and better planning signals. OneWM-VLA compresses each camera view and frame into one semantic token, then generates future latent tokens and action chunks together. It reports MetaWorld average success of 61.3% against 47.9% for π0, 98.1% average success on LIBERO, and 71.7% real Piper-arm success under clean conditions against 50.0% for π0.

RLA-WM uses Residual Latent Action (RLA), a compact code for DINO feature changes. It predicts future visual features with 3.5T FLOPs per inference and beats listed feature and flow baselines on ManiSkill and IWS prediction metrics. RC-aux adds reachability supervision to latent world models, showing that accurate short-horizon prediction can still mislead a planner. On Wall, it raises success to 83.6 ± 3.6 compared with 50.4 ± 6.5 for the LeWM control.

#### Evidence
- [One Token Per Frame: Reconsidering Visual Bandwidth in World Models for VLA Policy](../Inbox/2026-05-08--one-token-per-frame-reconsidering-visual-bandwidth-in-world-models-for-vla-policy.md): OneWM-VLA compression design and success-rate results across MetaWorld, LIBERO, and real Piper tasks.
- [Learning Visual Feature-Based World Models via Residual Latent Action](../Inbox/2026-05-08--learning-visual-feature-based-world-models-via-residual-latent-action.md): RLA-WM residual latent action design, prediction metrics, and compute comparison.
- [Predictive but Not Plannable: RC-aux for Latent World Models](../Inbox/2026-05-08--predictive-but-not-plannable-rc-aux-for-latent-world-models.md): RC-aux reachability training and goal-conditioned control gains.

### Contact and failure signals for VLA control
Several papers add feedback channels that only appear during execution. AT-VLA adds a tactile gate and a dual stream: slower vision-language reasoning plus faster tactile correction. The paper reports closed-loop tactile response within 0.04 s. In real-robot contact-rich tasks, AT-VLA improves Unzip Bag to 0.33 success against 0.20 for GO-1 and 0.00 for π0.5, and Wipe Vase to 0.67 against 0.07 and 0.33.

AFIL uses failed rollouts as negative guidance for diffusion- and flow-based VLA policies. It trains separate success and failure action generators while sharing one vision-language backbone. The available summary gives no table values, so the grounded point is architectural: failure data becomes an online training signal and a sampling-time repulsion term.

#### Evidence
- [AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models](../Inbox/2026-05-08--at-vla-adaptive-tactile-injection-for-enhanced-feedback-reaction-in-vision-language-action-models.md): AT-VLA tactile gating, dual-stream design, reaction time, and real-robot success rates.
- [Failing Forward: Adaptive Failure-Informed Learning for Vision-Language-Action Models](../Inbox/2026-05-08--failing-forward-adaptive-failure-informed-learning-for-vision-language-action-models.md): AFIL failure-rollout collection, dual action generators, and adaptive negative guidance.

### Data-constrained VLA training
The training papers focus on data that is private, sparse, or domain-specific. ForgeVLA trains on distributed vision-action logs without centralizing raw data or adding manual language labels. Each client assigns pseudo instructions locally, while a contrastive planning loss and server aggregation handle non-i.i.d. robot data. On LIBERO-Goal, it reaches 55.2% success and 100% Pass@50 compared with 28.8% and 80% for FedAvg.

ACA addresses small real-robot adaptation budgets by repeating demonstrations at selected anchor conditions, then collecting boundary data where the policy deviates. With 100 trajectories on a Franka Panda setup, π0.5 plus ACA reaches 72.5% mean success against 31.7% for π0.5. BioProVLA-Agent applies the same deployment pressure in wet labs: it parses biology protocols into verified subtasks, uses visual checks before and after actions, and runs on a reported 800–850 USD hardware platform, though the excerpt gives no exact success rates.

#### Evidence
- [ForgeVLA: Federated Vision-Language-Action Learning without Language Annotations](../Inbox/2026-05-08--forgevla-federated-vision-language-action-learning-without-language-annotations.md): ForgeVLA federated training design and LIBERO results.
- [Escaping the Diversity Trap in Robotic Manipulation via Anchor-Centric Adaptation](../Inbox/2026-05-08--escaping-the-diversity-trap-in-robotic-manipulation-via-anchor-centric-adaptation.md): Anchor-Centric Adaptation method and real-robot success gains under limited demonstrations.
- [BioProVLA-Agent: An Affordable, Protocol-Driven, Vision-Enhanced VLA-Enabled Embodied Multi-Agent System with Closed-Loop-Capable Reasoning for Biological Laboratory Manipulation](../Inbox/2026-05-08--bioprovla-agent-an-affordable-protocol-driven-vision-enhanced-vla-enabled-embodied-multi-agent-system-with-closed-loop-capable-reasoning-for-biological-laboratory-manipulation.md): BioProVLA-Agent protocol parsing, verification loop, low-cost platform, and benchmark scope.

### Physical consistency as a world-model criterion
LaWM and Sword make rollout quality a control requirement. LaWM defines the next latent state through a learned least-action objective and an unrolled solver. Its strongest numbers are on controlled physical motion: PIS-vx reaches 0.9938 ± 0.0045, and acceleration consistency PIS-ax reaches 0.8964 ± 0.0275 against 0.6568 ± 0.013 for NewtonGen.

Sword trains an action-conditioned world model for LIBERO rollouts under visual style changes. Dynamic Latent Bootstrapping caches predicted VAE latents and gradually feeds them into training, cutting context-frame storage to under 20 GB. On LIBERO-Mixed, Sword reports FID 32.59 and FVD 111.19 against 119.62 and 198.84 for WoVR.

#### Evidence
- [LaWM: Least Action World Models for Long-Horizon Physical Consistency from Visual Observations](../Inbox/2026-05-08--lawm-least-action-world-models-for-long-horizon-physical-consistency-from-visual-observations.md): LaWM least-action transition design and physical consistency metrics.
- [Sword: Style-Robust World Models as Simulators via Dynamic Latent Bootstrapping for VLA Policy Post-Training](../Inbox/2026-05-08--sword-style-robust-world-models-as-simulators-via-dynamic-latent-bootstrapping-for-vla-policy-post-training.md): Sword style augmentation, Dynamic Latent Bootstrapping, storage claim, and LIBERO generation metrics.
