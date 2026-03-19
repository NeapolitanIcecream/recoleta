---
source: arxiv
url: http://arxiv.org/abs/2603.04848v1
published_at: '2026-03-05T06:04:01'
authors:
- Jin Yang
- Ping Wei
- Yixin Chen
topics:
- robotic-manipulation
- self-supervised-pretraining
- hyperbolic-representation-learning
- multiview-3d
- sim2real
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Hyperbolic Multiview Pretraining for Robotic Manipulation

## Summary
This paper proposes HyperMVP, a method that extends 3D multiview self-supervised pretraining for robotic manipulation from Euclidean space to hyperbolic space in order to learn more structured visual representations. It also constructs the large-scale 3D-MOV dataset and reports stronger generalization and robustness in both simulation and real-world scenarios.

## Problem
- Existing visual pretraining for robotic manipulation mostly learns representations in **Euclidean space**, whose flat geometry makes it difficult to express hierarchical and structured spatial relations.
- This limits the robot’s spatial perception and generalization ability in **scene perturbations, cross-task settings, and real environments**, which are exactly what matter for real-world deployment.
- Simply scaling up data is costly, so a **more efficient way to improve representation quality** is needed rather than just continuing to add more data.

## Approach
- Proposes **HyperMVP**: first performs self-supervised pretraining on five-view orthographic images rendered from 3D point clouds, then jointly finetunes the pretrained encoder with **RVT** for robotic manipulation policy learning.
- The core mechanism is simple: it first uses a ViT/MAE-style encoder to extract multiview features, then “lifts” these Euclidean features into **hyperbolic space (Lorentz model)** so the representations can more easily organize hierarchical and structural relations.
- Designs a **GeoLink encoder** and learns hyperbolic representations with two self-supervised constraints: **Top-K neighborhood rank correlation loss** preserves neighbor order consistency between Euclidean and hyperbolic spaces, and **entailment loss** encourages global and local features to form a partially hierarchical inclusion relationship.
- The pretraining task includes not only conventional **single-view reconstruction**, but also **cross-view reconstruction**, where the model predicts the anchor view from other views to strengthen 3D and multiview consistency.
- Builds **3D-MOV** as the pretraining data: a total of **200,052** 3D point clouds and about **1 million** rendered images, covering four categories including objects, indoor scenes, and tabletop scenes; moreover, the method can scale to **an arbitrary number of input views** during finetuning.

## Results
- On the **COLOSSEUM** generalization benchmark, the authors claim that HyperMVP achieves an **average 33.4% improvement** over the previous best baseline under all perturbation settings.
- In the most difficult **All Perturbations** setting on COLOSSEUM, the authors report a **2.1×** performance gain, indicating stronger robustness to complex environmental perturbations.
- In **RLBench** multitask manipulation, RVT combined with the **GeoLink encoder** shows significant improvements over both **RVT trained from scratch** and methods using **Euclidean-space representations**, but the abstract/excerpt **does not provide specific numbers**.
- In **real-world experiments**, the paper claims that HyperMVP also shows strong effectiveness while maintaining comparable or better generalization; however, the excerpt **does not provide clear quantitative metrics**.
- In terms of data scale, the pretraining **3D-MOV** dataset contains **200,052** point clouds and about **1M** multiview images; implementation-wise, pretraining uses **100 epochs**, a mask ratio of **0.75**, image resolution **224×224**, and **5** orthographic views per point cloud.

## Link
- [http://arxiv.org/abs/2603.04848v1](http://arxiv.org/abs/2603.04848v1)
