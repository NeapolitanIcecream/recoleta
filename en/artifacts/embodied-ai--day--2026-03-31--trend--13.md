---
kind: trend
trend_doc_id: 13
granularity: day
period_start: '2026-03-31T00:00:00'
period_end: '2026-04-01T00:00:00'
topics:
- robotics
- world-models
- vision-language-action
- object-centric-learning
- data-efficiency
run_id: materialize-outputs
aliases:
- recoleta-trend-13
tags:
- recoleta/trend
- topic/robotics
- topic/world-models
- topic/vision-language-action
- topic/object-centric-learning
- topic/data-efficiency
language_code: en
pass_output_id: 6
pass_kind: trend_synthesis
---

# Robot world models are moving into the action loop, with stronger results than structure

## Overview
This day is about world models becoming the control surface for robotics. DIAL ties a VLM to action through a latent future state and claims a large data-efficiency gain in VLA training. HCLSM tackles scene structure directly with slots, hierarchy, and causal edges, but its own results show how hard stable object-centric world modeling still is.

## Clusters

### Latent intent becomes the main VLA design point
DIAL treats future visual features as the control interface. The vision-language model (VLM) predicts a latent future at horizon 16, and a separate policy turns that forecast plus the current observation into a 16-step action chunk. The concrete payoff is data efficiency: the paper reports state-of-the-art results on RoboCasa GR1 Tabletop with 2,400 trajectories where prior full-data runs used 24,000. It also extends the recipe beyond one robot setup, using 27,419 EgoDex human trajectories for zero-shot generalization tests and reporting real-world transfer on the IRON-R01-1.11 humanoid.

#### Evidence
- [DIAL: Decoupling Intent and Action via Latent World Modeling for End-to-End VLA](../Inbox/2026-03-31--dial-decoupling-intent-and-action-via-latent-world-modeling-for-end-to-end-vla.md): Summary captures the latent intent bottleneck, two-stage training, benchmark scope, and 10x fewer demonstrations claim.

### Object-centric world models are becoming more explicit, but still fragile
HCLSM pushes world modeling toward object and event structure, but the evidence is mixed. The model splits scenes into slots, runs separate dynamics for continuous motion, event frames, and higher-level goals, and adds learned interaction edges between objects. Its two-stage training matters: first enforce slot specialization, then turn on future prediction. On PushT, the reported next-state prediction error is 0.008 with the staged method, and throughput reaches 2.9 steps per second. The paper also shows the current limits. Slots stay diffuse, the learned causal graph does not become useful, and only 2 of 4 runs finish because of bf16 NaNs.

#### Evidence
- [HCLSM: Hierarchical Causal Latent State Machines for Object-Centric World Modeling](../Inbox/2026-03-31--hclsm-hierarchical-causal-latent-state-machines-for-object-centric-world-modeling.md): Summary provides the staged training claim, PushT metrics, throughput, weak decomposition, failed causal graph, and instability details.
