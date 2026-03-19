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
- self-supervised-learning
- hyperbolic-embeddings
- 3d-pretraining
- multiview-learning
relevance_score: 0.19
run_id: materialize-outputs
language_code: en
---

# Hyperbolic Multiview Pretraining for Robotic Manipulation

## Summary
This paper proposes HyperMVP, which uses hyperbolic space instead of Euclidean space for 3D multiview self-supervised pretraining to improve spatial perception, robustness, and generalization in robotic manipulation. It also constructs the large-scale 3D-MOV dataset and reports results outperforming strong baselines in both simulated and real-world settings.

## Problem
- Existing 3D visual pretraining for robotic manipulation is mostly conducted in **Euclidean** embedding spaces, which struggle to represent hierarchical and structured spatial relations, leading to insufficient scene understanding and poor generalization under perturbations.
- Real-world robotic deployment must handle viewpoint changes, environmental perturbations, and scene diversity; task-level multitask training alone often suffers performance degradation under these conditions.
- High-quality pretraining data is expensive, so beyond simply scaling data, it is also necessary to improve the modeling capacity of the representation space itself, enabling stronger spatial representations to be learned from the same amount of data.

## Approach
- Proposes **HyperMVP**: a 3D multiview self-supervised framework following a “pretrain-finetune” paradigm. It renders point clouds into five orthographic views, learns representations in a manner similar to MAE, but lifts the representations into hyperbolic space under the **Lorentz model**.
- Designs the **GeoLink encoder**: it first uses ViT to extract patch/CLS features from each view, then maps Euclidean features into hyperbolic space via the exponential map; afterward, it sends them back to Euclidean space via the logarithmic map to remain compatible with downstream robotic policy networks.
- To learn “structured” hyperbolic representations in an unsupervised manner, it uses two key constraints: **Top-K neighborhood rank correlation loss** to preserve patch neighborhood ranking consistency between Euclidean and hyperbolic spaces; and **entailment loss** to model hierarchical structure through local-global containment relations.
- The pretraining task does not only perform single-view reconstruction, but jointly uses **intra-view reconstruction** and **inter-view reconstruction**, so the model reconstructs the current view while also predicting the anchor view from other views, thereby learning cross-view 3D consistency.
- Builds the **3D-MOV** dataset: containing 200,052 point cloud samples and about 1M multiview images, covering four categories of 3D data including object, indoor scene, and tabletop, to support large-scale pretraining.

## Results
- On **COLOSSEUM**, the paper claims that HyperMVP achieves an **average 33.4% improvement** over the “previous best baseline” under all perturbation settings.
- In the most challenging **All Perturbations** setting on COLOSSEUM, the paper reports a relative performance of **2.1× gain**.
- In **RLBench** multitask manipulation, the authors state that combining the GeoLink encoder with RVT significantly outperforms **RVT from scratch** and models pretrained in Euclidean space, but the provided excerpt **does not include specific numerical tables**.
- In real-world experiments, the authors claim that HyperMVP shows **strong real-world effectiveness** while maintaining the same generalization advantages observed in simulation; the excerpt **does not provide specific success-rate numbers**.
- In terms of pretraining data scale, 3D-MOV contains **180K** Objaverse-XL object point clouds, **6,052** fine-grained indoor scene point clouds, **3,999** vanilla tabletop point clouds, and **10,001** crowd tabletop point clouds, totaling **200,052** point clouds and about **1M** rendered images.
- At the method level, the authors claim this is the **first** framework to apply 3D multiview hyperbolic pretraining to robotic manipulation, and that its view-decoupled design allows finetuning to scale to **any number of input views**.

## Link
- [http://arxiv.org/abs/2603.04848v1](http://arxiv.org/abs/2603.04848v1)
