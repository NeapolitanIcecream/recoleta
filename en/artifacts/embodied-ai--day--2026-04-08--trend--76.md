---
kind: trend
trend_doc_id: 76
granularity: day
period_start: '2026-04-08T00:00:00'
period_end: '2026-04-09T00:00:00'
topics:
- embodied-ai
- world-models
- model-based-rl
- retrieval
- safety
run_id: materialize-outputs
aliases:
- recoleta-trend-76
tags:
- recoleta/trend
- topic/embodied-ai
- topic/world-models
- topic/model-based-rl
- topic/retrieval
- topic/safety
language_code: en
pass_output_id: 42
pass_kind: trend_synthesis
---

# Embodied control work concentrates on grounded decision mechanisms

## Overview
This day is small but clear. Both papers work on embodied decision loops that stay closer to real constraints. One uses memory retrieval over event-coded situations for UAV control. The other uses grounded imagination to cut rollout drift in model-based reinforcement learning. The common emphasis is action selection that remains fast, checkable, and stable when horizons get longer or environments get messier.

## Clusters

### Retrieval-based world models for inspectable action selection
Memory is the main concrete mechanism in the day’s embodied control paper. The UAV system turns a scene into semantic events, retrieves similar past situations from a knowledge bank, then picks an action from the best-matching maneuver cluster. The paper’s claim is practical: keep the control loop fast enough for deployment while leaving a trace of why an action was chosen. Reported results are strong inside its own setup, with 20–50 ms control intervals, sub-millisecond retrieval, and 100% success with zero collisions across five adversarial curriculum episodes. The evidence is narrower than a benchmark-heavy robotics paper, since the excerpt does not show external baselines or broad ablations.

#### Evidence
- [Event-Centric World Modeling with Memory-Augmented Retrieval for Embodied Decision-Making](../Inbox/2026-04-08--event-centric-world-modeling-with-memory-augmented-retrieval-for-embodied-decision-making.md): Summary gives the event-centric retrieval design and reported UAV results.

### Grounded imagination in model-based reinforcement learning
The reinforcement learning paper centers on keeping imagined trajectories tied to reality over long horizons. GIRL adds a grounding signal from DINOv2, a vision model, and replaces a fixed KL term with an adaptive trust-region bottleneck that reacts to uncertainty and real-transition feedback. The reported gains are broad: IQM 0.81 on DeepMind Control versus 0.67 for DreamerV3 and 0.71 for TD-MPC2, plus lower drift scores and better results on distractor and manipulation tasks. A distilled variant also cuts the grounding overhead from 22% of wall-clock time to under 4%, which matters if the method is to stay competitive in training speed.

#### Evidence
- [GIRL: Generative Imagination Reinforcement Learning via Information-Theoretic Hallucination Control](../Inbox/2026-04-08--girl-generative-imagination-reinforcement-learning-via-information-theoretic-hallucination-control.md): Summary gives the method, benchmark comparisons, drift reductions, and compute note.
