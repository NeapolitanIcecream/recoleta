---
source: arxiv
url: https://arxiv.org/abs/2605.14398v1
published_at: '2026-05-14T05:33:41'
authors:
- Hongyu Wang
- Jingquan Wang
- Bocheng Zou
- Radu Serban
- Dan Negrut
topics:
- world-model
- physics-simulation
- agentic-code-generation
- embodied-simulation
- robot-simulation
- video-world-models
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Coding Agent Is Good As World Simulator

## Summary
The paper claims that a coding agent can build a physics-based world model by writing and repairing executable PyChrono simulation code. Its main value is replacing video-only rollouts with simulator state that can expose bodies, joints, contacts, sensors, and solver diagnostics.

## Problem
- Video world models can make plausible frames while losing physical state, which leads to unstable contacts, shape distortion, and inconsistent motion in long rollouts.
- Building physics simulations by hand takes simulator knowledge, asset selection, collision setup, code writing, parameter tuning, and visual inspection.
- This matters for embodied agents, robot tasks, vehicles, and fluid-solid interaction, where control and evaluation depend on executable dynamics rather than appearance alone.

## Approach
- The system turns a text prompt, with an optional reference image, into a structured simulation plan with objects, spatial relations, physical roles, implementation steps, and camera settings.
- A code agent writes PyChrono code using a skill library, an asset library, deterministic tools, and a version-specific API index.
- The generated program runs in Project Chrono and produces logs, trajectories, rendered frames, and videos.
- A visual review agent checks the rendered video for objects, layout, motion, contacts, and mismatches with the plan.
- A simulation judge combines logs, trajectory data, and visual review, then sends concrete error reports back to patch the same program across iterations.

## Results
- Plan generation reached 100% Pass@1, Pass@3, and Pass@5 on all three reported tasks: Outdoor vehicle, FSI vehicle, and Robot in office, under both text-only and text-plus-image inputs.
- Representative successful runs took 24 minutes for Outdoor vehicle, 30 minutes for FSI vehicle, and 28 minutes for Robot in office.
- Token use was high: 1.68e+06 total tokens for Outdoor vehicle, 3.24e+06 for FSI vehicle, and 6.34e+06 for Robot in office.
- On WorldModelBench scenario-level totals, the system beat Wan2.2-TI2V-5B on Vehicle FSI by +1.70 points, 6.80±1.03 versus 5.10±0.99, with p=0.0012.
- Outdoor vehicle improved by +0.30 points, 5.80±1.14 versus 5.50±1.08, with p=0.5203; Robot in office improved by +0.80 points, 6.90±0.57 versus 6.10±1.10, with p=0.0528.
- Aggregated by metric, instruction score improved by +2.40 points, 5.90±0.57 versus 3.50±0.85, with p=0.000059; physical-laws score improved by +0.40 with p=0.5086, and common-sense score was tied at 2.30 versus 2.30 with p=1.0000.

## Link
- [https://arxiv.org/abs/2605.14398v1](https://arxiv.org/abs/2605.14398v1)
