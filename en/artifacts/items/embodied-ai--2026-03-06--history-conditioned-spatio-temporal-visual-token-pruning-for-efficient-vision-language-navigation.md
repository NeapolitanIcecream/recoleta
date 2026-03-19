---
source: arxiv
url: http://arxiv.org/abs/2603.06480v1
published_at: '2026-03-06T17:03:16'
authors:
- Qitong Wang
- Yijun Liang
- Ming Li
- Tianyi Zhou
- Christopher Rasmussen
topics:
- vision-language-navigation
- vision-language-action
- token-pruning
- spatio-temporal-reasoning
- efficient-inference
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# History-Conditioned Spatio-Temporal Visual Token Pruning for Efficient Vision-Language Navigation

## Summary
This paper proposes a **training-free spatio-temporal visual token pruning** method for vision-language navigation (VLN) that reduces inference latency while preserving navigation performance as much as possible, without modifying a pretrained VLA model. The core idea is to apply different pruning strategies to the current frame and historical frames: the current frame preserves spatial coverage, while historical frames are compressed spatio-temporally according to their relevance to the current task.

## Problem
- Vision-Language-Action (VLA) models perform strongly in VLN, but Transformers contain many visual tokens, leading to high inference latency that makes it difficult to satisfy the needs of **real-time closed-loop navigation** in robotics.
- Existing visual token pruning methods are mostly designed for single frames or general vision models, and **do not explicitly leverage VLN's dependence on historical observations and spatio-temporal relationships**.
- Under high pruning rates, if one considers only saliency or only text relevance, it is easy to retain **redundant but similar** tokens while losing complementary information that is critical for navigation decisions.

## Approach
- First compute a base importance score for all visual patches: use the cosine similarity between the global `[CLS]` token in the visual encoder and each patch token as that patch's saliency score.
- For the **current frame**, use adaptive Maximal Marginal Relevance (A-MMR) to iteratively select tokens: at each step, choose tokens that are both **important and different from already selected tokens**. In simple terms, this preserves key targets and diverse background content at the same time, avoiding duplication.
- For **historical frames**, first use the pruned tokens from the current frame as queries, compute the maximum similarity between each historical token and the current view, and then multiply this relevance by the base importance to obtain a new score.
- Then apply the same A-MMR procedure to historical tokens to obtain a **compact yet information-rich memory pool**, which is finally passed into the projection layer and LLM to predict navigation actions.
- The whole method **requires no retraining and no modification of the pretrained model**, and can be directly inserted into existing VLA navigation systems.

## Results
- On **R2R val-unseen** with **90% pruning** (retaining 72/729 tokens), the method achieves **SR 47.63, SPL 36.36, OS 68.46, NE 5.69**; compared with **SparseVLM 31.08 SPL**, **DivPrune 18.55 SPL**, and **VisPruner 29.27 SPL**, SPL improves by **5.28, 17.81, and 7.09** points, respectively.
- On **RxR val-unseen** with **90% pruning**, the method achieves **SR 45.71, SPL 32.91, nDTW 47.69, NE 6.90**; compared with **SparseVLM 20.87 SPL**, **DivPrune 14.56 SPL**, and **VisPruner 25.34 SPL**, SPL improves by **12.04, 18.35, and 7.57** points, respectively.
- In terms of latency, the paper states that under **90% pruning**, CUDA inference latency drops from **231.34 ms** without pruning to **213.40 ms**, and is further faster than **SparseVLM, DivPrune, and VisPruner** by **6.09 ms, 7.31 ms, and 10.96 ms**.
- Compared with the unpruned model, performance still declines at 90% pruning, but remains relatively robust: for example, **R2R SPL drops from 49.66 to 36.36**, and **RxR SPL drops from 47.26 to 32.91**, indicating that this method preserves task-relevant information better than existing pruning approaches under extreme compression.
- Ablation experiments (R2R) show that the combination of "semantic importance + diversity" is most effective: under **90% pruning**, the full setting reaches **SPL 36.51**, outperforming diversity-only at **36.18** and significantly outperforming semantic-only at **27.80**; this shows that considering both "importance" and "redundancy reduction" is key.
- The paper also reports real-world deployment on a **Unitree Go2 quadruped robot**, claiming reliable, low-latency instruction-following navigation, but the excerpt **does not provide quantitative real-robot metrics**.

## Link
- [http://arxiv.org/abs/2603.06480v1](http://arxiv.org/abs/2603.06480v1)
