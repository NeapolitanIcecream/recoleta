---
source: arxiv
url: http://arxiv.org/abs/2603.06679v1
published_at: '2026-03-03T18:58:17'
authors:
- Ryan Po
- David Junhao Zhang
- Amir Hertz
- Gordon Wetzstein
- Neal Wadhwa
- Nataniel Ruiz
topics:
- diffusion-game-engine
- external-memory
- multiplayer-world-model
- level-design
- interactive-video-generation
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# MultiGen: Level-Design for Editable Multiplayer Worlds in Diffusion Game Engines

## Summary
MultiGen proposes a diffusion-based game engine with explicit external memory to generate first-person game worlds that are editable, reproducible, and support multiplayer shared state. The core contribution is adding a persistently readable and writable memory for maps and player state beyond the traditional generation paradigm that "only looks at the most recent few frames."

## Problem
- Existing diffusion game engines typically keep state implicit within a limited frame context, which makes long-horizon generation prone to drift, hard to reproduce, and difficult for users to directly edit world structure.
- This makes shared multiplayer worlds especially difficult: different players lack a unified, readable and writable common state, and consistency of cross-view interactions is hard to guarantee.
- This problem matters because controllable level design and consistent multiplayer interaction are key capabilities for generative game engines to move toward real creation workflows and interactive entertainment.

## Approach
- The method decomposes the system into three modules: **Memory** stores external world state (2D map geometry and player poses), **Observation** generates the next frame from historical frames + memory readout + actions, and **Dynamics** updates poses based on actions and features.
- External memory is the central mechanism: users can directly edit a top-down 2D minimap, and the model queries this map at every step instead of relying only on short-term visual history to "guess" world structure.
- To feed map information into the visual generator, the system performs ray tracing on the map from the current pose to obtain 1D depth/disparity signals, which are provided as additional conditioning to the diffusion UNet.
- Actions are injected into the observation model through embeddings and cross-attention; pose updates are predicted by a lightweight Transformer as pose increments, thereby advancing the shared world state.
- In multiplayer mode, each player runs their own observation/dynamics modules, but all players read from and write to the same external memory, so one player's actions can affect what another player sees.

## Results
- The level-design evaluation is based on **Doom**, using data from **100** procedurally generated maps and more than **10 million** frames of gameplay data.
- Compared with a no-external-memory baseline similar to **GameNGen**, overall visual similarity is better: **SSIM** improves from **0.457** to **0.469**, and **LPIPS** decreases from **0.442** to **0.416**.
- In early steps **1–128**, **SSIM** improves from **0.476** to **0.484**, and **LPIPS** decreases from **0.389** to **0.375**.
- In later steps **128–196**, which better reflect long-horizon stability, **SSIM** improves from **0.418** to **0.438**, and **LPIPS** decreases from **0.549** to **0.496**, indicating that external memory better suppresses long-range structural drift.
- The paper also claims real-time multiplayer generation, cross-player viewpoint consistency, and shared interactions such as kills/respawns, but the provided excerpt does not include quantitative metrics for the multiplayer portion.

## Link
- [http://arxiv.org/abs/2603.06679v1](http://arxiv.org/abs/2603.06679v1)
