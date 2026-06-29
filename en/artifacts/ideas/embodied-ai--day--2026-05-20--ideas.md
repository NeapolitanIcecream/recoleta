---
kind: ideas
granularity: day
period_start: '2026-05-20T00:00:00'
period_end: '2026-05-21T00:00:00'
run_id: bfdb3bae-77e6-44b1-88f2-6274001cf2f7
status: succeeded
topics:
- embodied AI
- vision-language-action
- robot manipulation
- 3D perception
- dexterous hands
- world models
- robot evaluation
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/vision-language-action
- topic/robot-manipulation
- topic/3d-perception
- topic/dexterous-hands
- topic/world-models
- topic/robot-evaluation
language_code: en
pass_output_id: 189
pass_kind: trend_ideas
upstream_pass_output_id: 188
upstream_pass_kind: trend_synthesis
---

# Manipulation Policy Hardware Checks

## Summary
Robot policy teams have enough detail to add three practical checks to their work: a low-cost physical VLA regression station, 3D geometry supervision tied to action prediction, and a direct-joint-sensing test for dexterous hands. Each targets a visible failure mode in manipulation: lab results that do not survive contact, action decoders that miss geometry, and hand controllers that depend on fragile external perception.

## A low-cost physical regression station for VLA policy releases
VLA teams can add a small real-robot station to their release process and use it as a recurring regression test. VLA-REPLICA gives a concrete bill of materials and protocol: an SO-101 6-DoF arm, RealSense D455 top camera, wrist webcam, light box, commodity objects, AprilTag alignment, fixed lighting, reference images, and predefined object placements. The full setup is reported at about $1050, and one user built it in under an hour.

The useful adoption change is a fixed local gate before claiming progress on a new policy or fine-tune. Run the same 10 manipulation tasks, reuse the 500-demonstration adaptation set, and report success across the 50 in-distribution and 40 out-of-distribution scenes. The baseline table also sets expectations: π0.5 leads the tested policies at 0.54 average success in-distribution, while ACT, DiT variants, SmolVLA, X-VLA, and π0 are lower. A team with a new VLA can learn quickly whether a leaderboard gain still works with lighting, camera pose, object placement, and contact on real hardware.

### Evidence
- [VLA-REPLICA: A Low-Cost, Reproducible Benchmark for Real-World Evaluation of Vision-Language-Action Models](../Inbox/2026-05-20--vla-replica-a-low-cost-reproducible-benchmark-for-real-world-evaluation-of-vision-language-action-models.md): VLA-REPLICA specifies the low-cost hardware, 10-task suite, 500 demonstrations, 90 test scenes, reproducibility check, and policy success rates.
- [VLA-REPLICA: A Low-Cost, Reproducible Benchmark for Real-World Evaluation of Vision-Language-Action Models](../Inbox/2026-05-20--vla-replica-a-low-cost-reproducible-benchmark-for-real-world-evaluation-of-vision-language-action-models.md): The paper describes the motivation for a locally executable real-world benchmark and gives the accessible hardware setup.

## 3D geometry checks inside VLA action prediction
Teams training VLAs on RGB-D manipulation data can test whether geometry reaches the action output by adding an explicit 3D path and measuring contact-sensitive failures. PointACT gives one build pattern: encode colored point clouds with Point Transformer v3, let action tokens attend to local point windows at multiple scales, and then combine geometry with VLM features during decoding. GaussianDream gives another test pattern: add training-time 3D Gaussian reconstruction and short-horizon scene-flow prediction, then remove the auxiliary heads at inference and keep the learned prefix tokens for action generation.

The practical check is a controlled ablation on spatial tasks and long-horizon kitchen tasks. Keep the base VLA and training data fixed, add either point-cloud attention in the decoder or 3D Gaussian auxiliary supervision, and compare errors on grasp points, target poses, stacking, unstacking, and spatial relations. PointACT reports 96.0% average success on LIBERO and a 17.9-point gain over SpatialVLA in the same table. GaussianDream reports 98.4% on LIBERO and 52.6% on RoboCasa Human-50 while avoiding test-time Gaussian rendering or future video rollout.

### Evidence
- [PointACT: Vision-Language-Action Models with Multi-Scale Point-Action Interaction](../Inbox/2026-05-20--pointact-vision-language-action-models-with-multi-scale-point-action-interaction.md): PointACT describes point-cloud features connected directly to action tokens and reports LIBERO results and the SpatialVLA comparison.
- [GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation](../Inbox/2026-05-20--gaussiandream-a-feed-forward-3d-gaussian-world-model-for-robotic-manipulation.md): GaussianDream describes training-time 3D Gaussian reconstruction, future scene-flow supervision, inference-time removal of auxiliary heads, and reported LIBERO and RoboCasa results.

## Direct joint-sensor evaluation for tendon-driven dexterous hands
Dexterous-hand teams using tendon-driven hardware can run a focused sensing upgrade before adding more cameras or tactile sensors. The concrete test is to install direct joint angle sensing, train a student controller on joint position and velocity histories, and compare it with motor-encoder-only and vision-based baselines on continuous cube rotation. Proprioceptive Transformer uses a teacher trained with privileged object pose in Isaac Lab, then distills control into a policy that receives joint histories, previous action, previous command, and goal command.

The reported hardware result makes the check worth doing on real hands. On a 55 mm cube, the direct-joint-sensing policy reaches 11.83 RPM with 100% rotation accuracy, 100% drop-free success, and zero drops across three 60-second trials. The same paper reports a 26.8% speed gain over the motor-encoder version on the 55 mm cube. For teams fighting cable stretch, backlash, occlusion, and camera calibration, this is a measurable retrofit: add direct joint sensing, train the history model, and score RPM, drops, and rotation accuracy against the existing controller.

### Evidence
- [Learning Robust Dexterous In-Hand Manipulation from Joint Sensors with Proprioceptive Transformer](../Inbox/2026-05-20--learning-robust-dexterous-in-hand-manipulation-from-joint-sensors-with-proprioceptive-transformer.md): Proprioceptive Transformer specifies the joint-history student policy, direct joint sensing on the ORCA hand, and the cube-rotation results against baselines.
- [Learning Robust Dexterous In-Hand Manipulation from Joint Sensors with Proprioceptive Transformer](../Inbox/2026-05-20--learning-robust-dexterous-in-hand-manipulation-from-joint-sensors-with-proprioceptive-transformer.md): The abstract frames joint-only dexterous manipulation and the teacher-student design using only joint sensing feedback.
