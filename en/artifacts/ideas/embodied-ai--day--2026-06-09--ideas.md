---
kind: ideas
granularity: day
period_start: '2026-06-09T00:00:00'
period_end: '2026-06-10T00:00:00'
run_id: 7b3c03ed-ff97-4d7b-8a00-4fcc1d105f84
status: succeeded
topics:
- robot manipulation
- VLA policies
- real-robot evaluation
- occlusion
- dexterous manipulation
- sim-real correlation
tags:
- recoleta/ideas
- topic/robot-manipulation
- topic/vla-policies
- topic/real-robot-evaluation
- topic/occlusion
- topic/dexterous-manipulation
- topic/sim-real-correlation
language_code: en
pass_output_id: 271
pass_kind: trend_ideas
upstream_pass_output_id: 270
upstream_pass_kind: trend_synthesis
---

# Real-world robot control reliability

## Summary
Robot manipulation work in this window points to three practical changes: evaluate wrist-view policies with fixed physical rollout protocols, add RGB-D action checking before execution, and train dexterous-hand policies from human video through shared hand keypoints and contact labels.

## Fixed real-robot rollout protocols for UMI-style wrist-view policies
Teams training UMI-style tabletop policies should add a repeatable physical evaluation loop before comparing model versions. UMI-Bench 1.0 gives a usable pattern: fixed workstation setup, wrist-view RGB inputs, scene reset images, scene JSON, rollout logging, human scoring, Full Success Rate, and a 0 to 100 Progress Score. The useful detail is the split by seen and unseen factors, because it separates failures caused by layout, pose, dynamics, object identity, and appearance.

This matters for labs that currently compare policies after ad hoc resets or camera changes. UMI-Bench reports that π0.5 leads its three-model comparison with a 55.84 mean Overall Score, but the more operational result is the drop in Progress Score: 59.62 in Seen/Seen episodes, 45.33 under position, layout, pose, or dynamics shifts, and 40.19 under combined shifts. A policy release checklist can copy this structure with 20 to 50 rollouts per task, saved reset images, factor labels, and per-rollout failure notes. The same evaluation table can reserve simulation for ranking checks only when it preserves real-world ordering; the sim-real study found REALM had the best policy-ranking correlation among the tested simulators, with Spearman 0.700 before simulator post-training and 0.875 after it.

### Sources
- [UMI-Bench 1.0: An Open and Reproducible Real-World Benchmark for Tabletop Robotic Manipulation with UMI Data](../Inbox/2026-06-09--umi-bench-1-0-an-open-and-reproducible-real-world-benchmark-for-tabletop-robotic-manipulation-with-umi-data.md): UMI-Bench specifies the workstation, reset, logging, scoring, task-factor splits, and reported degradation under physical shifts.
- [A Practical Recipe Towards Improving Sim-and-Real Correlation for VLA Evaluation](../Inbox/2026-06-09--a-practical-recipe-towards-improving-sim-and-real-correlation-for-vla-evaluation.md): The sim-real study reports policy-ranking correlation metrics and shows why simulation should be checked against real rollout decisions.

## RGB-D action verification before VLA policy execution
VLA manipulation deployments can add a pre-execution action verifier around an existing policy. The verifier samples several candidate 7D actions from the frozen policy, back-projects depth into 3D scene coordinates, scores contact and clearance geometry, and executes the highest-ranked candidate. This is a concrete fit for teams seeing missed grasps, small pose errors, collisions, or wrong subgoal progress after one-shot policy outputs.

VeriSpace is the clearest implementation reference. With OpenVLA on SimplerEnv-WidowX, average success rose from 37.0% to 55.0% across four tasks and 50 trials per task. The largest listed task gain was Stack Cubes, from 28.0% to 62.0%. A cheap adoption test is to log the top five candidate actions, the verifier score, depth-derived contact features, and the executed outcome on tasks where failure changes the scene enough to block recovery. If the verifier only helps on easy scenes, it should stay as a diagnostic tool; if it reduces first-action physical mistakes, it belongs in the control loop.

### Sources
- [VeriSpace: Spatially Grounded Action Verification for Vision-Language-Action Models](../Inbox/2026-06-09--verispace-spatially-grounded-action-verification-for-vision-language-action-models.md): VeriSpace describes candidate action sampling, RGB-D spatial scoring, pairwise ranking, and the reported success gains.
- [VeriSpace: Spatially Grounded Action Verification for Vision-Language-Action Models](../Inbox/2026-06-09--verispace-spatially-grounded-action-verification-for-vision-language-action-models.md): The paper frames the operational failure mode: one-shot action prediction can cause grasp failure, collision, or wrong task progression.

## Dexterous-hand training from human video with wrist, fingertip, object, and contact labels
Dexterous-hand groups can test a human-video data pipeline before committing weeks to multi-finger teleoperation. Dexterous Point Policy uses six shared 3D hand points, the wrist and five fingertips, plus object points, language, camera pose, and fingertip contact labels. At deployment, inverse kinematics maps the predicted keypoints to robot joints, while contact flags add closing offsets for fingertip force.

The reported gap is large enough to justify a small replication on one pick-and-place task and one tool-use task. Across eight real-robot dexterous tasks, DPP reports 75.0% average success, compared with 3.7% for Point Policy and 1.0% for VITRA. Its ablation assigns a 71.3 percentage point gain to contact prediction over the point-only baseline. The adoption blocker is annotation quality: the workflow needs reliable hand keypoints, object masks, depth or stereo estimates, and contact labels. A first internal test should measure whether the extracted fingertip trajectories and contact flags stay stable across camera angles and object categories before training a full policy.

### Sources
- [Dexterous Point Policy: Learning Point-based Dexterous Hand Policies from Human Demonstrations](../Inbox/2026-06-09--dexterous-point-policy-learning-point-based-dexterous-hand-policies-from-human-demonstrations.md): Dexterous Point Policy reports the six-keypoint representation, human-video-only training setup, contact prediction, and real-robot results.
- [Dexterous Point Policy: Learning Point-based Dexterous Hand Policies from Human Demonstrations](../Inbox/2026-06-09--dexterous-point-policy-learning-point-based-dexterous-hand-policies-from-human-demonstrations.md): The paper states the embodiment gap and the high cost of robot demonstrations for dexterous manipulation.
