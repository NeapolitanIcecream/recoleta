---
kind: ideas
granularity: week
period_start: '2026-06-01T00:00:00'
period_end: '2026-06-08T00:00:00'
run_id: 95a6ffb5-b05a-4f1b-af52-1b717666af9a
status: succeeded
topics:
- robotics
- vision-language-action
- 3D grounding
- world models
- policy evaluation
- action representation
- robot adaptation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/3d-grounding
- topic/world-models
- topic/policy-evaluation
- topic/action-representation
- topic/robot-adaptation
language_code: en
pass_output_id: 265
pass_kind: trend_ideas
upstream_pass_output_id: 264
upstream_pass_kind: trend_synthesis
---

# Robot Policy Interface Calibration

## Summary
Robot VLA teams can make progress by changing the control interface and evaluation workflow around existing policies. The most practical moves are a voxel heatmap action head for low-data manipulation tuning, closed-loop world-model screening for VLA checkpoints, and 3D coordinate alignment before training on mixed robot datasets.

## Voxel heatmap action heads for low-data manipulation fine-tuning
Small end-effector errors still decide many manipulation rollouts. ActionMap gives VLA teams a concrete retrofit to test: replace the native continuous action decoder with a voxel heatmap head over translation, rotation, and gripper commands, then decode continuous actions with top-k soft argmax.

The build is narrow enough for an ablation inside an existing OpenVLA-OFT or pi0.5 training run. Keep the backbone and dataset fixed, train the heatmap head against Gaussian blobs over the action grid, and compare grasp-position error plus task success against the current L1 or flow-matching head. The ActionMap results justify that check: on LIBERO with OpenVLA-OFT, the average rose from 89.1% to 97.3% at matched training steps. With only 43 LIBERO-Spatial demonstrations, it reached 93.2% against 67.2% for the L1 head. On real Franka tasks, it completed 20 of 30 trials against 7 of 30 for the regression head.

This is most useful for teams blocked by scarce demonstrations or millimeter-scale miss rates on grasping, sweeping, and insertion. The cheap validation is a per-task head swap on the current policy, with no backbone change, and a real-robot check that reports both success rate and end-effector error.

### Sources
- [ActionMap: Robot Policy Learning via Voxel Action Heatmap](../Inbox/2026-06-05--actionmap-robot-policy-learning-via-voxel-action-heatmap.md): Summarizes ActionMap's drop-in voxel heatmap head, LIBERO gains, low-data result, and real Franka trial counts.
- [ActionMap: Robot Policy Learning via Voxel Action Heatmap](../Inbox/2026-06-05--actionmap-robot-policy-learning-via-voxel-action-heatmap.md): Confirms the heatmap head directly replaces existing VLA action decoders and reports matched-step LIBERO improvements.

## Closed-loop world-model evaluation for VLA checkpoint screening
Robot evaluation teams can add a closed-loop imagined rollout stage before committing hardware time to every VLA checkpoint. PiL-World shows the specific workflow: freeze the VLA policy, let it predict an action chunk, use a world model to generate the next synchronized multi-view observation, feed the terminal generated observation back into the policy, and repeat.

The operational value is checkpoint triage. Real rollouts are slow because they need safe execution, resets, and repeated trials. PiL-World reduced the average gap between imagined and real success rates on three real dual-arm tasks from 63.2% with Ctrl-World to 12.0%, and reported a 0.94 Pearson correlation between real and imagined success rates across task-checkpoint settings. For Stack Bowls at a 40k-step checkpoint, real success was 96.7% and PiL-World estimated 92.5%.

A practical adoption path is to calibrate the world model on a small set of real successful and failed trajectories for the target cell, then use imagined rollouts to rank checkpoints and task variants. Hardware trials still remain the authority for release, but the screening budget can focus on checkpoints whose closed-loop rollouts preserve scene state, gripper motion, and multi-view consistency.

### Sources
- [PiL-World: A Chunk-Wise World Model for VLA Policy-in-the-Loop Evaluation](../Inbox/2026-06-04--pil-world-a-chunk-wise-world-model-for-vla-policy-in-the-loop-evaluation.md): Summarizes PiL-World's policy-in-the-loop method, training inputs, real-imagined success gaps, and correlation results.
- [PiL-World: A Chunk-Wise World Model for VLA Policy-in-the-Loop Evaluation](../Inbox/2026-06-04--pil-world-a-chunk-wise-world-model-for-vla-policy-in-the-loop-evaluation.md): Confirms the need for observe-act closed-loop testing and the cost limits of real-robot evaluation.

## 3D coordinate alignment preprocessing for mixed robot manipulation datasets
Teams training one VLA across cameras, robot arms, and dataset conventions should add a preprocessing layer that expresses observations, proprioception, and output actions in a shared 3D frame. Dex-BEV is the clearest template: use camera calibration and depth when available to lift pixels into 3D, project multi-view geometry into a canonical bird’s-eye-view frame, and express actions in that same coordinate system.

The pain is concrete. Mixed robot data contains different camera poses, base frames, action conventions, and execution speeds. Dex-BEV reports 89.9% average success on modified LIBERO camera and pose settings, while the listed 2D baselines fall below 10%. On RoboTwin 2.0 Clean it reaches 76.0%, ahead of the 64.8% 2D ablation. GeoAlign points to a lighter rollout variant for geometry-sensitive tasks: post-train an RGB geometry branch with robot RGB-D data, discard the depth head, and let proprioceptive state query geometry features during action generation. On real ALOHA tasks, GeoAlign reports 78.8% average success against 65.0% for the RGB-only baseline, with transparent-bottle success at 75.0% against 35.0%.

The immediate test is a camera-pose perturbation suite and a small set of transparent, thin, or insertion tasks. If success drops mainly under view changes or local geometry demands, 3D alignment belongs in the data pipeline before adding more demonstrations.

### Sources
- [Dexterity-BEV: Aligning 3D World and Actions for Generalizable Robot Policies Learning](../Inbox/2026-06-01--dexterity-bev-aligning-3d-world-and-actions-for-generalizable-robot-policies-learning.md): Summarizes Dex-BEV's shared 3D coordinate frame, BEV preprocessing, modified LIBERO generalization, and RoboTwin results.
- [GeoAlign: Beyond Semantics with State-Guided Spatial Alignment in VLA Models](../Inbox/2026-06-02--geoalign-beyond-semantics-with-state-guided-spatial-alignment-in-vla-models.md): Summarizes GeoAlign's RGB-derived geometry features, proprioceptive querying, real ALOHA gains, and transparent-object result.
