---
kind: trend
trend_doc_id: 285
granularity: day
period_start: '2026-05-06T00:00:00'
period_end: '2026-05-07T00:00:00'
topics:
- robot learning
- Vision-Language-Action
- latent actions
- visual foresight
- model predictive control
- world models
run_id: materialize-outputs
aliases:
- recoleta-trend-285
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action
- topic/latent-actions
- topic/visual-foresight
- topic/model-predictive-control
- topic/world-models
language_code: en
pass_output_id: 134
pass_kind: trend_synthesis
---

# Robot policies are being measured by compact foresight and deployable control

## Overview
The current emphasis is robot policies that keep useful internal state under deployment constraints. Vision-Language-Action (VLA) work focuses on compact spatial tokens, latent action supervision, and test-time visual correction. Dream-MPC adds the same pressure to continuous control: plan online, but keep model calls low.

## Findings

### Compact spatial foresight for VLA manipulation
ConsisVLA-4D treats spatial consistency as an inference budget problem. It keeps 32 instruction-relevant visual tokens, aligns them across multiple camera views, and stores geometry in compact latent tokens. The reported gains are tied to both accuracy and speed: 21.6% better performance and 2.3× faster inference than OpenVLA on LIBERO, plus 41.5% better performance and 2.4× faster inference on real robot platforms.

T³VF addresses a different failure point in visual-foresight VLA models. It compares a predicted future image with the later observed image, then updates only learnable query tokens when action variance is low. On LIBERO-Plus with perturbed training, it raises Mantis average success from 49.3% to 52.1%, with larger gains on camera and lighting perturbations.

#### Sources
- [ConsisVLA-4D: Advancing Spatiotemporal Consistency in Efficient 3D-Perception and 4D-Reasoning for Robotic Manipulation](../Inbox/2026-05-06--consisvla-4d-advancing-spatiotemporal-consistency-in-efficient-3d-perception-and-4d-reasoning-for-robotic-manipulation.md): Summary of ConsisVLA-4D token compression, multi-view 3D perception, future-scene reasoning, and reported LIBERO and real-world gains.
- [Test-Time Training for Visual Foresight Vision-Language-Action Models](../Inbox/2026-05-06--test-time-training-for-visual-foresight-vision-language-action-models.md): Summary of T³VF test-time training mechanism, filtered updates, and LIBERO-Plus perturbation results.

### Latent action tokens as VLA supervision
The latent-action study gives a controlled comparison that many VLA papers have lacked. Using one Qwen3-VL-2B-based baseline, it tests image-based latent actions and action-based latent actions across four integration methods. The strongest results depend on task type. LA-Direct reaches 96.6% on LIBERO-Long, a 10.8-point gain over the baseline. LA-Tok reaches 78.0% average success on RoboTwin 2.0, a 17.5-point gain, and improves motor-heavy tasks such as Move Can Pot from 46% to 70%.

The practical point is clear: latent actions are useful when they are matched to the supervision problem. Image-derived tokens help long-horizon scene reasoning. Action-derived tokens help normalize motor control across heterogeneous robot data.

#### Sources
- [From Pixels to Tokens: A Systematic Study of Latent Action Supervision for Vision-Language-Action Models](../Inbox/2026-05-06--from-pixels-to-tokens-a-systematic-study-of-latent-action-supervision-for-vision-language-action-models.md): Summary of the unified VLA baseline, four latent-action supervision strategies, and LIBERO, LIBERO-Long, and RoboTwin 2.0 results.

### Cheap online planning in latent world models
Dream-MPC applies the deployment theme to continuous control. It samples only five candidate action sequences from a policy prior, rolls them through a learned latent world model, and takes one gradient step using predicted reward and terminal value. An uncertainty penalty discourages plans that enter model-error regions, and action reuse carries optimization work across model-predictive-control steps.

The efficiency claim is concrete. In the reported setup, Dream-MPC uses 15 world-model evaluations per time step, compared with 9,216 for the cited MPPI configuration. With BMPC across 24 continuous-control tasks, it improves IQM normalized score by 26.7% and mean normalized score by 20.5%. With TD-MPC2, it improves over the policy-only baseline but does not consistently match TD-MPC2 with MPPI.

#### Sources
- [Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination](../Inbox/2026-05-06--dream-mpc-gradient-based-model-predictive-control-with-latent-imagination.md): Summary of Dream-MPC method, planner settings, evaluation counts, and benchmark results.
