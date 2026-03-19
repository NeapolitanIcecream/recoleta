---
source: arxiv
url: http://arxiv.org/abs/2603.12144v1
published_at: '2026-03-12T16:45:42'
authors:
- Mengfei Duan
- Hao Shi
- Fei Teng
- Guoqiang Zhao
- Yuheng Zhang
- Zhiyong Li
- Kailun Yang
topics:
- open-vocabulary-occupancy
- omnidirectional-perception
- 3d-scene-understanding
- mamba
- embodied-perception
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# O3N: Omnidirectional Open-Vocabulary Occupancy Prediction

## Summary
O3N proposes the first **purely visual, end-to-end** panoramic open-vocabulary 3D occupancy prediction framework, aiming to reconstruct geometry and scalable semantics simultaneously from a single 360° image. It primarily addresses panoramic distortion, long-range context modeling, and semantic alignment for unseen categories, and achieves SOTA on QuadOcc and Human360Occ.

## Problem
- Existing 3D occupancy prediction methods typically rely on limited-view inputs and closed category sets, making them difficult to meet the **360° safe perception** needs of embodied agents in the open world.
- Panoramic ERP images have **geometric distortion and non-uniform sampling**, which disrupt spatial continuity and increase the risk of semantic sparsity in distant regions and training overfitting.
- Under the open-vocabulary setting, alignment across the **pixel-voxel-text** tri-modal space can easily fail because training only sees base classes, leading to poor generalization to novel classes.

## Approach
- Proposes **O3N**: given a single panoramic RGB image and category text, it directly predicts open-vocabulary 3D occupancy; the paper claims it is the first purely visual end-to-end framework for this task.
- Uses **Polar-spiral Mamba (PsM)** to perform spiral scanning and dual-branch modeling on polar/cylindrical voxels. Put simply, it aggregates information from near to far in an order that better matches 360° geometry, then fuses this with Cartesian voxels to improve long-range context and spatial continuity modeling.
- Uses **Occupancy Cost Aggregation (OCA)** to first compute a cost volume measuring “how well voxel features match text features,” then performs spatial aggregation and category aggregation, instead of directly hard-aligning discrete features, thereby reducing open-vocabulary overfitting.
- Uses **Natural Modality Alignment (NMA)** for gradient-free text-prototype alignment: it repeatedly fuses text embeddings with semantic prototypes derived from pixel features to obtain a more consistent shared semantic space, alleviating the gap among pixel/voxel/text modalities.
- The framework can be trained on top of occupancy networks such as MonoScene and SGN, with losses consisting of semantic occupancy supervision, voxel-pixel alignment, and OCA loss.

## Results
- On **QuadOcc**, the paper reports improvements of **+2.21 mIoU** and **+3.01 Novel mIoU** over the baseline.
- On **Human360Occ**, the paper reports improvements of **+0.86 mIoU** and **+1.54 Novel mIoU** over the baseline.
- The QuadOcc results shown in Figure 1 indicate that O3N reaches **16.54 mIoU** and **21.16 Novel mIoU**, and the paper claims this is SOTA on that benchmark.
- The paper claims to outperform existing open-vocabulary occupancy methods on both panoramic occupancy benchmarks, **QuadOcc** and **Human360Occ**, and to **surpass some fully supervised methods**.
- In the dataset setup, QuadOcc treats **vehicle/road/building** as novel classes, accounting for about **68%** of all voxels; Human360Occ treats 7 classes as novel, accounting for about **75%**, indicating that the evaluation is fairly challenging in the open-vocabulary setting.
- The abstract also claims notable **cross-scene generalization** and **semantic scalability**, but the provided excerpt does not include more detailed full-table metrics broken down by dataset or model.

## Link
- [http://arxiv.org/abs/2603.12144v1](http://arxiv.org/abs/2603.12144v1)
