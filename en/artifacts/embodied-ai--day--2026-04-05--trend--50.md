---
kind: trend
trend_doc_id: 50
granularity: day
period_start: '2026-04-05T00:00:00'
period_end: '2026-04-06T00:00:00'
topics:
- embodied-ai
- vla-safety
- adaptive-control
- driving-world-models
- dexterous-grasping
run_id: materialize-outputs
aliases:
- recoleta-trend-50
tags:
- recoleta/trend
- topic/embodied-ai
- topic/vla-safety
- topic/adaptive-control
- topic/driving-world-models
- topic/dexterous-grasping
language_code: en
pass_output_id: 16
pass_kind: trend_synthesis
---

# Embodied AI work is concentrating on the action loop

## Overview
April 5 is a strong embodied-AI day centered on action control. The clearest papers improve what happens between perception and execution: safer VLA policies, adaptive action chunking, and joint video-action planning for driving. The common thread is operational detail. Authors are editing robot policies at module level, tuning replanning at inference time, and training world models so predicted scenes stay aligned with planned motion.

## Clusters

### Selective unlearning reaches robot policy level
Safety work in vision-language-action models is getting more concrete. VLA-Forget edits the visual encoder, cross-modal projector, and upper action layers in stages, then uses retain, forget, mismatch, and feature-preservation losses to remove unwanted behavior without wiping out task skill. The reported numbers are strong for this kind of intervention: on OpenVLA-7B with Open X-Embodiment it posts FC 93, RC 91, and TSR 78, with lower safety-violation recovery after quantization than NPO and much better retention than GA. That matters because the failure target is a robot action, not just a text output.

#### Evidence
- [VLA-Forget: Vision-Language-Action Unlearning for Embodied Foundation Models](../Inbox/2026-04-05--vla-forget-vision-language-action-unlearning-for-embodied-foundation-models.md): Summary with method and benchmark results for selective unlearning in VLA policies

### Action timing is becoming adaptive at inference
Inference-time control is a live optimization target. AAC changes action chunk size on the fly by reading entropy over sampled candidate trajectories, then replans sooner when the model is uncertain and executes longer chunks when predictions stay stable. The gains are modest but broad: GR00T rises from 59.7% to 62.0% on RoboCasa, from 94.1% to 95.0% on LIBERO, and from 88.8% to 92.8% on LIBERO-Long. The pattern matches the last few days of robotics work in this corpus: progress is coming from tighter control over the action interface and replanning loop.

#### Evidence
- [Adaptive Action Chunking at Inference-time for Vision-Language-Action Models](../Inbox/2026-04-05--adaptive-action-chunking-at-inference-time-for-vision-language-action-models.md): Summary with AAC mechanism and benchmark deltas across RoboCasa and LIBERO

### Driving world models keep gaining from joint video supervision
Joint video-and-action generation is still one of the clearest routes to stronger driving planners. DriveVA predicts future video latents and ego trajectory tokens in one generative process, and the paper ties a large part of its gain to dense video supervision. On NAVSIM v1 it reaches 90.9 PDMS, above DiffusionDrive at 88.1, and it reports large zero-shot transfer gains on nuScenes and Bench2Drive/CARLA v2, including an 83.3% collision-rate reduction on nuScenes against the stated world-model baseline. The notable point is practical: the model claims near-optimal closed-loop performance with only two sampling steps.

#### Evidence
- [DriveVA: Video Action Models are Zero-Shot Drivers](../Inbox/2026-04-05--driveva-video-action-models-are-zero-shot-drivers.md): Summary with architecture, ablation claim on video supervision, and closed-loop plus transfer results

### Sparse task structure is improving dexterous grasping
Dexterous manipulation work is also leaning on sparse structure that humans can inspect. GRIT uses a 30-way grasp taxonomy plus wrist orientation as the high-level command, chosen by a vision-language model from the scene and task, then executes with a taxonomy-conditioned control policy. It reports 87.9% overall success and tests on 373 novel objects after training on 30 YCB objects. The paper also emphasizes user control: when a grasp strategy is wrong, the interface gives a concrete handle for changing it.

#### Evidence
- [Learning Dexterous Grasping from Sparse Taxonomy Guidance](../Inbox/2026-04-05--learning-dexterous-grasping-from-sparse-taxonomy-guidance.md): Summary with two-stage taxonomy-guided method and reported success on novel objects
