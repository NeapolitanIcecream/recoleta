---
kind: trend
trend_doc_id: 43
granularity: day
period_start: '2026-04-04T00:00:00'
period_end: '2026-04-05T00:00:00'
topics:
- robot-learning
- safety
- data-generation
- medical-robotics
- vla
run_id: materialize-outputs
aliases:
- recoleta-trend-43
tags:
- recoleta/trend
- topic/robot-learning
- topic/safety
- topic/data-generation
- topic/medical-robotics
- topic/vla
language_code: en
pass_output_id: 14
pass_kind: trend_synthesis
---

# Robot learning work is getting closer to the control loop

## Overview
April 4 is a small but coherent robotics day. The strongest work tightens the loop between observation, action, and safety: synthetic demonstrations that keep action labels, behavior-switch detection that meets control-time constraints, and a colonoscopy platform that logs aligned multimodal data for closed-loop learning.

## Clusters

### Action-labeled synthetic data for robot transfer
Robot learning papers today focus on better action grounding, not bigger generic models. CRAFT is the clearest example. It uses simulator rollouts plus a Canny-guided video diffusion pipeline to generate photorealistic demonstrations that keep paired action labels. That matters in bimanual tasks, where contact and coordination errors break transfer quickly. The gains are large in cross-embodiment tests: from UR5 to Franka, CRAFT reports 82.6% on Lift Pot, 89.3% on Place Cans, and 86.0% on Stack Bowls with no target-robot demos. In real tests from xArm7 to Franka, it reaches 17/20, 15/20, and 16/20 successes on three tasks. The method also supports viewpoint, lighting, background, and embodiment changes in one pipeline.

#### Evidence
- [CRAFT: Video Diffusion for Bimanual Robot Data Generation](../Inbox/2026-04-04--craft-video-diffusion-for-bimanual-robot-data-generation.md): Summary with method and full reported results.

### Fast behavior-change detection for safer shared manipulation
Safety work is getting more specific about when a controller must react. UA-ToM adds a 992K belief module to a frozen 7B vision-language-action model and tracks whether a collaborator has changed behavior mid-task. The paper argues that loose detection windows hide operational risk. Its stronger result is at a tighter ±3-step window, about 150 ms in a 50 ms control loop, where UA-ToM reaches 85.7% hard detection across 1,200 episodes. More important for deployment, switch detection cuts post-switch collisions from 2.34 to 1.11 per episode, a 52% reduction, with 7.4 ms added inference cost.

#### Evidence
- [Belief Dynamics for Detecting Behavioral Shifts in Safe Collaborative Manipulation](../Inbox/2026-04-04--belief-dynamics-for-detecting-behavioral-shifts-in-safe-collaborative-manipulation.md): Summary with detection-window analysis, collision reduction, and overhead.

### Closed-loop datasets are getting instrumented enough for medical autonomy
Medical robotics contributes infrastructure rather than a new policy result. OpenRC packages a low-cost robotic colonoscopy setup with synchronized video, operator commands, actuation state, and 6-DoF tip pose. The practical point is data alignment for closed-loop learning. The system can be assembled for under $5,000 excluding the EM tracker, and the dataset includes 1,894 episodes over about 19 hours across 10 task variations. It also includes 142 failure episodes and 141 recovery episodes, which gives future work grounded cases for navigation mistakes, wall contact, and lumen loss. After alignment, residual lag between action and actuation is 55.6 ms, and actuation-to-tip-pose lag is centered at 0.0 ms.

#### Evidence
- [OpenRC: An Open-Source Robotic Colonoscopy Framework for Multimodal Data Acquisition and Autonomy Research](../Inbox/2026-04-04--openrc-an-open-source-robotic-colonoscopy-framework-for-multimodal-data-acquisition-and-autonomy-research.md): Summary with dataset scale, modality alignment, and latency metrics.
