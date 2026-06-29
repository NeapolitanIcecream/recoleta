---
kind: trend
trend_doc_id: 455
granularity: day
period_start: '2026-05-27T00:00:00'
period_end: '2026-05-28T00:00:00'
topics:
- robot learning
- vision-language-action models
- manipulation
- tactile sensing
- model compression
- autonomous driving safety
run_id: materialize-outputs
aliases:
- recoleta-trend-455
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/manipulation
- topic/tactile-sensing
- topic/model-compression
- topic/autonomous-driving-safety
language_code: en
pass_output_id: 234
pass_kind: trend_synthesis
---

# Vision-language-action papers focus on deployable robot control

## Overview
Vision-language-action (VLA) research in this period is centered on execution: closed-loop planning, reusable skills, tactile force control, and model compression for robots. VERA, PrimitiveVLA, and Ω-QVLA carry the clearest empirical claims, with real-robot or manipulation-suite tests attached to most papers.

## Clusters

### Structured execution for manipulation VLAs
Several papers make VLA policies easier to run as long-horizon controllers. PrimitiveVLA cuts demonstrations into 11 reusable primitives and plans primitive sequences at test time; it reports OpenVLA success rising to 45.50% on LIBERO-90-Novel and pi0.5 success reaching 80.25% on LIBERO-Long. ProgVLA uses a 0.1B-parameter policy with compressed multimodal tokens and progress heads, reaching 91.1% average LIBERO success and 68% real-world success over 100 PiPER-arm trials. A separate probing study finds that frozen VLA features already contain a value-like success signal, then uses a linear probe to select among Pi0.5 action chunks, improving pooled hard-3 success to 42.44% against 31.11% for greedy decoding.

#### Evidence
- [PrimitiveVLA: Learning Reusable Motion Primitives for Efficient and Generalizable Robotic Manipulation](../Inbox/2026-05-27--primitivevla-learning-reusable-motion-primitives-for-efficient-and-generalizable-robotic-manipulation.md): PrimitiveVLA primitive segmentation, inference sequencing, and LIBERO gains.
- [ProgVLA: Progress-Aware Robot Manipulation Skill Learning](../Inbox/2026-05-27--progvla-progress-aware-robot-manipulation-skill-learning.md): ProgVLA compact policy design, progress heads, benchmark results, and real-world trials.
- [What Frozen VLAs Already Know About Success: A Probing Study of Value-Like Structure in Foundation Robot Policies](../Inbox/2026-05-27--what-frozen-vlas-already-know-about-success-a-probing-study-of-value-like-structure-in-foundation-robot-policies.md): Frozen VLA value probes and online Pi0.5 action selection results.

### Video and phase models as closed-loop action sources
VERA keeps planning in video space and trains a robot-specific Jacobian inverse dynamics model to convert generated frame-to-frame motion into actions. The method reports closed-loop simulation success of 70.0% on Allegro-Sim, 94.0% on Panda-Sim, and 92.5% on PushT-Sim, with the same video planner paired to different robot adapters. Mag-VLA applies a related execution idea at microscale: it fine-tunes Qwen2.5-VL-7B for bimanual magnetic microrobot control, predicts task phase, and emits short dual-arm action chunks. In real tests, approach success is 90% across three tasks, while transport success drops with harder paths.

#### Evidence
- [Turning Video Models into Generalist Robot Policies](../Inbox/2026-05-27--turning-video-models-into-generalist-robot-policies.md): VERA video planner, Jacobian inverse dynamics model, and cross-embodiment robot results.
- [Mag-VLA: Vision-Language-Action Model for Bimanual Magnetically Actuated Microrobot Manipulation](../Inbox/2026-05-27--mag-vla-vision-language-action-model-for-bimanual-magnetically-actuated-microrobot-manipulation.md): Mag-VLA phase-aware dual-arm control and real microrobot manipulation results.

### Touch and force enter the success criteria
The tactile papers treat contact quality as part of the control problem. Tabero builds vision-touch-language data by replaying manipulation trajectories in Isaac Lab with tactile sensing, then predicts pose and force targets for a hybrid controller. It reports over 70% lower average grip force under gentle instructions, while tracking peak and average grip and applied forces. CoP uses a center-of-pressure contact description for dexterous sim-to-real learning on an Allegro hand. On real peg-in-hole insertion, CoP reaches 0.78 success across six shapes, ahead of raw taxels at 0.48 and binary contact at 0.53.

#### Evidence
- [Tabero: Learning Gentle Manipulation with Closed-Loop Force Feedback from Vision, Touch, and Language](../Inbox/2026-05-27--tabero-learning-gentle-manipulation-with-closed-loop-force-feedback-from-vision-touch-and-language.md): Tabero tactile data pipeline, force feedback controller, and grip-force result.
- [Beyond Binary: Sim-to-Real Dexterous Manipulation with Physics-Grounded Contact Representation](../Inbox/2026-05-27--beyond-binary-sim-to-real-dexterous-manipulation-with-physics-grounded-contact-representation.md): CoP tactile representation and real peg-in-hole sim-to-real results.

### Deployment tests target memory cost and input fragility
Ω-QVLA compresses both the language backbone and diffusion action head of VLA policies to uniform W4A4 precision without training. On Pi 0.5 it reports 98.0% average manipulation success, close to the FP16 reference at 97.1%, while reducing static memory footprint by 71.3%. ReasonBreak covers a different deployment risk: small text corruptions in driving commands can alter reasoning and trajectories in NVIDIA Alpamayo models. In closed-loop simulation, the paper reports up to 72% attack success for trajectory manipulation and links successful attacks to higher collision, off-road, and wrong-lane failures.

#### Evidence
- [Ω-QVLA: Robust Quantization for Vision-Language-Action Models via Composite Rotation and Per-step Scaling](../Inbox/2026-05-27--o-qvla-robust-quantization-for-vision-language-action-models-via-composite-rotation-and-per-step-scaling.md): Ω-QVLA W4A4 quantization, success rates, and memory reduction.
- [ReasonBreak: Probing Vulnerabilities in Reasoning-Enabled Vision-Language-Action Models for Autonomous Driving](../Inbox/2026-05-27--reasonbreak-probing-vulnerabilities-in-reasoning-enabled-vision-language-action-models-for-autonomous-driving.md): ReasonBreak black-box text perturbation attacks and closed-loop driving safety results.
