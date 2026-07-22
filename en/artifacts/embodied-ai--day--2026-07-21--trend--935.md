---
kind: trend
trend_doc_id: 935
granularity: day
period_start: '2026-07-21T00:00:00'
period_end: '2026-07-22T00:00:00'
topics:
- embodied world models
- robotics
- action representations
- real-to-sim
- interactive simulation
run_id: materialize-outputs
aliases:
- recoleta-trend-935
tags:
- recoleta/trend
- topic/embodied-world-models
- topic/robotics
- topic/action-representations
- topic/real-to-sim
- topic/interactive-simulation
language_code: en
pass_output_id: 372
pass_kind: trend_synthesis
---

# Structured action interfaces anchor embodied world models

## Overview
The prior daily signal around action-relevant state continues, but today’s five papers apply structure more directly to world modeling. Visual trajectories, physical decomposition, and simulatable episode records connect actions to predicted consequences. Evidence comes from heterogeneous preprints and mostly separate evaluations, so it establishes a shared design direction rather than a settled winning architecture.

## Findings

### Visual action representations
RoboInter1.5 and Masked Visual Actions both place spatially explicit signals between intent and predicted outcomes. RoboInter1.5 supplies object grounding, affordances, contact points, and motion traces across more than 230,000 episodes. Masked Visual Actions instead exposes pixel-space entity trajectories to a pretrained video model; one checkpoint can predict scene responses or infer robot motion from desired object movement. On DROID, it reports LPIPS of 0.0945 versus 0.362 for Ctrl-World. Together, the papers support visual structure as an embodiment-flexible control interface, although RoboInter1.5’s inspected excerpt does not provide downstream comparison metrics.

#### Sources
- [RoboInter1.5: A Holistic Intermediate Representation Suite for Embodied World Modeling and Robotic Manipulation](../Inbox/2026-07-21--robointer1-5-a-holistic-intermediate-representation-suite-for-embodied-world-modeling-and-robotic-manipulation.md): Reports more than 230,000 episodes and over ten intermediate-representation types, including grounding, affordances, contacts, and motion traces.
- [Masked Visual Actions for Unified World Modeling](../Inbox/2026-07-21--masked-visual-actions-for-unified-world-modeling.md): Uses masked pixel-space trajectories for forward and inverse modeling and reports DROID LPIPS of 0.0945 versus 0.362 for Ctrl-World.

### Physical causes and replayable state
Two papers make physical attribution explicit rather than asking one latent transition to absorb every change. DWM separates action-driven effects from persistent environmental effects such as gravity and drift; it improves planning success by an average of 13.1 percentage points across three modified simulated benchmarks. Agentic Real2Sim reconstructs recorded interactions as physics-based episode twins with geometry, object state, alignment, and replay metrics. Its best tested backend replayed 48 of 100 DROID episodes successfully, showing both the utility and current brittleness of automated conversion.

#### Sources
- [DWM: Separating World Effects from Actions in Latent World Models](../Inbox/2026-07-21--dwm-separating-world-effects-from-actions-in-latent-world-models.md): Separates action-invariant world effects during training and reports a 13.1-point mean absolute planning gain across three W-variant benchmarks.
- [Agentic Real2Sim: Physics-based World Modeling with Vision-Language Agents](../Inbox/2026-07-21--agentic-real2sim-physics-based-world-modeling-with-vision-language-agents.md): Builds physics-based episode twins; the strongest tested backend achieved 48 successful replays out of 100 DROID episodes.

### World models as usable systems
The corpus also treats latency, hardware cost, and downstream use as part of world-model quality. ABot-World-0 reports persistent 720P generation at up to 16 FPS on one RTX 5090, with 1.2 seconds to the first action-conditioned frame and about 19 GiB peak memory. Masked Visual Actions uses imagined rollouts for policy evaluation and candidate ranking, while Agentic Real2Sim compares model cost alongside replay success. These results broaden evaluation beyond visual fidelity, but benchmark coverage remains uneven and ABot-World-0’s inspected text lacks numerical baseline comparisons.

#### Sources
- [ABot-World-0: Infinite Interactive World Rollout on a Single Desktop GPU](../Inbox/2026-07-21--abot-world-0-infinite-interactive-world-rollout-on-a-single-desktop-gpu.md): Reports 720P streaming at up to 16 FPS, 1.2-second action-to-first-frame latency, and roughly 19 GiB peak VRAM on an RTX 5090.
- [Masked Visual Actions for Unified World Modeling](../Inbox/2026-07-21--masked-visual-actions-for-unified-world-modeling.md): Applies imagined rollouts to policy evaluation, model-based planning, and inverse motion synthesis.
- [Agentic Real2Sim: Physics-based World Modeling with Vision-Language Agents](../Inbox/2026-07-21--agentic-real2sim-physics-based-world-modeling-with-vision-language-agents.md): Reports replay success and model bills across four vision-language model backends, with all backends below 50% absolute success.
