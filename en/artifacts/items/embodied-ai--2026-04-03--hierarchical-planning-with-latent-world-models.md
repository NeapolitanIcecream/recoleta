---
source: arxiv
url: http://arxiv.org/abs/2604.03208v1
published_at: '2026-04-03T17:32:36'
authors:
- Wancong Zhang
- Basile Terver
- Artem Zholus
- Soham Chitnis
- Harsh Sutaria
- Mido Assran
- Randall Balestriero
- Amir Bar
- Adrien Bardes
- Yann LeCun
- Nicolas Ballas
topics:
- hierarchical-planning
- latent-world-models
- model-predictive-control
- zero-shot-robot-control
- long-horizon-planning
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Hierarchical Planning with Latent World Models

## Summary
This paper introduces HWM, a hierarchical planning method for learned latent world models that improves long-horizon zero-shot control. It plans at two time scales in a shared latent space, which raises success rates on real robot manipulation and simulation tasks while cutting planning compute.

## Problem
- Learned world models can support zero-shot control, but flat model predictive control gets weak on long-horizon tasks because rollout errors grow over time.
- Planning over long sequences of primitive actions is expensive because the search space grows quickly with horizon.
- This matters for embodied control because many robot and navigation tasks need multi-stage, non-greedy behavior from high-dimensional observations, often with only a goal image at test time.

## Approach
- HWM trains two latent world models in the same latent space: a low-level model for short-horizon primitive actions and a high-level model for longer-horizon transitions.
- The high-level model predicts waypoint latents using learned macro-actions. These macro-actions come from an action encoder that compresses chunks of low-level actions between waypoints.
- At inference, the high-level planner searches over latent macro-actions to move the current latent state toward the goal latent. Its first predicted latent waypoint becomes a subgoal.
- The low-level planner then searches over primitive actions to reach that latent subgoal, and the system replans in MPC style during execution.
- Because both levels share the same latent space, HWM does not need task-specific rewards, skill learning, inverse models, or hierarchical policies.

## Results
- On a real Franka pick-and-place task with VJEPA2-AC and only a final goal image, flat planning gets **0%** success and HWM gets **70%** success, a **+70 point** gain.
- On Franka drawer open/close, VJEPA2-AC improves from **30%** to **70%**, a **+40 point** gain.
- On Push-T with DINO-WM, success rises from **17%** to **61%**, a **+44 point** gain.
- On Diverse Maze with PLDM, success rises from **44%** to **83%**, a **+39 point** gain.
- On pick-and-place with oracle subgoals, the flat planner and HWM both get **80%**, which shows the main gain comes from automatic subgoal generation rather than easier low-level control.
- The paper claims similar or better success with about **3× less planning time** in the figure caption and up to **4× lower** inference-time planning cost in the contribution summary.

## Link
- [http://arxiv.org/abs/2604.03208v1](http://arxiv.org/abs/2604.03208v1)
