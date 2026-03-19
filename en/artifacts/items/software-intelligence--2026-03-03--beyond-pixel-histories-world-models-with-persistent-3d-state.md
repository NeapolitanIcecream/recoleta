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
- world-models
- 3d-scene-representation
- interactive-video-generation
- neural-rendering
- diffusion-models
relevance_score: 0.34
run_id: materialize-outputs
language_code: en
---

# Beyond Pixel Histories: World Models with Persistent 3D State

## Summary
PERSIST proposes an interactive world model with a persistent 3D state. Instead of relying only on past pixel frames, it explicitly maintains a latent 3D scene that evolves over time. This yields better spatial memory, geometric consistency, and stability in long-horizon generation.

## Problem
- Existing autoregressive video/world models usually look only at a limited-length history of pixel frames, so once generation goes beyond the context window, they tend to forget previously seen regions.
- Implicitly learning 3D structure from pixels alone is difficult, especially under viewpoint changes, occlusion, off-screen dynamics, and long-horizon revisitation, leading to geometric inconsistency and temporal drift.
- This matters because interactive generation must not only make individual frames look realistic, but also maintain a persistent, revisitable, and stable world over long episodes that can support agent training.

## Approach
- Core idea: replace memory based on pixel history with a continuously updated latent 3D world state. The model maintains three parts: a 3D world-frame, camera state, and a rendering module from 3D to pixels.
- The world-frame model uses 3D latent variables to predict how the scene evolves with actions; the camera model predicts the player's viewpoint; then geometric projection maps 3D voxel features onto the screen, after which a pixel generator produces the current frame.
- The pixel generator acts like a learned deferred shader: it uses the projected 3D features as the main conditioning signal, then adds information not directly covered by the 3D representation, such as texture, lighting, particles, and screen-space effects.
- To mitigate exposure bias in autoregressive inference, the authors apply diffusion forcing to the diffusion/flow models and add noise augmentation when training different components, allowing modules to be trained separately and combined directly at inference time.
- Training relies on supervision from the environment in the form of 3D voxel world-frame data and camera parameters; at inference, the model can be initialized from only a single RGB frame, and it also supports providing an initial 3D world-frame for further gains.

## Results
- On Luanti/Craftium, the authors collected about 40 million environment interactions, roughly 100,000 trajectories, and a total of 460 hours of 24 Hz gameplay data; the 3D observations are 48^3 voxel grids centered on the player.
- Compared with Oasis, PERSIST-S reduces FVD from 706 to 209, and PERSIST-XL reduces it to 181; both are also substantially lower than WorldMem's 596, indicating better video distribution quality and long-horizon stability.
- In the user study, PERSIST-S achieves 2.8/2.7/2.5/2.6 on single-frame visual quality / 3D consistency / temporal consistency / overall score; Oasis scores 2.1/1.9/1.8/1.9, and WorldMem scores 1.7/1.7/1.5/1.5 (on a 1-5 scale).
- The strongest configuration, PERSIST-XL+w0, reaches an FVD of 116 and user scores of 3.2 (visual quality), 2.8 (3D consistency), 2.8 (temporal consistency), and 3.0 (overall), outperforming all baselines and other PERSIST variants.
- The paper also claims the model can synthesize diverse 3D environments from a single image, support 600-step autoregressive rollout, and enable direct editing of terrain/biomes/trees and other objects in 3D space for geometry-aware control; these capabilities are mainly shown through qualitative results.

## Link
- [http://arxiv.org/abs/2603.03482v1](http://arxiv.org/abs/2603.03482v1)
