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
- 3d-occupancy-prediction
- open-vocabulary
- omnidirectional-vision
- embodied-ai
- mamba
- scene-understanding
relevance_score: 0.29
run_id: materialize-outputs
language_code: en
---

# O3N: Omnidirectional Open-Vocabulary Occupancy Prediction

## Summary
O3N proposes the first framework for end-to-end open-vocabulary 3D occupancy prediction using only a single panoramic RGB image, aiming to recover both geometry and scalable semantics in 360° scenes. By adapting a 3D representation to panoramic geometry, voxel-text cost aggregation, and gradient-free modality alignment, it improves generalization to unseen categories and across scenes.

## Problem
- Existing 3D occupancy prediction methods mostly rely on limited-view inputs and closed category sets, making them difficult to support safe and complete perception for embodied agents in the open world.
- Panoramic images use ERP projection, which introduces polar discontinuities, geometric distortion, and non-uniform sampling, making 3D geometric reconstruction and semantic alignment more difficult.
- Directly performing “pixel-voxel-text” feature alignment can easily overfit to seen categories, thereby weakening open-vocabulary recognition ability for novel categories.

## Approach
- Proposes **O3N**: the first **purely visual, end-to-end** panoramic open-vocabulary occupancy prediction framework, taking a single panoramic RGB image and category text as input.
- Uses **Polar-spiral Mamba (PsM)** to scan polar/cylindrical voxels in a spiral manner, and fuses them with cubic voxels, to more naturally model 360° spatial continuity and long-range context.
- Uses **Occupancy Cost Aggregation (OCA)** to first compute similarities between voxel embeddings and text embeddings, forming a voxel-text “cost volume,” then performs spatial aggregation and category aggregation, rather than rigidly aligning discrete features directly.
- Uses **Natural Modality Alignment (NMA)** for gradient-free text-prototype alignment: it uses EMA to obtain seen-class prototypes, and iteratively updates text/prototypes via a random-walk-style process to mitigate the modality gap among pixels, voxels, and text.
- During training, novel categories are unified as unknown; only base-class semantic supervision is used, and optimization jointly combines occupancy loss, voxel-pixel alignment loss, and OCA loss.

## Results
- The paper claims **state-of-the-art** performance on the two panoramic occupancy benchmarks **QuadOcc** and **Human360Occ**.
- On **QuadOcc**, O3N improves over the baseline by **+2.21 mIoU** and **+3.01 Novel mIoU**; Figure 1 also reports **16.54 mIoU** and **21.16 Novel mIoU**.
- On **Human360Occ**, O3N improves over the baseline by **+0.86 mIoU** and **+1.54 Novel mIoU**.
- The paper emphasizes that it not only outperforms existing open-vocabulary occupancy methods, but also **surpasses some fully supervised methods**, though the current excerpt does not provide the final numbers from all comparison tables.
- The data setup is fairly challenging: in **QuadOcc**, voxels designated as novel categories account for about **68%**; in **Human360Occ**, novel categories account for about **75%**, and some base categories account for **less than 1%**.
- In terms of benchmark scale, **QuadOcc** uses a **64×64×8** voxel grid with **6** semantic classes plus empty; **Human360Occ** uses **10** semantic classes plus empty, and includes same-city / cross-city evaluation splits.

## Link
- [http://arxiv.org/abs/2603.12144v1](http://arxiv.org/abs/2603.12144v1)
