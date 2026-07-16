---
kind: trend
trend_doc_id: 735
granularity: week
period_start: '2026-06-22T00:00:00'
period_end: '2026-06-29T00:00:00'
topics:
- robotics
- vision-language-action
- robot manipulation
- deployment adaptation
- robot safety
- world models
run_id: materialize-outputs
aliases:
- recoleta-trend-735
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/robot-manipulation
- topic/deployment-adaptation
- topic/robot-safety
- topic/world-models
language_code: en
pass_output_id: 320
pass_kind: trend_synthesis
---

# Robot VLA reliability is being measured in rollouts, calibration, and safety cost

## Overview
Robot vision-language-action (VLA) research this week centers on policies that can be checked during execution. FORCE, ICWM, and LIBERO-Safety anchor the signal: robot papers are tying progress to online rollouts, setup calibration, and unsafe-success metrics.

## Findings

### Deployment adaptation
Several papers treat the deployed robot as a system that needs local evidence before or during the task. ICWM lets a policy run a short probing phase, then uses the observed action-to-image changes as context for control under new camera views or body setups. FORCE uses online rollouts to fine-tune a VLA policy with a calibrated critic and reports real-world Franka success rising from 45.0% under behavior cloning to 98.3% after fine-tuning, with no human intervention during the online stage. PhysReflect-VLA adds execution-time feasibility checks and correction after observed state mismatches, giving smaller but consistent real-robot gains on long-horizon tasks.

#### Sources
- [In-Context World Modeling for Robotic Control](../Inbox/2026-06-24--in-context-world-modeling-for-robotic-control.md): ICWM summary details active probing, context clips, LIBERO gains, and real-robot tests under unseen viewpoints.
- [FORCE: Efficient VLA Reinforcement Fine-Tuning via Value-Calibrated Warm-up and Self-Distillation](../Inbox/2026-06-24--force-efficient-vla-reinforcement-fine-tuning-via-value-calibrated-warm-up-and-self-distillation.md): FORCE summary gives the online fine-tuning recipe and simulation plus real-world success-rate gains.
- [PhysReflect-VLA: Physical Feasibility and Self-Reflective Regulation for Reliable Vision-Language-Action Policies](../Inbox/2026-06-25--physreflect-vla-physical-feasibility-and-self-reflective-regulation-for-reliable-vision-language-action-policies.md): PhysReflect-VLA summary describes runtime feasibility scoring and corrective reflection on real-robot manipulation tasks.

### Geometry and action consequences
Geometry is being added as an execution signal, not only as a visual feature. Reflective VLA stores observation-action-consequence triplets so the policy can infer camera calibration, actuation bias, and robot setup effects at inference time. G3VLA injects camera intrinsics and extrinsics into visual tokens through ray embeddings, projective positional encoding, and cross-view fusion while keeping the base action pathway. Both lines point to the same practical need: a robot policy has to know how its own actions change the scene under the current camera and embodiment.

#### Sources
- [Reflective VLA: In-Context Action Consequences Make VLAs Generalize](../Inbox/2026-06-23--reflective-vla-in-context-action-consequences-make-vlas-generalize.md): Reflective VLA summary explains observation-action-consequence triplets and reports gains under LIBERO distribution shifts.
- [G$^3$VLA: Geometric inductive bias for Vision-Language-Action Models](../Inbox/2026-06-23--g-3-vla-geometric-inductive-bias-for-vision-language-action-models.md): G3VLA summary details camera-aware visual tokens and reported gains on LIBERO, RoboCasa24, RoboTwin2.0, and real-world pouring.

### Safety as a trajectory metric
Safety work is getting more diagnostic. LIBERO-Safety tests whether VLA policies can complete manipulation without unsafe contact or unsafe instruction following, across 75 tasks and 19,664 screened collision-free demonstrations. ForesightSafety-VLA scores each rollout as safe success, unsafe success, safe failure, or unsafe failure, then adds process metrics such as cumulative safety cost and risk exposure time. The important evidence is that task success can hide risky motion: ForesightSafety-VLA reports unsafe success even for the strongest listed baseline, while LIBERO-Safety shows large drops on harder physical-safety levels.

#### Sources
- [LIBERO-Safety: A Comprehensive Benchmark for Physical and Semantic Safety in Vision-Language-Action Models](../Inbox/2026-06-22--libero-safety-a-comprehensive-benchmark-for-physical-and-semantic-safety-in-vision-language-action-models.md): LIBERO-Safety summary provides task count, dataset size, safety suites, and baseline failure details.
- [ForesightSafety-VLA: A Unified Diagnostic Safety Benchmark for Vision-Language-Action Models](../Inbox/2026-06-25--foresightsafety-vla-a-unified-diagnostic-safety-benchmark-for-vision-language-action-models.md): ForesightSafety-VLA summary gives rollout outcome categories, process metrics, and baseline unsafe-success rates.

### Action data and new skills
The week also shows more work on making action supervision cheaper and more reusable. InSight segments existing demonstrations into named primitives, lets a vision-language model choose missing primitive attempts, and folds successful robot rollouts back into the VLA. It reports 92% twist success and 96% pour success on real xArm tasks after adding 20 successful acquired primitive episodes for each skill. LA4VLA takes a data-first route: it derives 33,116 language-action episodes from DROID and pretrains policies on instruction-conditioned motion without images, improving a 1B-parameter VLA on simulated and real-world tasks.

#### Sources
- [InSight: Self-Guided Skill Acquisition via Steerable VLAs](../Inbox/2026-06-23--insight-self-guided-skill-acquisition-via-steerable-vlas.md): InSight summary gives the primitive segmentation loop, target-skill acquisition process, and real-robot results.
- [LA4VLA: Learning to Act without Seeing via Language-Action Pretraining](../Inbox/2026-06-25--la4vla-learning-to-act-without-seeing-via-language-action-pretraining.md): LA4VLA summary describes the 33,116 language-action episodes and reported gains from mixed language-action and VLA pretraining.
