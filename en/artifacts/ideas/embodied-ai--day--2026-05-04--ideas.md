---
kind: ideas
granularity: day
period_start: '2026-05-04T00:00:00'
period_end: '2026-05-05T00:00:00'
run_id: 200f4e14-b6d3-4f91-8594-ac2c0258ec2b
status: succeeded
topics:
- robotics
- vision-language-action models
- robot data
- inference latency
- simulation augmentation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action-models
- topic/robot-data
- topic/inference-latency
- topic/simulation-augmentation
language_code: en
pass_output_id: 131
pass_kind: trend_ideas
upstream_pass_output_id: 130
upstream_pass_kind: trend_synthesis
---

# VLA evaluation gates

## Summary
Robot manipulation teams can now test VLA claims with more concrete gates: per-step latency under skipped backbone calls, stale-observation success under delayed action chunks, targeted simulation-video augmentation for visual variation, and reproducible baselines from released MolmoAct2 weights and datasets.

## Latency and stale-observation test bench for VLA action chunks
Robot teams evaluating a VLA policy should add a delay sweep to their normal task-success tests. The test should record end-to-end milliseconds per control step, VLM backbone call frequency, action chunk length, and success at fixed delays such as d=0, 2, 4, 8, 15, and 20. This catches a failure mode that single success-rate tables hide: the robot may keep moving while the next action chunk was computed from an old observation.

Two current papers give useful baselines for this check. Latent Bridge reports near-synchronous LIBERO success while cutting GR00T-N1.6-3B from 90 ms to 49 ms per step and pi_0.5 from 76 ms to 46 ms by predicting feature or KV-cache deltas between full VLM calls. The asynchronous-inference benchmark shows a separate control problem: at LIBERO delay d=20, A2C2 reaches about 58% success while a naive asynchronous baseline is around 10–12%. A practical adoption gate is to run the candidate policy through both measurements before any real-robot trial: latency with skipped backbone calls, then task success under delayed action chunks.

### Sources
- [Latent Bridge: Feature Delta Prediction for Efficient Dual-System Vision-Language-Action Model Inference](../Inbox/2026-05-04--latent-bridge-feature-delta-prediction-for-efficient-dual-system-vision-language-action-model-inference.md): Latent Bridge reports reduced per-step latency and close task-success retention for GR00T-N1.6-3B and pi_0.5.
- [Understanding Asynchronous Inference Methods for Vision-Language-Action Models](../Inbox/2026-05-04--understanding-asynchronous-inference-methods-for-vision-language-action-models.md): The asynchronous-inference benchmark compares VLA delay methods and reports success rates under increasing action-chunk delays.
- [Understanding Asynchronous Inference Methods for Vision-Language-Action Models](../Inbox/2026-05-04--understanding-asynchronous-inference-methods-for-vision-language-action-models.md): The paper describes why synchronous execution lowers control frequency and naive asynchronous execution creates stale-observation and chunk-boundary failures.

## Coreset simulation-video augmentation for layout and instruction variation
Teams with simulation trajectories can test a small, targeted video-transfer pass before collecting more real robot data. The concrete workflow is to select a coreset using action-prediction loss and visual diversity, generate realistic variants that preserve the same action trajectory, then train the VLA policy on the mixed data. The validation set should include changed object layouts, textures, lighting, and language instructions.

Seeing Realism from Simulation gives a useful scale for the first experiment. A 10% augmented coreset raised RoboTwin 2.0 Hard multi-task success for RDT-1B from 23.0% to 31.0%, and LIBERO-Plus pi_0 improved from 42.7% to 47.8%, with larger gains on object layout and instruction changes. The same paper reports small drops on standard LIBERO, so the check should target deployments where train and test visuals differ enough to matter.

### Sources
- [Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation](../Inbox/2026-05-04--seeing-realism-from-simulation-efficient-video-transfer-for-vision-language-action-data-augmentation.md): The summary describes the video-transfer pipeline, coreset selection method, and reported gains on RoboTwin 2.0 and LIBERO-Plus.
- [Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation](../Inbox/2026-05-04--seeing-realism-from-simulation-efficient-video-transfer-for-vision-language-action-data-augmentation.md): The abstract states the method converts simulated VLA videos into realistic training videos while preserving task semantics and action trajectories.
- [Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation](../Inbox/2026-05-04--seeing-realism-from-simulation-efficient-video-transfer-for-vision-language-action-data-augmentation.md): The paper describes preserving task semantics and action trajectories while diversifying the visual environment.

## Reproducible local baseline using MolmoAct2 weights and robot datasets
Labs comparing closed or partially released robot policies can now build a local baseline around MolmoAct2. The minimum useful workflow is to run the released model and code on a small set of local tasks, then fine-tune or filter from the released SO-100/101, DROID, or BimanualYAM data sources using the same evaluation script. This gives teams a check on whether their robot, cameras, and task mix benefit from the open model before they spend time collecting a large local dataset.

MolmoAct2 is relevant because the release includes model weights, code, and training data, including 720 hours of bimanual YAM trajectories, 38,059 SO-100/101 episodes, and 74,604 filtered DROID successful episodes. The paper also names deployment blockers that local teams already face: costly hardware assumptions, latency from reasoning-heavy policies, and success rates below dependable use. The missing operational step is a reproducibility run on the lab’s own tasks with success rate, intervention count, and control latency logged together.

### Sources
- [MolmoAct2: Action Reasoning Models for Real-world Deployment](../Inbox/2026-05-04--molmoact2-action-reasoning-models-for-real-world-deployment.md): The summary reports released weights, code, training data, model components, dataset sizes, and deployment constraints.
- [MolmoAct2: Action Reasoning Models for Real-world Deployment](../Inbox/2026-05-04--molmoact2-action-reasoning-models-for-real-world-deployment.md): The paper lists the released Hugging Face model, dataset, and code links.
- [MolmoAct2: Action Reasoning Models for Real-world Deployment](../Inbox/2026-05-04--molmoact2-action-reasoning-models-for-real-world-deployment.md): The paper describes practical deployment blockers and the released robot datasets.
