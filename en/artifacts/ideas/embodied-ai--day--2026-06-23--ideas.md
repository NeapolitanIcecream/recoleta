---
kind: ideas
granularity: day
period_start: '2026-06-23T00:00:00'
period_end: '2026-06-24T00:00:00'
run_id: 915a4e16-f949-4b3d-952c-e79655edb831
status: succeeded
topics:
- robotics
- vision-language-action
- world models
- manipulation
- navigation
- synthetic data
- evaluation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/manipulation
- topic/navigation
- topic/synthetic-data
- topic/evaluation
language_code: en
pass_output_id: 309
pass_kind: trend_ideas
upstream_pass_output_id: 308
upstream_pass_kind: trend_synthesis
---

# VLA Policy Support Layers

## Summary
Robot VLA teams can now test three practical support layers around existing policies: a primitive acquisition loop for missing manipulation skills, a geometry path for multi-camera fine-tuning with limited real demos, and step-level scoring for long-horizon task debugging and data filtering.

## Post-deployment primitive acquisition loop for missing manipulation skills
A manipulation team running a VLA in a fixed cell can add a small acquisition loop for skills the policy lacks. The workflow is concrete: segment the existing teleoperation set into named primitives, let a VLM plan a failed new task, identify the missing primitive labels, collect robot rollouts for those primitives with a constrained low-level controller, accept successful segments with a VLM oracle, and retrain the policy so the new primitive is callable later.

InSight gives a workable shape for this. On real xArm twist and pour tasks, it started from 50 pick-and-place demonstrations, added 20 successful acquired primitive episodes, and reported 92% twist success and 96% pour success. It also chained 14 primitives for a twist-then-pour task with no end-to-end demonstrations and reached 80% success. The reported acquisition cost is small enough for a lab trial: 23 trials and 39.7 minutes for 20 twist primitives, and 31 trials and 85.3 minutes for 20 pour primitives.

The same deployment workflow should store the policy’s own observation-action-consequence triplets during rollouts. Reflective VLA shows why that log matters: the triplets expose camera geometry, calibration error, and actuation bias through the visible result of an executed action. On LIBERO-Plus, Reflective VLA reports 87.7% average success against 82.3% for a matched reactive baseline, with the largest listed gain on the Robot shift at 72.9% versus 50.0%. A cheap check is to run the loop on one missing primitive and one camera or robot offset, then measure whether the retrained policy keeps the old pick-and-place skill while improving the new primitive.

### Evidence
- [InSight: Self-Guided Skill Acquisition via Steerable VLAs](../Inbox/2026-06-23--insight-self-guided-skill-acquisition-via-steerable-vlas.md): InSight describes primitive segmentation, VLM-guided missing primitive acquisition, real xArm twist and pour results, long-horizon composition, and acquisition time.
- [Reflective VLA: In-Context Action Consequences Make VLAs Generalize](../Inbox/2026-06-23--reflective-vla-in-context-action-consequences-make-vlas-generalize.md): Reflective VLA describes observation-action-consequence triplets and reports gains under robot, camera, and calibration shifts.

## Calibration-aware visual tokens and 2D waypoint supervision for VLA fine-tuning
A team with calibrated multi-camera manipulation rigs can test a geometry add-on before collecting a much larger action dataset. The build is specific: attach camera-aware visual token modules to the VLA, add ray embeddings from intrinsics, add projective positional encoding from intrinsics and extrinsics, fuse views before the action pathway, and train the added geometry path with point-map or teacher supervision. For synthetic robot videos, route generated data through a 2D end-effector waypoint head and keep action-head training on real demonstrations.

G3VLA supports the camera-calibration half of this workflow. It keeps the pretrained VLA backbone, action space, and imitation objective in place, while adding ray embeddings, PRoPE, and cross-view fusion. On LIBERO with pi0, ground-truth geometric supervision raises average success from 84.6% to 88.1%, with larger gains on Object and Spatial suites. The reported real-world pouring result also improves OOD success from 70.8-75.0% to 83.3-87.5%.

GRA supports the synthetic-video half. It uses generated videos for future 2D end-effector waypoint supervision and trains actions only on real robot demonstrations. On three real Franka pick-and-place tasks, 25 real demos plus 75 generated videos per task reached 68.9% mean success, compared with 61.1% for the real-only matched budget and lower scores for pseudo-action baselines. A practical first test is a three-arm ablation on one task: real-only, real plus pseudo-actions, and real plus generated-video waypoint supervision.

### Evidence
- [G$^3$VLA: Geometric inductive bias for Vision-Language-Action Models](../Inbox/2026-06-23--g-3-vla-geometric-inductive-bias-for-vision-language-action-models.md): G3VLA documents calibration-aware visual tokens, ray embeddings, PRoPE, cross-view fusion, and benchmark and real-world pouring results.
- [Supervise What Survives: Geometry-Guided VLA Adaptation from Synthetic Robot Videos](../Inbox/2026-06-23--supervise-what-survives-geometry-guided-vla-adaptation-from-synthetic-robot-videos.md): GRA documents generated-video 2D waypoint supervision, real-only action training, Franka task results, and pseudo-action comparisons.

## Step-level task oracles with video progress scores for robot run review
Long-horizon VLA evaluations need a run review tool that says which step failed and whether the trajectory contained hesitation or retry behavior. A simulator-side version can start from natural-language task instructions, generate atomic checks such as `Open(fridge)`, `Pick(bottle)`, `Place(bottle, fridge)`, and `Close(fridge)`, and attach those checks to ordered or partially ordered task sequences. A data-review version can score recorded videos for task progress and use the score to filter or weight mixed-quality demonstrations.

MANGO gives the step-localization piece. It builds reusable atomic task libraries, maps each atomic task to simulator functions such as open state, holding state, contact, and spatial relations, and uses Generator, Assessor, and Judge agents to refine executable oracles. The available excerpt reports evaluation on LIBERO_10 and RoboCasa Humanoid Tabletop, with generated oracles detecting a similar number of failures as hand-written symbolic oracles while identifying failed atomic steps and order violations.

World Value Models give the progress-scoring piece for imperfect data. WVM uses a pretrained video world model to estimate task progress from video and language, and introduces Suboptimal-Value-Bench with 800 human-annotated trajectories across 3 embodiments and 15 tasks. It reports 0.05 average Hesitation-RMSE and 0.78 average Retry-VOC, ahead of the listed value-model baselines, and reports better downstream policy learning with WVM-guided AWR and filtered BC across simulated and real tasks. The first useful deployment check is a replay dashboard for one benchmark suite that shows the failed atomic step, a progress curve, and segments tagged as hesitation or retry.

### Evidence
- [MANGO: Automated Multi-Agent Test Oracle Generation for Vision-Language-Action Models](../Inbox/2026-06-23--mango-automated-multi-agent-test-oracle-generation-for-vision-language-action-models.md): MANGO documents automatic generation of fine-grained oracles, atomic task libraries, simulator checks, and failure localization on LIBERO_10 and RoboCasa Humanoid Tabletop.
- [World Value Models for Robotic Manipulation](../Inbox/2026-06-23--world-value-models-for-robotic-manipulation.md): WVM documents video-based task progress scoring, Suboptimal-Value-Bench, hesitation and retry metrics, and downstream policy-learning use.
