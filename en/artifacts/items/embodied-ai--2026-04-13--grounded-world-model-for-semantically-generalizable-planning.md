---
source: arxiv
url: http://arxiv.org/abs/2604.11751v1
published_at: '2026-04-13T17:25:41'
authors:
- Quanyi Li
- Lan Feng
- Haonan Zhang
- Wuyang Li
- Letian Wang
- Alexandre Alahi
- Harold Soh
topics:
- world-model
- vision-language-action
- semantic-generalization
- model-predictive-control
- robot-planning
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Grounded World Model for Semantically Generalizable Planning

## Summary
This paper replaces goal-image scoring in model-predictive control with language-grounded scoring in a shared vision-language latent space. The result is a planning system, GWM-MPC, that keeps pretrained semantic knowledge and generalizes far better than standard vision-language-action policies on unseen instructions and visual signals.

## Problem
- Standard visuomotor MPC usually needs a goal image and scores candidate futures by latent distance to that image. That is awkward for new tasks and weak as a human interface.
- Fine-tuned VLA policies often memorize training instructions and scene shortcuts instead of using pretrained semantic knowledge. In this paper's WISER benchmark, they solve training tasks but fail on held-out tasks that require the same motions with new wording and new visual cues.
- The target problem is semantic generalization: follow unseen referring expressions and world-knowledge-based instructions as long as the needed motions were shown in training.

## Approach
- The paper trains a **Grounded World Model (GWM)** in the frozen latent space of **Qwen3-VL-Embedding**, a multimodal retrieval model that maps text, images, and videos into one embedding space.
- At test time, the system proposes **12** candidate action sequences by nearest-neighbor retrieval over demonstrated trajectories using current joint positions. For each candidate, GWM predicts the future latent embedding of the resulting behavior.
- It scores each predicted future against the language instruction with **cosine similarity** in the shared embedding space, then executes the highest-scoring action chunk. This turns MPC into a language-conditioned planner without requiring a goal image.
- To encode actions without learning a separate action tokenizer, the method uses **Rendering-based Action Tokenization (RAT)**: it renders future robot joint configurations as images with the robot URDF and camera parameters, then feeds those renderings through the pretrained vision encoder.
- Training uses only future-observation supervision in latent space with an MSE loss between predicted future features and ground-truth future features. The foundation model stays frozen, which is meant to preserve its semantic knowledge.

## Results
- On **WISER**, a new benchmark with **24** knowledge categories and **288** train tasks plus **288** test tasks, **GWM-MPC** reaches **0.87 test success**, versus **0.22 average** for VLA baselines.
- GWM-MPC gets **0.92 train success** and **0.87 test success**. The baseline average is **0.90 train success** and **0.22 test success**, so GWM keeps performance on seen tasks while sharply reducing the train-test generalization gap.
- Test-set success for named baselines is much lower: **InstructVLA 0.47**, **Wall-OSS 0.40**, **InternVLA-A1 0.26**, **π0.5 0.26**, **GR00T-N1.6 0.18**, **SmolVLA 0.08**, **π0 0.08**.
- GWM-MPC also posts **0.99 test grasp** and **0.88 test reach**, compared with baseline averages of **0.54** and **0.29**.
- The proposed action tokenizer matters: **GWM-MPC-AC** drops to **0.24 test success**, while full GWM-MPC stays at **0.87**.
- Zero-shot transfer across robot embodiment is strong in this benchmark: **GWM-MPC-xArm6** reports **0.83 test success** despite different action space, kinematics, and appearance. A retrieval upper bound, **GT-MPC**, reaches **0.93 test success**, which suggests the main bottleneck is scoring quality in the frozen foundation model space.

## Link
- [http://arxiv.org/abs/2604.11751v1](http://arxiv.org/abs/2604.11751v1)
