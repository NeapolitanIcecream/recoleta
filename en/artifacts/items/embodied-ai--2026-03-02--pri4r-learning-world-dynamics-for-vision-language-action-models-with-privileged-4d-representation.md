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
- world-model
- robot-manipulation
- 3d-point-tracking
- privileged-learning
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# Pri4R: Learning World Dynamics for Vision-Language-Action Models with Privileged 4D Representation

## Summary
Pri4R enables Vision-Language-Action (VLA) models to additionally learn during training "how actions change the 3D world," thereby improving robots' physical awareness and control precision in manipulation. It uses privileged 4D representations (3D point trajectories over time) as auxiliary supervision, but adds no extra input, output, or computational overhead at test time.

## Problem
- Existing VLAs are mainly trained with action labels, so they learn "how to move," but often fail to learn "how the world will change after moving."
- As a result, policies may be semantically reasonable yet lack understanding of geometric constraints, contact, and object motion dynamics, making them prone to failure in interactions involving door handles, drawers, knobs, and similar objects.
- Using language, images, features, or goal observations as auxiliary prediction signals is typically not directly aligned with the spatiotemporal metric space of robot control, and often introduces extra inference overhead.

## Approach
- The core method adds a lightweight point track head to the VLA during training, allowing it to predict future **3D point displacement trajectories** based on the current observation and the backbone network's internal features.
- These 3D point trajectories serve as "privileged supervision": they are generated from ground-truth scene meshes in simulation, and pseudo-labeled by an off-the-shelf 3D point tracker in real data; this branch is discarded after training.
- By injecting the VLA's internal embeddings used for action prediction into the point track head, the gradients from the point trajectory loss reshape the shared representation in reverse, causing it to encode how scene geometry evolves with actions.
- The authors choose **3D point trajectories** rather than images, language, or depth maps because they combine the advantages of temporal density, geometric metric structure, spatial sparsity, and better alignment with the action space.
- This design is compatible with two mainstream VLA types: backbone-centric (such as OpenVLA-OFT) and expert-style (such as the π series), requiring only minor architectural changes, while restoring the original VLA architecture unchanged at inference time.

## Results
- **LIBERO**: OpenVLA-OFT average success rate improves from **92.7%** to **96.3%** (+3.6); among them, **LIBERO-Long** improves from **85.5%** to **95.3%** (+9.8, roughly interpretable as +10%).
- **LIBERO**: π0.5 improves from **92.6%** to **94.0%** (+1.4); **LIBERO-Long** improves from **90.5%** to **94.3%** (+3.8). π0 improves from **87.4%** to **90.6%** (+3.2).
- **RoboCasa**: OpenVLA-OFT average success rate improves from **33.1%** to **46.3%** (+13.2, approximately a **40%** relative improvement); category-level gains include turning levers **36.0→66.7** (+30.7), pressing buttons **56.0→79.3** (+23.3), and open/close drawers **59.0→80.0** (+21.0).
- **RoboCasa**: π0.5 average **52.9→57.0** (+4.1), π0 average **38.8→42.2** (+3.4), showing that gains exist across different VLA architectures.
- The paper also claims improvements in **real-world experiments**, and ablations validate that 3D point trajectories are a more effective supervision target for learning action-world dynamics; however, the provided excerpt does not include specific numbers for the real-robot portion.

## Link
- [http://arxiv.org/abs/2603.01549v2](http://arxiv.org/abs/2603.01549v2)
