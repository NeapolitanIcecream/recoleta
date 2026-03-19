---
source: arxiv
url: http://arxiv.org/abs/2603.03482v1
published_at: '2026-03-03T19:58:31'
authors:
- Samuel Garcin
- Thomas Walker
- Steven McDonagh
- Tim Pearce
- Hakan Bilen
- Tianyu He
- Kaixin Wang
- Jiang Bian
topics:
- world-model
- persistent-3d-state
- interactive-video-generation
- 3d-consistency
- spatial-memory
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# Beyond Pixel Histories: World Models with Persistent 3D State

## Summary
PERSIST proposes an interactive world model with a **persistent 3D latent state**, rather than relying solely on pixel history to continue video generation. It places "memory" into a 3D scene representation that evolves over time, thereby improving spatial consistency, geometric consistency, and stability in long-horizon generation.

## Problem
- Existing interactive video/world models are typically based on autoregressive pixel history. Constrained by context windows, they can only remember a few seconds of the past and tend to forget previously seen regions in long sequences.
- Pixels are viewpoint-dependent, information-redundant, and only locally visible. Recovering the 3D world state by retrieving keyframes becomes increasingly difficult, leading to geometric inconsistency and weak spatial memory when revisiting scenes.
- This directly harms immersive interactive experiences and also hinders the use of world models as reliable simulators for training agents.

## Approach
- Core idea: explicitly maintain a **continuously evolving 3D latent world state**, and decompose world modeling into three parts: 3D world frame prediction, camera state prediction, and rendering generation from 3D to pixels.
- The world frame model predicts how the environment changes with actions in a voxelized 3D latent space; the camera model predicts the agent viewpoint; the 3D world is then projected onto the screen to form a depth-ordered stack of 2D features.
- The pixel generator uses these projected 3D features as the main conditioning input, generating the current frame like a "learnable deferred renderer/shader," thereby explicitly injecting geometric consistency into video generation.
- For training, it uses rectified flow / diffusion-forcing for autoregressive generation, and adds noise augmentation to mitigate exposure bias between ground-truth conditioning during training and model-predicted conditioning during inference.
- Importantly, at inference time it can be initialized from only a single RGB image; although training uses 3D world frame and camera supervision, testing does not require real 3D conditions.

## Results
- Trained on the Craftium/Luanti procedural 3D world, with a data scale of about **40 million interactions, 100,000 trajectories, 460 hours, 24Hz**; evaluation uses **148 trajectories** from unseen test worlds.
- Compared with the baselines **Oasis** and **WorldMem**, PERSIST performs dramatically better on FVD: **PERSIST-S 209**, **PERSIST-XL 181**, **PERSIST-XL+w0 116**, versus **Oasis 706** and **WorldMem 596**. This indicates a clear improvement in long-horizon video distribution quality.
- User study results (1-5 scale) show across-the-board improvements in spatial, temporal, and overall quality: for example, **Overall Score** improves from **Oasis 1.9±0.1** and **WorldMem 1.5±0.07** to **PERSIST-S 2.6±0.09** and **PERSIST-XL 2.6±0.08**, reaching **3.0±0.1** when given the initial 3D world frame.
- On **3D Consistency**, **Oasis 1.9±0.1** and **WorldMem 1.7±0.09**, while **PERSIST-S 2.7±0.1** and **PERSIST-XL+w0 2.8±0.1**; on **Temporal Consistency**, **Oasis 1.8±0.1** and **WorldMem 1.5±0.08**, while PERSIST reaches **2.5-2.8**.
- The paper also claims new capabilities: synthesizing diverse 3D environments from a **single image**, supporting **600-step** autoregressive long sequences, enabling direct scene editing in 3D space, and maintaining the evolution of off-screen dynamic processes.
- Beyond Table 1, the excerpt does not provide more fine-grained task success-rate numbers; the strongest conclusion is that explicitly persistent 3D state significantly outperforms rolling-window and memory-retrieval-based pixel baselines.

## Link
- [http://arxiv.org/abs/2603.03482v1](http://arxiv.org/abs/2603.03482v1)
