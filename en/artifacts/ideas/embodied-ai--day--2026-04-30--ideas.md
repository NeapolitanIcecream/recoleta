---
kind: ideas
granularity: day
period_start: '2026-04-30T00:00:00'
period_end: '2026-05-01T00:00:00'
run_id: e2031d26-2165-4df5-ae61-5753d11ad71c
status: succeeded
topics:
- robot world models
- vision-language-action policies
- latent reasoning
- reinforcement learning
- synthetic robot data
- extended reality
- graph world models
tags:
- recoleta/ideas
- topic/robot-world-models
- topic/vision-language-action-policies
- topic/latent-reasoning
- topic/reinforcement-learning
- topic/synthetic-robot-data
- topic/extended-reality
- topic/graph-world-models
language_code: en
pass_output_id: 123
pass_kind: trend_ideas
upstream_pass_output_id: 122
upstream_pass_kind: trend_synthesis
---

# Latency-Aware Robot Policy Training

## Summary
Robot teams can put predictive policies through control tests that report action quality, p95 inference delay, update rate, and the amount of task data needed. The concrete work is a latency-aware evaluation harness, RL post-training that updates latent reasoning as part of the policy, and an XR data collection workflow for contact-rich manipulation cases where physical teleoperation is slow.

## Latency-aware evaluation harness for world-action robot policies
Robot policy teams should add a control-loop test harness that reports success rate together with end-to-end latency, p95 latency, action update frequency, and the cost of future-state prediction. The useful comparison is direct VLA control, latent future-aware control, and video-action joint prediction on the same task suite, with the same camera layout and action chunking.

MotuBrain gives a concrete target for this kind of test: it reports RoboTwin 2.0 success above 95% while cutting end-to-end latency from 4.90 seconds to 0.09 seconds and raising frequency to 11.11 Hz. Being-H0.7 points to a second design point: train with future observations, drop the future-aware branch at inference, and run at 3–4 ms per step without test-time video rollout. A practical first check is a replay-and-robot run on long-horizon manipulation tasks where the report fails any model that improves prediction quality while missing the robot’s control deadline.

### Sources
- [MotuBrain: An Advanced World Action Model for Robot Control](../Inbox/2026-04-30--motubrain-an-advanced-world-action-model-for-robot-control.md): MotuBrain reports joint future-video/action prediction, RoboTwin 2.0 success above 95%, and a latency reduction from 4.90 s to 0.09 s.
- [Being-H0.7: A Latent World-Action Model from Egocentric Videos](../Inbox/2026-04-30--being-h0-7-a-latent-world-action-model-from-egocentric-videos.md): Being-H0.7 trains with future observations, removes the posterior branch at inference, and reports 3–4 ms per-step deployment.
- [World Model for Robot Learning: A Comprehensive Survey](../Inbox/2026-04-30--world-model-for-robot-learning-a-comprehensive-survey.md): The robot world-model survey defines action-conditioned future prediction and frames foresight, planning, and data amplification as core capabilities.

## RL post-training run that updates latent reasoning and action tokens together
Teams fine-tuning VLA manipulation policies can test a small RL post-training pass that treats latent reasoning tokens as trainable decision variables, not only hidden features. The run should start with a narrow task family, one or a few demonstrations per task, and a task reward that updates both latent embeddings and emitted action chunks.

LaST-R1 is the clearest local case. It starts from Qwen3-VL-4B with SigLIP2-Large vision encoding, uses compact latent targets based on DINOv3 CLS features, and applies Latent-to-Action Policy Optimization to the latent sequence and action sequence. The reported results are high enough to justify a replication check: 99.9% average success across LIBERO suites after one demonstration per task for warm-up, plus up to a 22.5% average gain over supervised fine-tuning in four real-world tasks. The useful adoption test is whether the same reward path reduces compounding errors on a team’s own long-horizon task without adding inference-time encoders.

### Sources
- [LaST-R1: Reinforcing Robotic Manipulation via Adaptive Physical Latent Reasoning](../Inbox/2026-04-30--last-r1-reinforcing-robotic-manipulation-via-adaptive-physical-latent-reasoning.md): LaST-R1 describes LAPO, joint RL optimization of latent reasoning and action tokens, one-demonstration LIBERO warm-up, and reported real-robot gains.
- [LaST-R1: Reinforcing Robotic Manipulation via Adaptive Physical Latent Reasoning](../Inbox/2026-04-30--last-r1-reinforcing-robotic-manipulation-via-adaptive-physical-latent-reasoning.md): The paper states 99.9% LIBERO average success with one-shot supervised warm-up and up to 22.5% real-world improvement over supervised fine-tuning.

## XR demonstration collection workflow for contact-rich manipulation data gaps
Robot data teams can pilot XR demonstration collection for tasks where physical teleoperation time is lost to resets, safety checks, and scene setup. The workflow is concrete: run MuJoCo in the headset browser, record SE(3) hand or controller motion, retarget it to the robot hand or gripper with inverse kinematics, then generate multi-view training images with varied camera poses, lighting, clutter, and object meshes.

Lucid-XR reports the operational numbers that make this worth a limited trial. The system runs at 90 fps on Apple Vision Pro, records at 25 fps, and collected about twice as many demonstrations as real teleoperation during 30-minute sessions across three tasks. With augmentation, the effective dataset reached about five times the real teleoperation baseline. A cheap validation is a matched 30-minute collection comparison on one contact-rich task, followed by a cluttered holdout test; in the Lucid-XR kitchen-clearing result, ACT plus LucidSim kept 90% success in low clutter while ACT alone fell to 0%.

### Sources
- [Lucid-XR: An Extended-Reality Data Engine for Robotic Manipulation](../Inbox/2026-04-30--lucid-xr-an-extended-reality-data-engine-for-robotic-manipulation.md): Lucid-XR describes browser-based MuJoCo collection, retargeting, generative multi-view data, 90 fps operation, 25 fps recording, and throughput gains over real teleoperation.
- [Lucid-XR: An Extended-Reality Data Engine for Robotic Manipulation](../Inbox/2026-04-30--lucid-xr-an-extended-reality-data-engine-for-robotic-manipulation.md): The paper describes retargeting human pose data to robot form factors with MuJoCo inverse kinematics and markup bindings.
