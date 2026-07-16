---
kind: ideas
granularity: day
period_start: '2026-04-29T00:00:00'
period_end: '2026-04-30T00:00:00'
run_id: 2b5934f0-a60d-4a6a-bb05-ecd0d45a2420
status: succeeded
topics:
- robotics
- world models
- Vision-Language-Action
- 3D generation
- simulation
- social navigation
tags:
- recoleta/ideas
- topic/robotics
- topic/world-models
- topic/vision-language-action
- topic/3d-generation
- topic/simulation
- topic/social-navigation
language_code: en
pass_output_id: 121
pass_kind: trend_ideas
upstream_pass_output_id: 120
upstream_pass_kind: trend_synthesis
---

# Geometry Checks for Robot Training

## Summary
Robot manipulation work now gives teams a concrete way to test whether predicted geometry improves execution: add RGB-D future prediction, end-effector geometry, and contact-region checks to policy evaluations. The related 3D generation work points to a practical asset gate for simulation teams: generated objects need joints, physical parameters, collision geometry, and simulator-compatible files before they are useful for robot training. Outdoor language-grounded navigation is promising, but the available evidence mainly supports a field-test protocol with complete safety and completion logs.

## Contact-region evaluation for RGB-D manipulation policies
Manipulation teams should add a contact-region evaluation slice to VLA policy testing. The useful test cases are tasks where a small 3D error changes the outcome: hanging a mug by its handle, handover, pressing a tool, placing an object through an opening, and moving near obstacles. The evaluation should log success, collisions, missed grasps, contact-point error, end-effector clearance, and whether the model attends to the object region that controls the action.

STARRY gives a concrete design to copy and test. It predicts future depth and end-effector positions, unprojects predicted depth into 3D, computes token distances to the predicted end effector, and uses those distances to bias action-to-video attention. The paper reports 93.82% clean and 93.30% randomized average success on 50 RoboTwin 2.0 bimanual tasks, plus 70.8% average success in real ARX R5 bimanual experiments using 50 demonstrations per task and 20 evaluation rollouts per method. The biggest value is the failure analysis it enables: when a policy misses a handle or collides near an opening, the team can inspect the predicted depth, end-effector path, and attention weights before collecting more demonstrations.

### Sources
- [STARRY: Spatial-Temporal Action-Centric World Modeling for Robotic Manipulation](../Inbox/2026-04-29--starry-spatial-temporal-action-centric-world-modeling-for-robotic-manipulation.md): Describes STARRY’s future depth and end-effector geometry, GASAM attention weighting, benchmark results, and real ARX R5 evaluation.
- [STARRY: Spatial-Temporal Action-Centric World Modeling for Robotic Manipulation](../Inbox/2026-04-29--starry-spatial-temporal-action-centric-world-modeling-for-robotic-manipulation.md): Names contact-sensitive manipulation examples and the failure modes caused by local geometry errors.

## Action-first denoising latency test for world-action policies
Teams adapting video diffusion models for robot control should run a latency test that decodes actions earlier than video. The test is simple: train or fine-tune a model that predicts future RGB-D frames, robot state, and a block of future actions, then compare control latency and task success under different denoising budgets for actions and video. The pass condition is practical, not visual: the robot must produce actions fast enough for closed-loop control while depth and video predictions remain good enough for debugging and planning.

X-WAM is a useful reference implementation. It fine-tunes Wan2.2-TI2V-5B on multi-view robot data, predicts 8 future RGB frames, 8 future states, and 32 future actions, and adds a depth branch without doubling the token sequence. Its Asynchronous Noise Sampling trains video and action noise levels from a coupled distribution so inference can use fewer denoising steps for actions. Reported results include 79.2% average success on RoboCasa across 24 tasks and 90.7% on RoboTwin 2.0 Randomized. A lab can reproduce the most relevant part without matching the full scale: measure milliseconds per action, success rate, and geometric prediction quality as the action denoising budget is reduced.

### Sources
- [Unified 4D World Action Modeling from Video Priors with Asynchronous Denoising](../Inbox/2026-04-29--unified-4d-world-action-modeling-from-video-priors-with-asynchronous-denoising.md): Describes X-WAM’s multi-view RGB-D, state, and action prediction setup, asynchronous denoising, training scale, and benchmark results.
- [Unified 4D World Action Modeling from Video Priors with Asynchronous Denoising](../Inbox/2026-04-29--unified-4d-world-action-modeling-from-video-priors-with-asynchronous-denoising.md): States that X-WAM predicts multi-view RGB-D futures and uses Asynchronous Noise Sampling for efficient action execution.

## Simulator import checks for generated robot-training assets
Simulation teams using generated 3D assets should add an import gate before assets enter robot-training runs. The gate should reject objects that have only shape and texture. A useful generated asset needs valid mesh geometry, collision geometry, joint definitions, joint limits, mass, friction, material behavior where relevant, and export to formats such as URDF, MJCF, or USD. The check should load the asset in the target simulator, execute its joints, drop or push it under physics, and verify that the file can be reused across the team’s training jobs.

The 3D generation survey names the adoption blocker clearly: visual quality does not guarantee physical validity. It defines simulation readiness around geometry, physical parameterization, kinematic executability, and simulator compatibility, and connects generated content to engines and formats including MuJoCo, Isaac Sim, Habitat, AI2-THOR, OmniGibson, PyBullet, ManiSkill3, Genesis, URDF, MJCF, and USD. That turns asset generation into a testable workflow issue for robotics groups. A small validator script and simulator smoke test will catch many failures before policy training consumes bad scenes.

### Sources
- [3D Generation for Embodied AI and Robotic Simulation: A Survey](../Inbox/2026-04-29--3d-generation-for-embodied-ai-and-robotic-simulation-a-survey.md): Defines simulation-ready 3D generation requirements, including geometry, physical parameters, kinematics, and simulator compatibility.
- [3D Generation for Embodied AI and Robotic Simulation: A Survey](../Inbox/2026-04-29--3d-generation-for-embodied-ai-and-robotic-simulation-a-survey.md): Names URDF, MJCF, joint configurations, mass distributions, and friction coefficients as necessary for useful generated assets.
