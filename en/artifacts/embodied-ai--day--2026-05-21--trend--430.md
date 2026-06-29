---
kind: trend
trend_doc_id: 430
granularity: day
period_start: '2026-05-21T00:00:00'
period_end: '2026-05-22T00:00:00'
topics:
- vision-language-action
- robot manipulation
- spatial grounding
- runtime verification
- world models
- autonomous driving
run_id: materialize-outputs
aliases:
- recoleta-trend-430
tags:
- recoleta/trend
- topic/vision-language-action
- topic/robot-manipulation
- topic/spatial-grounding
- topic/runtime-verification
- topic/world-models
- topic/autonomous-driving
language_code: en
pass_output_id: 190
pass_kind: trend_synthesis
---

# VLA work now judges policies by grounding, memory, and action checks

## Overview
Vision-language-action (VLA) research dominates this period. CrossVLA, AVP, and SOMA make the current emphasis clear: policy quality is being measured through post-training gains, explicit spatial grounding, persistent memory, latency, and closed-loop execution outcomes.

## Clusters

### Explicit spatial grounding for manipulation
Several robot papers add intermediate target signals between language and motor control. AVP makes the vision-language model output visual primitives before action prediction, then feeds those tokens to a flow-matching action expert. On Chinese chess manipulation, it reports 90.28% average success versus 62.67% for π₀.₅, with 0.27 seconds per instruction.

GesVLA handles a different source of ambiguity: human pointing. It turns wrist and index-finger keypoints into gesture tokens and combines them with language and scene perception. Across three real-robot tasks, success reaches 83.3%, compared with 31.7% for a text-only VLA. SOMA adds persistent spatial memory for objects outside the current camera view, using head-camera scans and memory tokens with semantic and 3D position data. Its gains are smaller in success rate, but it cuts target search time and grasp attempts across out-of-vision tasks.

#### Evidence
- [Action with Visual Primitives](../Inbox/2026-05-21--action-with-visual-primitives.md): AVP architecture and real-robot success, latency, and ablation results.
- [GesVLA: Gesture-Aware Vision-Language-Action Model Embedded Representations](../Inbox/2026-05-21--gesvla-gesture-aware-vision-language-action-model-embedded-representations.md): GesVLA gesture-token design and real-robot success rates.
- [Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action](../Inbox/2026-05-21--spatial-memory-for-out-of-vision-manipulation-in-vision-language-action.md): SOMA spatial memory method and out-of-vision manipulation results.

### Scene state and latent futures inside action systems
A second group works on the state that policies use after the first observation. EvoScene-VLA carries a recurrent scene prefix across control calls and predicts future scene tokens with the action chunk. On 31 RoboTwin tasks, it raises average success to 89.1% in fixed scenes and 88.5% with randomized layouts.

LVDrive applies a similar idea to camera-only autonomous driving. It predicts future scene features in latent space and uses them to refine the trajectory, reaching 80.71 Driving Score and 58.26% Success Rate on Bench2Drive. The TRM paper shows a related planning issue: a latent world model may contain the right state, while the terminal cost ranks candidates poorly. Replacing raw latent distance with a learned reachability metric raises hard TwoRoom success for LeWM from 7.0% to 97.0%.

#### Evidence
- [EvoScene-VLA: Evolving Scene Beliefs Inside the Action Decoder for Chunked Robot Control](../Inbox/2026-05-21--evoscene-vla-evolving-scene-beliefs-inside-the-action-decoder-for-chunked-robot-control.md): EvoScene-VLA recurrent scene prefix and RoboTwin success results.
- [LVDrive: Latent Visual Representation Enhanced Vision-Language-Action Autonomous Driving Model](../Inbox/2026-05-21--lvdrive-latent-visual-representation-enhanced-vision-language-action-autonomous-driving-model.md): LVDrive latent future prediction method and Bench2Drive metrics.
- [Beyond Euclidean Proximity: Repairing Latent World Models with Horizon-Matched Trajectory Reachability Metrics](../Inbox/2026-05-21--beyond-euclidean-proximity-repairing-latent-world-models-with-horizon-matched-trajectory-reachability-metrics.md): TRM learned reachability metric and TwoRoom planning gains.

### Post-training and action verification
CrossVLA treats VLA adaptation as an empirical systems problem. It adapts Direct Preference Optimization (DPO) to both autoregressive action-token policies and flow-matching continuous-action policies. On OpenVLA across LIBERO’s four suites, DoRA+DPO reaches 73.2% mean success versus 62.75% for supervised fine-tuning. Its latency breakdown also matters: π₀.₅ spends about 78.6% of sample-actions time in the denoising loop, so prefix key-value caching is a weak target.

Pre-VLA adds a runtime checker before execution or world-model rollout. It predicts action validity and critic-derived advantage for candidate action chunks. On LIBERO, it reports 0.9542 validity accuracy and raises RynnVLA-002 average closed-loop success from 30.79% to 37.62%, with 183.9 ms verification per chunk.

#### Evidence
- [CrossVLA: Cross-Paradigm Post-Training and Inference Optimization for Vision-Language-Action Models](../Inbox/2026-05-21--crossvla-cross-paradigm-post-training-and-inference-optimization-for-vision-language-action-models.md): CrossVLA DPO results, latency analysis, and caching negative result.
- [Pre-VLA: Preemptive Runtime Verification for Reliable Vision-Language-Action and World-Model Rollouts](../Inbox/2026-05-21--pre-vla-preemptive-runtime-verification-for-reliable-vision-language-action-and-world-model-rollouts.md): Pre-VLA runtime verification method, LIBERO accuracy, success, and latency.

### Safety-critical VLA remains more proposal than evidence
The endoscopic surgery copilot paper extends VLA reasoning into a high-risk setting, but its evidence is architectural and clinical rather than experimental. It defines a Level of Autonomy 2–3 assistant that can generate options, monitor the surgical scene, and execute bounded low-level maneuvers under surgeon authority. The proposed system fuses endoscopic video with preoperative and intraoperative signals, including CT/MRI priors, ultrasound, OCT, tracking, and force proxies.

The paper is useful as a requirements document. It names specific subtasks such as traction, dissection, hemostasis, smoke response, and bleeding-point localization. It also sets a sub-second response target. It reports no benchmark, runtime measurement, clinical trial, or success rate, so it should be read as a safety specification for future VLA work rather than a deployed result.

#### Evidence
- [How can reasoning capability empower the AI copilot robot in endoscopic surgery](../Inbox/2026-05-21--how-can-reasoning-capability-empower-the-ai-copilot-robot-in-endoscopic-surgery.md): Surgical copilot autonomy level, proposed VLA design, use cases, and lack of quantitative results.
