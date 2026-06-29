---
kind: ideas
granularity: day
period_start: '2026-04-02T00:00:00'
period_end: '2026-04-03T00:00:00'
run_id: 2b28af61-f822-4000-a611-e369ac085066
status: succeeded
topics:
- world-models
- vla-finetuning
- autonomous-driving
- uav-tracking
- robot-control
- adversarial-robustness
tags:
- recoleta/ideas
- topic/world-models
- topic/vla-finetuning
- topic/autonomous-driving
- topic/uav-tracking
- topic/robot-control
- topic/adversarial-robustness
language_code: en
pass_output_id: 11
pass_kind: trend_ideas
upstream_pass_output_id: 10
upstream_pass_kind: trend_synthesis
---

# Embodied policy reliability checks

## Summary
Recent work supports three concrete workflow changes: treat action tolerance and controller gains as part of the same robot finetuning loop, evaluate driving world-action models with explicit geometry in the planning path, and add object-surface adversarial tests to VLA manipulation release gates. The evidence is strongest where papers report operational metrics tied to deployment choices, including ManiSkill success gains for FAN-based finetuning, Navsim planning gains for depth-first driving models, and large failure-rate increases under Tex3D attacks.

## Action-distribution regularization and gain-aware finetuning for robot adaptation
Robot teams fine-tuning OpenVLA-like policies can add an action-distribution regularizer before they spend more on data collection. The usable change is narrow: keep probability mass over a small neighborhood of good actions during finetuning, then measure whether that improves held-out task success and OOD variants in the target environment. The FAN paper gives a concrete target for that check. On ManiSkill supervised finetuning with OpenVLA, in-distribution success rises from 78.1 to 89.8, and average OOD success rises from 58.1 to 63.3. That is large enough to justify a lightweight ablation in any manipulation stack that still trains against a single exact action label.

This also points to a practical support layer for deployment teams: inspection of action sharpness during finetuning. If the policy collapses to narrow peaks, that is a candidate failure mode for small demonstration sets and minor execution shifts. A cheap first test is to replay the current finetuning set, compare log-likelihood-only training against the same setup with a local Gaussian prior around the preferred action, and track success on small visual, semantic, and execution shifts. The controller-gain paper strengthens the case for this workflow because it shows that learnability depends on the control interface as well as the policy objective. In behavior cloning, the best closed-loop success appears in compliant, overdamped gain settings, and torque-to-position retargeting preserves at least 90% success with joint-position MSE below 1e-3 across gain settings up to 25x decimation. Teams adapting pretrained VLAs to a new arm or controller can treat action-tolerance tuning and gain selection as one finetuning problem, not two separate cleanup steps.

### Evidence
- [Boosting Vision-Language-Action Finetuning with Feasible Action Neighborhood Prior](../Inbox/2026-04-02--boosting-vision-language-action-finetuning-with-feasible-action-neighborhood-prior.md): Reports the core FAN regularizer and the verified ManiSkill gains for in-distribution and OOD success with OpenVLA finetuning.
- [Tune to Learn: How Controller Gains Shape Robot Policy Learning](../Inbox/2026-04-02--tune-to-learn-how-controller-gains-shape-robot-policy-learning.md): Shows that controller gains materially affect behavior-cloning learnability and that retargeted trajectories remain faithful across gain settings.

## Depth-first world-action planning for autonomous driving evaluation
Driving teams building world-action models can justify a geometry-first planning stack now that there is a concrete closed-loop result behind it. The build is specific: predict depth before future video and action, use that depth map as an explicit scaffold for imagination and planning, and keep the generators modular so planning-only and world-generation modes can share the same backbone. DriveDreamer-Policy gives a clean benchmark anchor for this design. On Navsim v1 it reaches 89.2 PDMS, ahead of PWM at 88.1, WoTE at 88.3, DriveVLA-W0 at 88.4, and AutoVLA at 89.1. On Navsim v2 it reaches 88.7 EPDMS, with the paper stating a 2.6-point gain over the previous method shown in the table.

The practical workflow change is in evaluation as much as model design. A visually convincing rollout is not enough if the representation misses free space, layout, or occlusion structure. A simple adoption path is to run a depth-first ablation against an existing future-video planner, then compare closed-loop planning scores and a small set of occlusion-heavy cases. The same logic appears in WAV for robot world models: verification improves when future-state plausibility and action reachability are checked separately, and the paper reports 2x sample efficiency across nine tasks plus an 18% downstream policy gain. Together, these results support a planning workflow where geometry and reachability get explicit intermediate checks, not just a final action loss.

### Evidence
- [DriveDreamer-Policy: A Geometry-Grounded World-Action Model for Unified Generation and Planning](../Inbox/2026-04-02--drivedreamer-policy-a-geometry-grounded-world-action-model-for-unified-generation-and-planning.md): Provides the geometry-first architecture and benchmarked planning gains on Navsim v1 and v2.
- [World Action Verifier: Self-Improving World Models via Forward-Inverse Asymmetry](../Inbox/2026-04-02--world-action-verifier-self-improving-world-models-via-forward-inverse-asymmetry.md): Supports the broader workflow of explicit intermediate verification with measured gains in sample efficiency and downstream policy quality.

## Object-surface adversarial testing for VLA manipulation release checks
Anyone evaluating VLA manipulation systems on physical tasks needs an object-surface attack test in the release checklist. Tex3D is concrete enough to move this from a research warning to a standard red-team step. The attack is attached to the manipulated object's 3D texture, optimized through a differentiable rendering path, and kept effective across long episodes with trajectory-aware weighting. In simulation, the failure jumps are large across several common models: OpenVLA rises from 24.1% to 88.1% under untargeted attack, OpenVLA-OFT from 4.7% to 76.0%, and pi0 from 4.6% to 71.8%. On OpenVLA spatial tasks, failure reaches 96.7% under targeted attack.

The workflow change is straightforward. Before shipping a new checkpoint, take a small set of benchmark objects, optimize surface textures against the frozen policy in simulation, and record failure rates by task family and object category. That gives teams a way to find policies that rely on brittle visual shortcuts even when standard perturbation tests look clean. The paper does not yet give a defense recipe with verified recovery numbers, so the near-term product is an evaluation harness and acceptance threshold, not a robustness claim. For teams selling VLA systems into warehouses, labs, or homes, that harness is easier to adopt than waiting for a full training-time defense stack.

### Evidence
- [Tex3D: Objects as Attack Surfaces via Adversarial 3D Textures for Vision-Language-Action Models](../Inbox/2026-04-02--tex3d-objects-as-attack-surfaces-via-adversarial-3d-textures-for-vision-language-action-models.md): Documents the physically grounded 3D texture attack method and the large measured failure-rate increases across OpenVLA, OpenVLA-OFT, and pi0.
