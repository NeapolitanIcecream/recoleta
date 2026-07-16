---
kind: trend
trend_doc_id: 471
granularity: day
period_start: '2026-05-28T00:00:00'
period_end: '2026-05-29T00:00:00'
topics:
- vision-language-action
- robot manipulation
- real-robot evaluation
- dexterous control
- spatial reasoning
- inference efficiency
run_id: materialize-outputs
aliases:
- recoleta-trend-471
tags:
- recoleta/trend
- topic/vision-language-action
- topic/robot-manipulation
- topic/real-robot-evaluation
- topic/dexterous-control
- topic/spatial-reasoning
- topic/inference-efficiency
language_code: en
pass_output_id: 236
pass_kind: trend_synthesis
---

# Robot VLA work is being judged on control speed, task transfer, and real-robot evidence

## Overview
The day’s research is concentrated on deployable robot control. Vision-language-action (VLA) models get larger task coverage, faster inference paths, richer spatial grounding, and more real-robot checks. Qwen-VLA carries the broadest unification claim, BORA gives the clearest dexterous adaptation result, and PhAIL questions how real-robot success should be measured.

## Findings

### Generalist VLA policies
Qwen-VLA is the scale-and-unification anchor. It uses Qwen3.5-4B for vision-language understanding and a DiT flow-matching action decoder for continuous actions. The model reads robot descriptions, images, and instructions, then predicts action or trajectory chunks across manipulation, navigation, and trajectory prediction. Reported results span LIBERO, Simpler-WidowX, RoboTwin, R2R, RxR, ALOHA out-of-distribution trials, and DOMINO dynamic manipulation.

VLA-Pro takes a modular route to transfer. It stores task-specific LoRA adapters with structured procedural states, retrieves related memories at inference, and fuses the weights for the current action chunk. The gains are large in the reported settings: π0.5 real-world success on six held-out UR7e tasks rises from 5.8% to 65.0%, and RoboTwin results improve across X-VLA, RDT, and π0.5 backbones.

#### Sources
- [Qwen-VLA: Unifying Vision-Language-Action Modeling across Tasks, Environments, and Robot Embodiments](../Inbox/2026-05-28--qwen-vla-unifying-vision-language-action-modeling-across-tasks-environments-and-robot-embodiments.md): Qwen-VLA summary, architecture, training setup, and benchmark results.
- [VLA-Pro: Cross-Task Procedural Memory Transfer for Vision-Language-Action Models](../Inbox/2026-05-28--vla-pro-cross-task-procedural-memory-transfer-for-vision-language-action-models.md): VLA-Pro procedural memory method and transfer results.

### Real-world adaptation and human intent
BORA focuses on dexterous hands, where contact errors build up quickly. It trains an action-conditioned critic offline, then freezes the base VLA during deployment and learns a small residual actor with human interventions. On five Franka arm plus 12-DoF hand tasks, BORA-Full reaches 86.0% average success, compared with 53.0% for the consistency-policy base. On unseen objects it reaches 70.0%, compared with 27.0% for the same base.

Gaze2Act treats human gaze as a control signal for target choice and part-level interaction. It maps first-person gaze into the robot camera view, draws mask and heatmap cues on the robot observation, and adds a gaze branch to the GROOT N1.5 diffusion action head. On a Unitree G1 humanoid, it reports 83.5% task success across 15 main real-robot tasks, with stronger results than language-only and language-grounded spatial baselines.

#### Sources
- [BORA: Bridging Offline Reinforcement Learning and Online Residual Adaptation for Real-World Dexterous VLA Models](../Inbox/2026-05-28--bora-bridging-offline-reinforcement-learning-and-online-residual-adaptation-for-real-world-dexterous-vla-models.md): BORA offline-to-online residual adaptation method and real-world dexterous results.
- [Gaze2Act: Gaze-Conditioned Vision-Language-Action Policies for Interactive Robot Manipulation](../Inbox/2026-05-28--gaze2act-gaze-conditioned-vision-language-action-policies-for-interactive-robot-manipulation.md): Gaze2Act gaze-conditioned policy design and Unitree G1 evaluation.

### Perception and inference efficiency
VisualThink-VLA adds sparse visual evidence tokens for object boxes, edges, motion, and relations. The router chooses evidence channels per decision step while the VLA backbone stays frozen. On BridgeData V2, it reports 89.49% success at 0.367 seconds per step, compared with ECoT at 85.09% and 8.377 seconds.

3DVLA adds 3D spatial memory, object-centric instance tokens, and occlusion completion to pretrained VLA policies. Its gains are modest on LIBERO-Plus but broader on RoboTwin 2.0, where π0+3DVLA improves Easy success from 46.4% to 54.5% and Hard success from 16.3% to 23.2%.

ElegantVLA reduces compute by learning when to recompute the vision encoder, language model, and action head. In GR00T-based real-world tests, it reports a 2.18× compute reduction, control frequency rising from 13.8 Hz to 26.3 Hz, and average success rising from 61.67% to 65.00%.

#### Sources
- [VisualThink-VLA: Visual Intermediate Reasoning for Effective and Low-Latency Vision-Language-Action Policies](../Inbox/2026-05-28--visualthink-vla-visual-intermediate-reasoning-for-effective-and-low-latency-vision-language-action-policies.md): VisualThink-VLA visual evidence routing and latency-success results.
- [3DVLA: Enhancing Vision-Language-Action Models via 3D Spatial and Instance Understanding](../Inbox/2026-05-28--3dvla-enhancing-vision-language-action-models-via-3d-spatial-and-instance-understanding.md): 3DVLA 3D spatial and instance reasoning results on LIBERO-Plus and RoboTwin 2.0.
- [ElegantVLA: Learning When to Think for Efficient Vision-Language-Action Models](../Inbox/2026-05-28--elegantvla-learning-when-to-think-for-efficient-vision-language-action-models.md): ElegantVLA learned compute scheduling and real-world speed results.

### Evaluation, diagnosis, and confidence
The evaluation papers target failure modes that single success rates miss. PhAIL measures time-to-success distributions on a Franka FR3 and anchors scoring to same-fixture human teleoperation. In its benchmark, the best evaluated VLA is about seven times slower than the human reference by RMST ratio, and no inference model exceeds 19% Human-Relative Throughput on any object.

VLA-Trace probes how VLA policies use image and text during action decoding. On LIBERO-10, π0.5 drops from 93.5% success to 0.0% when image access is removed during generation, while removing text access leaves 39.0% success. OpenVLA shows a different dependency pattern, with text removal dropping success to 0.0% across the reported LIBERO settings.

VLAConf adds calibrated task-success confidence using frozen VLA features and a success-only confidence head. It is designed for online failure anticipation and reports much lower inference cost than ConfidenceVLA on OpenVLA-OFT: 64.9 ms versus 712.9 ms average query time.

#### Sources
- [PhAIL: A Real-Robot VLA Benchmark and Distributional Methodology](../Inbox/2026-05-28--phail-a-real-robot-vla-benchmark-and-distributional-methodology.md): PhAIL real-robot benchmark, time-to-success evaluation, and throughput findings.
- [VLA-Trace: Diagnosing Vision-Language-Action Models through Representation and Behavior Tracing](../Inbox/2026-05-28--vla-trace-diagnosing-vision-language-action-models-through-representation-and-behavior-tracing.md): VLA-Trace modality ablation and representation-behavior diagnostics.
- [VLAConf: Calibrated Task-Success Confidence for Vision-Language-Action Models](../Inbox/2026-05-28--vlaconf-calibrated-task-success-confidence-for-vision-language-action-models.md): VLAConf confidence estimation method and latency/calibration results.
