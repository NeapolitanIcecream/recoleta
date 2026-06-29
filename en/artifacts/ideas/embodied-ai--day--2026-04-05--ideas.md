---
kind: ideas
granularity: day
period_start: '2026-04-05T00:00:00'
period_end: '2026-04-06T00:00:00'
run_id: 2b28af61-f822-4000-a611-e369ac085066
status: succeeded
topics:
- embodied-ai
- vla-safety
- adaptive-control
- driving-world-models
- dexterous-grasping
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/vla-safety
- topic/adaptive-control
- topic/driving-world-models
- topic/dexterous-grasping
language_code: en
pass_output_id: 17
pass_kind: trend_ideas
upstream_pass_output_id: 16
upstream_pass_kind: trend_synthesis
---

# Adaptive policy control

## Summary
Embodied AI work here is getting more concrete at the control interface. The clearest near-term changes are a post-training unlearning workflow for deployed VLA policies, an inference-time adaptive chunking layer for robot replanning, and a joint video-and-trajectory evaluation track for driving world models. Each one is tied to a specific operational pain point: removing unsafe behavior without wiping out task skill, reducing fixed-chunk tuning in manipulation, and improving zero-shot transfer in driving planners.

## Post-training unlearning workflow for deployed VLA robot policies
Robot teams fine-tuning VLA policies need a post-training safety edit path that changes behavior without retraining the whole stack. VLA-Forget points to a concrete build: a policy editing workflow that targets the visual encoder, cross-modal projector, and upper action layers separately, then runs a fixed regression suite on retained tasks and safety probes before deployment. The practical user is the team that has already found a bad behavior in demonstration data or a privacy-sensitive pattern in a shipped model and needs a narrow fix.

The paper matters because it treats unlearning as a robot-control problem, not only a model-compliance problem. On OpenVLA-7B with Open X-Embodiment, it reports FC 93 and RC 91, with TSR 78 and SVR 5, while keeping much better retain performance than GA and improving post-quantization recovery over other baselines. That supports a build centered on staged edits plus acceptance tests after quantization, since the model may recover unsafe behavior when compressed for deployment.

A cheap validation step is straightforward: pick one recurring forbidden action or one known spurious visual trigger in an existing policy, apply a module-level edit, and measure three things side by side on the same eval set: forgetting success, retained task success, and safety-violation recovery after quantization. If those numbers move together, unlearning becomes a practical support layer for robotics deployment reviews.

### Evidence
- [VLA-Forget: Vision-Language-Action Unlearning for Embodied Foundation Models](../Inbox/2026-04-05--vla-forget-vision-language-action-unlearning-for-embodied-foundation-models.md): Summary of the staged unlearning method and benchmark results on OpenVLA-7B and pi0fast-base.
- [VLA-Forget: Vision-Language-Action Unlearning for Embodied Foundation Models](../Inbox/2026-04-05--vla-forget-vision-language-action-unlearning-for-embodied-foundation-models.md): Abstract claims on forgetting efficacy, retention, and post-quantization recovery reduction.
- [VLA-Forget: Vision-Language-Action Unlearning for Embodied Foundation Models](../Inbox/2026-04-05--vla-forget-vision-language-action-unlearning-for-embodied-foundation-models.md): Introduction frames the operational problem as unsafe or sensitive behaviors turning into physical actions.

## Inference-time adaptive action chunking middleware for robot replanning
Teams running manipulation models on long tasks can add an inference-time controller that changes action chunk length based on policy uncertainty. AAC is a concrete recipe for this: sample candidate action chunks, estimate entropy across future steps, execute a shorter segment when uncertainty rises, and let the robot run longer before replanning when predictions stay stable.

This is useful because fixed chunk size is still a tuning burden in VLA deployment. One setting gives smoother motion but reacts slowly; another replans quickly but can introduce discontinuities. AAC avoids retraining and works as a wrapper around an existing model. The reported gains are modest but consistent: GR00T on RoboCasa moves from 59.7% to 62.0%, LIBERO from 94.1% to 95.0%, and LIBERO-Long from 88.8% to 92.8%. The same pattern appears on pi-0.5 and on LIBERO-Pro perturbation tests.

The first build should be a replanning middleware layer for one existing policy, with logs that show chosen chunk length, entropy trend, and task outcome. A low-cost check is to replay a benchmark or lab task suite with fixed chunk sizes and AAC under the same compute budget, then compare success rate, replan count, and visible motion discontinuities. That would tell a robotics team whether adaptive chunking is worth adopting before touching training data or model weights.

### Evidence
- [Adaptive Action Chunking at Inference-time for Vision-Language-Action Models](../Inbox/2026-04-05--adaptive-action-chunking-at-inference-time-for-vision-language-action-models.md): Summary of AAC, the fixed-chunk deployment problem, and benchmark gains across RoboCasa and LIBERO.
- [Adaptive Action Chunking at Inference-time for Vision-Language-Action Models](../Inbox/2026-04-05--adaptive-action-chunking-at-inference-time-for-vision-language-action-models.md): Abstract describes the responsiveness versus consistency trade-off in chunked execution.
- [Adaptive Action Chunking at Inference-time for Vision-Language-Action Models](../Inbox/2026-04-05--adaptive-action-chunking-at-inference-time-for-vision-language-action-models.md): Introduction states that chunk size varies by policy and task, which supports a middleware-style deployment tool.

## Joint video-and-trajectory planner evaluation for zero-shot driving transfer
Driving teams building world-model planners can add a training and evaluation track for joint video-and-trajectory generation, then test whether it improves zero-shot transfer without increasing sampling cost too much. DriveVA gives a concrete target: predict future video latents and ego trajectory tokens in one shared generative process, then keep the rollout short enough that two sampling steps still deliver near-peak closed-loop performance.

The paper is useful because it ties planning quality to a measurable design choice. On NAVSIM v1, DriveVA reaches 90.9 PDMS, above several listed baselines, and the summary attributes a large part of the gain to dense video supervision, with PDMS rising from 71.4 to 90.9 when video supervision is included. It also reports large zero-shot transfer gains on nuScenes and Bench2Drive/CARLA v2, including an 83.3% collision-rate reduction on nuScenes against the stated world-model baseline.

A practical next step is a paired ablation in one existing driving stack: train an action-only planner and a joint video-action planner on the same source dataset, then compare closed-loop score, collision rate, and transfer to one held-out domain. If the joint model keeps its edge with low sampling steps, the result supports a new default for planner training and simulator evaluation.

### Evidence
- [DriveVA: Video Action Models are Zero-Shot Drivers](../Inbox/2026-04-05--driveva-video-action-models-are-zero-shot-drivers.md): Summary of DriveVA, joint generation design, dense video supervision effect, and benchmark results.
- [DriveVA: Video Action Models are Zero-Shot Drivers](../Inbox/2026-04-05--driveva-video-action-models-are-zero-shot-drivers.md): Abstract explains the video-trajectory consistency problem in prior loosely coupled planners.
- [DriveVA: Video Action Models are Zero-Shot Drivers](../Inbox/2026-04-05--driveva-video-action-models-are-zero-shot-drivers.md): Reported closed-loop and zero-shot transfer metrics on NAVSIM, nuScenes, and Bench2Drive/CARLA v2.
