---
kind: trend
trend_doc_id: 704
granularity: day
period_start: '2026-06-23T00:00:00'
period_end: '2026-06-24T00:00:00'
topics:
- robotics
- vision-language-action
- world models
- manipulation
- navigation
- synthetic data
- evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-704
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/manipulation
- topic/navigation
- topic/synthetic-data
- topic/evaluation
language_code: en
pass_output_id: 308
pass_kind: trend_synthesis
---

# Robot VLA work is prioritizing deployment feedback, geometry, and world-model scoring

## Overview
This period’s robot papers focus on making vision-language-action (VLA) policies usable after deployment. InSight adds new manipulation primitives through robot rollouts. Reflective VLA records action consequences. G3VLA injects camera calibration into visual tokens. The common emphasis is measurable behavior under new skills, new cameras, and imperfect data.

## Clusters

### Deployment feedback for VLA policies
InSight treats missing robot skills as primitives that can be acquired after the initial demonstration set. It segments existing demonstrations into labeled actions, lets a vision-language model propose missing primitives, collects successful robot rollouts, and retrains the policy. The reported real xArm results are concrete: 92% twist success, 96% pour success, and 80% on a 14-primitive twist-then-pour task without end-to-end demonstrations.

Reflective VLA adds a different feedback path. It stores observation-action-consequence triplets, so the policy can infer camera geometry, calibration error, and actuation bias during deployment. On LIBERO-Plus it reports 87.7% average success against 82.3% for a matched reactive baseline, with the largest listed gain on the Robot shift at 72.9% against 50.0%.

#### Evidence
- [InSight: Self-Guided Skill Acquisition via Steerable VLAs](../Inbox/2026-06-23--insight-self-guided-skill-acquisition-via-steerable-vlas.md): InSight summary, method, and reported simulation and real-robot skill acquisition results.
- [Reflective VLA: In-Context Action Consequences Make VLAs Generalize](../Inbox/2026-06-23--reflective-vla-in-context-action-consequences-make-vlas-generalize.md): Reflective VLA summary, action-consequence context design, and LIBERO-Plus results.

### Geometry and contact signals for manipulation
Several papers add physical structure to robot perception without replacing the base policy. GRA uses generated robot videos only for 2D end-effector waypoint supervision, then trains actions on real demonstrations. With 25 real demos and 75 generated videos per task, it reaches 68.9% mean success on three Franka pick-and-place tasks, compared with 61.1% for the real-only matched budget.

G3VLA inserts camera calibration into VLA visual tokens through ray embeddings, projective positional encoding, and cross-view fusion. On LIBERO with pi0, ground-truth geometry supervision raises average success from 84.6% to 88.1%. NoContactNoWorries extends the same practical theme to dexterous hands by predicting fingertip contact from wrist RGB-D and joint state. On a real LEAP Hand, it reports F1 scores from 0.71 to 0.84 across tested objects.

#### Evidence
- [Supervise What Survives: Geometry-Guided VLA Adaptation from Synthetic Robot Videos](../Inbox/2026-06-23--supervise-what-survives-geometry-guided-vla-adaptation-from-synthetic-robot-videos.md): GRA summary, synthetic-video geometry supervision method, and Franka task results.
- [G$^3$VLA: Geometric inductive bias for Vision-Language-Action Models](../Inbox/2026-06-23--g-3-vla-geometric-inductive-bias-for-vision-language-action-models.md): G3VLA summary, camera-calibrated token design, and LIBERO/RoboCasa/RoboTwin results.
- [NoContactNoWorries: Estimating Contact through Vision and Proprioception for In-Hand Dexterous Manipulation](../Inbox/2026-06-23--nocontactnoworries-estimating-contact-through-vision-and-proprioception-for-in-hand-dexterous-manipulation.md): NoContactNoWorries summary, pseudo-tactile contact prediction setup, and real LEAP Hand scores.

### World models as progress scorers and planners
World-model work in this period is tied to control decisions. World Value Models use a pretrained video world model to estimate task progress in manipulation videos, including hesitation and retry segments. The new Suboptimal-Value-Bench has 800 human-annotated trajectories across 3 embodiments and 15 tasks. WVM reports 0.05 average Hesitation-RMSE and 0.78 Retry-VOC, ahead of the listed value-model baselines.

NavWM applies future prediction to visual navigation. It predicts multiple candidate paths and the future images for those paths, then uses that foresight for image-goal navigation. Across Go Stanford, SCAND, RECON, and HuRoN, its average trajectory error drops to 0.207 from UniWM’s 0.302. Future-frame PSNR reaches 17.340, and seen-environment navigation success rises from 66% to 72%.

#### Evidence
- [World Value Models for Robotic Manipulation](../Inbox/2026-06-23--world-value-models-for-robotic-manipulation.md): WVM summary, Suboptimal-Value-Bench details, and value-estimation results.
- [NavWM: A Unified Navigation World Model for Foresight-Driven Planning](../Inbox/2026-06-23--navwm-a-unified-navigation-world-model-for-foresight-driven-planning.md): NavWM summary, candidate trajectory and future-image method, and navigation metrics.

### Step-level evaluation for robot tasks
MANGO targets a practical weakness in VLA testing: final-state checks often hide the step where a long-horizon task failed. It builds atomic task libraries from natural-language instructions, maps steps such as open, pick, place, and close to simulator checks, and uses Generator, Assessor, and Judge agents to refine executable oracles.

The evidence is more diagnostic than benchmark-heavy. The paper evaluates on LIBERO_10 and RoboCasa Humanoid Tabletop, and reports that generated oracles detect a similar number of failures as hand-written symbolic oracles while localizing failed atomic steps and order violations. Exact precision, recall, and runtime numbers are absent from the available excerpt.

#### Evidence
- [MANGO: Automated Multi-Agent Test Oracle Generation for Vision-Language-Action Models](../Inbox/2026-06-23--mango-automated-multi-agent-test-oracle-generation-for-vision-language-action-models.md): MANGO summary, multi-agent oracle-generation method, and reported benchmark coverage.
