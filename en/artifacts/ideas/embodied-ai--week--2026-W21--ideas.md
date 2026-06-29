---
kind: ideas
granularity: week
period_start: '2026-05-18T00:00:00'
period_end: '2026-05-25T00:00:00'
run_id: bfdb3bae-77e6-44b1-88f2-6274001cf2f7
status: succeeded
topics:
- embodied AI
- vision-language-action
- robot manipulation
- 3D grounding
- spatial memory
- real-world evaluation
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/vision-language-action
- topic/robot-manipulation
- topic/3d-grounding
- topic/spatial-memory
- topic/real-world-evaluation
language_code: en
pass_output_id: 199
pass_kind: trend_ideas
upstream_pass_output_id: 198
upstream_pass_kind: trend_synthesis
---

# Physical VLA policy validation

## Summary
VLA teams can add small physical regression benches, target-state logging, and RGB-D geometry paths to check whether manipulation policies still work under real control conditions.

## Local real-robot regression bench for VLA policy releases
A VLA lab can make a small physical benchmark part of every policy release: rebuild the same SO-101 arm setup, run a fixed set of manipulation tasks, and publish per-task success on in-distribution and out-of-distribution scenes. VLA-REPLICA gives enough detail for this workflow to be practical: an SO-101 6-DoF arm, RealSense D455 top camera, wrist webcam, 32 inch light box, commodity objects, camera overlay tools, AprilTag alignment, fixed lighting, reference images, and predefined placements. The reported setup cost is about $1050, and a new user assembled it in under an hour.

The useful check is simple: train or fine-tune on the same 500 expert demonstrations, run the 90 defined test scenes, and compare against reported baselines such as π₀.₅ at 0.54 average success on the 10 in-distribution tasks. This gives robotics groups a cheap physical gate before claiming that a VLA policy works outside simulation.

### Evidence
- [VLA-REPLICA: A Low-Cost, Reproducible Benchmark for Real-World Evaluation of Vision-Language-Action Models](../Inbox/2026-05-20--vla-replica-a-low-cost-reproducible-benchmark-for-real-world-evaluation-of-vision-language-action-models.md): VLA-REPLICA describes the low-cost hardware setup, 500 demonstrations, 90 test scenes, reproducibility tools, setup time, and baseline success rates.
- [VLA-REPLICA: A Low-Cost, Reproducible Benchmark for Real-World Evaluation of Vision-Language-Action Models](../Inbox/2026-05-20--vla-replica-a-low-cost-reproducible-benchmark-for-real-world-evaluation-of-vision-language-action-models.md): The paper states the motivation for locally executable real-world evaluation and lists accessible off-the-shelf components.

## Target-state tokens logged before robot action prediction
Manipulation teams working on dense boards, bins, or object layouts should require the policy to expose a target state before predicting actions. AVP is a concrete pattern: the VLM predicts visual primitives such as points, boxes, masks, or memory primitives, projects them into visual token space, and conditions a flow-matching action expert. The labels come from end-effector kinematics through camera calibration, so teams can create supervision without hand-labeling every target prompt.

This also gives developers a better failure log. When a run fails, they can inspect whether the model selected the wrong object, chose a bad placement region, or produced a poor motor sequence after a correct target. AVP reports 90.28% average success on Chinese chess manipulation versus 62.67% for π₀.₅, with 0.27 seconds per instruction. SOMA points to the same operational need for partially visible scenes: persistent object memory with semantic and 3D position data cut time-to-grasp across five out-of-vision tasks and raised average success to 28.3% in its real-world ablation.

### Evidence
- [Action with Visual Primitives](../Inbox/2026-05-21--action-with-visual-primitives.md): AVP reports visual primitive tokens before action prediction, calibration-derived supervision, no external online detector or VLM API at inference, and real-robot gains over π₀.₅.
- [Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action](../Inbox/2026-05-21--spatial-memory-for-out-of-vision-manipulation-in-vision-language-action.md): SOMA shows persistent spatial memory for objects outside the current view, with real-world success, fixation, search path, grasp-attempt, and time-to-grasp results.

## RGB-D geometry inside the action decoder for precise manipulation
Teams with RGB-D cameras can test whether geometry belongs inside the action path, not just in a perception preprocessor. PointACT gives one direct build pattern: encode colored point clouds with Point Transformer v3, let action tokens attend to local point windows at multiple scales, then combine those geometry-conditioned action tokens with VLM features. The reported LIBERO average is 96.0%, including a 17.9 point gain over SpatialVLA in the cited table.

GaussianDream offers a training-time variant for teams that want geometry supervision without extra inference modules. It decodes learned prefix tokens into current 3D Gaussian scenes and short-horizon future Gaussian motion during training, using RGB rendering, depth, and pseudo 3D scene-flow losses. At inference, the Gaussian heads are removed and the policy keeps only the learned prefix tokens. The paper reports 98.4% average success on LIBERO, 52.6% on RoboCasa Human-50, and 50.0% in real-robot evaluation. A useful adoption test is to compare grasp-point and spatial-relation failures before and after adding either point-action attention or training-time 3D supervision.

### Evidence
- [PointACT: Vision-Language-Action Models with Multi-Scale Point-Action Interaction](../Inbox/2026-05-20--pointact-vision-language-action-models-with-multi-scale-point-action-interaction.md): PointACT describes direct multi-scale point-cloud interaction with action tokens and reports LIBERO gains over SpatialVLA and EO1.
- [GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation](../Inbox/2026-05-20--gaussiandream-a-feed-forward-3d-gaussian-world-model-for-robotic-manipulation.md): GaussianDream describes training-time 3D Gaussian reconstruction and future prediction, inference with prefix tokens only, and results on LIBERO, RoboCasa Human-50, and real robots.
