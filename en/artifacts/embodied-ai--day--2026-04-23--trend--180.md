---
kind: trend
trend_doc_id: 180
granularity: day
period_start: '2026-04-23T00:00:00'
period_end: '2026-04-24T00:00:00'
topics:
- robotics
- vision-language-action
- long-horizon manipulation
- world models
- safety evaluation
- dexterous manipulation
run_id: materialize-outputs
aliases:
- recoleta-trend-180
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/long-horizon-manipulation
- topic/world-models
- topic/safety-evaluation
- topic/dexterous-manipulation
language_code: en
pass_output_id: 104
pass_kind: trend_synthesis
---

# Robotics papers make execution supervision concrete

## Overview
This day’s robotics papers are strongest on execution control. The main work adds recovery signals, intervention loops, and physical constraints directly to acting systems. LoHo-Manip, Hi-WM, and the BEHAVIOR1K audit capture the emphasis: long-horizon success is being judged by whether a policy can recover, be corrected efficiently, and stay safe while it runs.

## Clusters

### Structured correction for long-horizon execution
Long-horizon robot work centered on explicit recovery logic inside the control loop. LoHo-Manip splits planning and execution, then replans from the current image with a remaining-plan memory and a 2D trace prompt. That design produced 63.1 on RoboVQA and 56.7 on EgoPlan2, ahead of named VLA baselines. ReCAPA attacks the same failure mode from another angle. It predicts mismatch across actions, subgoals, and full trajectories, and reports 58.65 on VisualAgentBench plus AI2-THOR success rate 0.75. The common point is simple: papers are putting progress checks and correction signals into execution, not leaving them outside the policy.

#### Evidence
- [Long-Horizon Manipulation via Trace-Conditioned VLA Planning](../Inbox/2026-04-23--long-horizon-manipulation-via-trace-conditioned-vla-planning.md): LoHo-Manip method and benchmark gains for progress-aware replanning with trace guidance.
- [ReCAPA: Hierarchical Predictive Correction to Mitigate Cascading Failures](../Inbox/2026-04-23--recapa-hierarchical-predictive-correction-to-mitigate-cascading-failures.md): ReCAPA hierarchy and results on cascading-failure mitigation.

### World models become intervention surfaces
World models are getting used as training workspaces, not only predictors. Hi-WM rolls a policy forward in a learned simulator, lets a human intervene near failure, and adds those corrections back into post-training. On three real robot tasks, average success improved by 37.9 points over the base policy and 19.0 over a world-model closed-loop baseline. The paper also reports Pearson r = 0.953 between world-model evaluation and real performance. That makes the simulator useful for deciding when intervention data is worth collecting, not just for offline scoring.

#### Evidence
- [Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training](../Inbox/2026-04-23--hi-wm-human-in-the-world-model-for-scalable-robot-post-training.md): Hi-WM setup and real-world post-training gains.

### Action heads get explicit spatial and contact cues
Several papers made physical structure more explicit at the action level. CorridorVLA predicts a few future end-effector anchors and constrains generated actions to stay inside a spatial corridor. That raises SmolVLA from 86.5% to 90.95% on LIBERO and from 45.37% to 57.74% on LIBERO-Plus, with similar gains for GR00T. FingerViP adds five fingertip cameras to a dexterous hand so the policy can see contact regions that wrist or third-person views miss. It reports 80.8% overall success across four real-world tasks, including confined and occluded settings. This day’s robotics papers kept adding structure close to contact: spatial anchors, fingertip views, and signals tied to the actual motion geometry.

#### Evidence
- [CorridorVLA: Explicit Spatial Constraints for Generative Action Heads via Sparse Anchors](../Inbox/2026-04-23--corridorvla-explicit-spatial-constraints-for-generative-action-heads-via-sparse-anchors.md): CorridorVLA explicit spatial anchors and benchmark improvements.
- [FingerViP: Learning Real-World Dexterous Manipulation with Fingertip Visual Perception](../Inbox/2026-04-23--fingervip-learning-real-world-dexterous-manipulation-with-fingertip-visual-perception.md): FingerViP fingertip visual sensing and real-world dexterous results.

### Safety gets measured during execution
Evaluation pressure also tightened. The BEHAVIOR1K audit argues that final-state metrics hide unsafe execution and unstable reproduction. Across 500 reviewed runs, grasp failure was the most common error and collisions were frequent. When safety penalties are added, average RLC score drops from Q = 0.256 to sQ = 0.239, and Comet drops from 0.192 to 0.173. A separate manipulation paper, Wiggle and Go!, fits the same concern from the task side: it uses one low-risk probing motion to estimate rope dynamics before acting, then reaches 3.55 cm real target accuracy against 15.34 cm without parameter-informed control. The message is practical. Better robotics results now depend on safer evaluation and safer information gathering before commitment.

#### Evidence
- [How VLAs (Really) Work In Open-World Environments](../Inbox/2026-04-23--how-vlas-really-work-in-open-world-environments.md): Safety-aware audit of VLA execution and metric drops under safety penalties.
- [Wiggle and Go! System Identification for Zero-Shot Dynamic Rope Manipulation](../Inbox/2026-04-23--wiggle-and-go-system-identification-for-zero-shot-dynamic-rope-manipulation.md): Low-risk probing for zero-shot rope manipulation with large accuracy gain.
