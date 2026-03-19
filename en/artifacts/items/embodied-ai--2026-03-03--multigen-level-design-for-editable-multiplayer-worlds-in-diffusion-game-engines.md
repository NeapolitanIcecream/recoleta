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
- multiplayer-worlds
- level-design
- video-world-model
relevance_score: 0.2
run_id: materialize-outputs
language_code: en
---

# MultiGen: Level-Design for Editable Multiplayer Worlds in Diffusion Game Engines

## Summary
MultiGen proposes a diffusion-based game engine with **explicit external memory** for generating interactive worlds that are editable, reproducible, and support multiplayer shared state. Its core contribution is to separate the "world state" from short-term video context, making level design and consistent multiplayer interaction more natural.

## Problem
- Existing diffusion game engines are mostly **next-frame predictors**, with world state implicit in a limited history of frames, which causes long-horizon generation to drift easily and makes reproduction difficult.
- Users have difficulty **directly editing environment structure**; when trying to specify a level layout in advance, the model often cannot follow it reliably over a long rollout.
- In multiplayer settings, different players usually do not truly **share an underlying world state**, so cross-view consistency and interaction are hard to maintain, even though both are important for interactive simulation and gameplay.

## Approach
- Introduces **external memory** independent of the context window to continuously store the static map and player poses, rather than relying only on the most recent image frames as state.
- Splits the system into three modules: **Memory** (stores map geometry and player pose), **Observation** (generates the next frame based on historical frames + memory readout + actions), and **Dynamics** (updates the next-step pose based on actions and features).
- Uses a user-editable **top-down 2D minimap** as the environment blueprint; at each step, the model performs ray-tracing from the map and current pose to obtain a 1D depth/disparity conditioning signal, which is then fed into the diffusion UNet.
- Actions are injected into the observation model through learned embeddings; the dynamics module uses a lightweight transformer to predict pose deltas, thereby advancing the shared state.
- In multiplayer mode, each player runs their own Observation/Dynamics, but they **jointly read and write the same external memory**, enabling first-person views that remain mutually consistent and can affect one another.

## Results
- Level-design dataset: the authors collected **more than 10 million frames** of gameplay data on **100 procedurally generated Doom maps** to train generalization across layouts.
- Compared with a no-external-memory baseline similar to **GameNGen**, the authors report better structural consistency on level-conditioned rollout: **SSIM(all) 0.469 vs 0.457**, **LPIPS(all) 0.416 vs 0.442**.
- In the early interval **steps 1–128**, the method achieves **SSIM 0.484 vs 0.476**, **LPIPS 0.375 vs 0.389**, indicating improved short-term quality as well.
- In the later interval **steps 128–196**, the improvement is more pronounced: **SSIM 0.438 vs 0.418**, **LPIPS 0.496 vs 0.549**, supporting the claim that **external memory reduces long-horizon drift**.
- For multiplayer generation, the excerpt mainly provides **qualitative results**: two players can meet, kill each other, respawn, and remain consistent across both viewpoints in a shared world; the passage does not provide explicit quantitative multiplayer metrics.

## Link
- [http://arxiv.org/abs/2603.06679v1](http://arxiv.org/abs/2603.06679v1)
