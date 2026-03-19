---
source: arxiv
url: http://arxiv.org/abs/2603.01549v2
published_at: '2026-03-02T07:23:53'
authors:
- Jisoo Kim
- Jungbin Cho
- Sanghyeok Chu
- Ananya Bal
- Jinhyung Kim
- Gunhee Lee
- Sihaeng Lee
- Seung Hwan Kim
- Bohyung Han
- Hyunmin Lee
- Laszlo A. Jeni
- Seungryong Kim
topics:
- vision-language-action
- robot-learning
- world-dynamics
- 3d-point-tracking
- privileged-supervision
relevance_score: 0.35
run_id: materialize-outputs
language_code: en
---

# Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation

## Summary
Pri4R enables Vision-Language-Action (VLA) models to additionally learn "how actions change the world" during training, rather than only imitating the actions themselves. It uses 3D point tracks as privileged 4D supervision to improve robots' physical awareness and control precision in complex manipulation, while adding no overhead at inference time.

## Problem
- Existing VLAs are mainly trained with action labels, so they learn "how to move" but lack a dynamics-level understanding of "how the world changes after moving."
- This gap can lead to operations that appear semantically reasonable but are physically inaccurate, such as ignoring door hinges or drawer constraints, resulting in brittle interaction and task failure.
- When language, images, features, or goal states are used as auxiliary supervision, they are often misaligned with the spatiotemporal metric space where real control occurs, and many methods also increase inference latency and complexity.

## Approach
- The authors propose Pri4R: during training, they add a lightweight point track head to the VLA to predict the displacement/trajectory of 3D points in the scene over a future time window.
- The core mechanism is simple: feed the internal representations used by the VLA for action prediction into this auxiliary head, so the model simultaneously learns both "actions" and "how future 3D geometry evolves," thereby compressing world dynamics into the shared representation.
- The supervision signal uses preconstructed 3D point tracks (4D geometry: 3D changing over time), with stepwise 3D displacement as the learning target; in simulation, these are generated from ground-truth meshes, while in real scenes, pseudo-labels are generated using an off-the-shelf 3D point tracking model.
- The method is compatible with two mainstream VLA architecture families (such as OpenVLA-OFT and the π series). After training, the auxiliary head is discarded, so at test time the original VLA architecture, input-output interface, and compute all remain unchanged.

## Results
- **LIBERO**: OpenVLA-OFT average success rate improves from **92.7%** to **96.3%** (+**3.6**); among them, **LIBERO-Long** improves from **85.5%** to **95.3%**, about +**10** percentage points.
- **LIBERO**: π0 improves from **87.4% ± 0.2** to **90.6% ± 0.2**; π0.5 improves from **92.6% ± 0.4** to **94.0% ± 0.2**. OpenVLA-OFT + Pri4R reaches **93.2 / 98.6 / 98.1 / 95.3** on the four subsets, respectively.
- **RoboCasa**: OpenVLA-OFT average success rate improves from **33.1%** to **46.3%**, an increase of **13.2** points, or roughly a relative +**40%**; the authors also explicitly emphasize a "**+40% gain**" on RoboCasa in the abstract.
- **RoboCasa**: π0 improves from **38.8%** to **42.2%** (+**3.4**), and π0.5 from **52.9%** to **57.0%** (+**4.1**). OpenVLA-OFT shows large gains across multiple categories, such as Turning levers **36.0→66.7** (+**30.7**), Pressing buttons **56.0→79.3** (+**23.3**), and Open/Close drawers **59.0→80.0** (+**21.0**).
- The authors also claim that 3D point tracks are better suited than other auxiliary supervision targets for learning action-world dynamics, and they validate key design choices through systematic ablations; however, the provided excerpt does not include the full numerical tables for those ablations.

## Link
- [http://arxiv.org/abs/2603.01549v2](http://arxiv.org/abs/2603.01549v2)
