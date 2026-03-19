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
- token-pruning
- embodied-ai
- robot-navigation
- spatio-temporal-modeling
relevance_score: 0.63
run_id: materialize-outputs
language_code: en
---

# History-Conditioned Spatio-Temporal Visual Token Pruning for Efficient Vision-Language Navigation

## Summary
This paper proposes a training-free visual token pruning method for vision-language navigation (VLN), using different compression strategies for the current view and historical memory, while preserving navigation performance as much as possible even under extremely high pruning rates. Its goal is to reduce the inference latency of VLA navigation models, bringing robots closer to real-time deployment.

## Problem
- This work addresses the problem that **VLA-driven VLN models are too computationally heavy at inference time to run low-latency closed-loop control on real robots**; this directly affects navigation responsiveness and deployment reliability.
- Existing visual token pruning methods mostly process single frames, **without explicitly leveraging the spatio-temporal structure of VLN, which depends on historical observations**, so they can easily lose critical information during long-horizon navigation.
- This problem matters because VLN is a core capability for embodied robots to execute natural-language navigation instructions, with applications in household assistance, office guidance, and search-and-rescue scenarios.

## Approach
- The method is a **training-free / plug-and-play** spatio-temporal visual token pruning framework that does not require retraining or modification of pretrained VLA models.
- For the **current frame**: it first estimates token importance using the similarity between [CLS] and patch tokens, then iteratively selects tokens with **Adaptive Maximal Marginal Relevance (A-MMR)**, balancing both importance and non-redundancy.
- For **historical frames**: it first uses the retained tokens from the current frame as queries to compute the relevance of each historical token to the current view; it then reweights the original importance with this relevance, preserving historical information that is both important and relevant to the current decision.
- Put simply, the core mechanism is: **preserve spatial coverage for the current view, retain only memory from past views that is most relevant to the current decision, and avoid redundant tokens**.
- Finally, the pruned tokens are fed into the original VLA projector and LLM to predict navigation actions, thereby reducing the computation required for long visual input sequences.

## Results
- On **R2R val-unseen** with **90% pruning** (retaining 72/729 tokens), the method achieves **SR 47.63, SPL 36.36, OS 68.46, NE 5.69**; compared with **SparseVLM** at **SPL 31.08**, **DivPrune** at **18.55**, and **VisPruner** at **29.27**, it is higher by **5.28, 17.81, and 7.09** points, respectively.
- On **RxR val-unseen** with **90% pruning**, the method achieves **SR 45.71, SPL 32.91, nDTW 47.69, NE 6.90**; compared with **SparseVLM 20.87 SPL**, **DivPrune 14.56**, and **VisPruner 25.34**, it is higher by **12.04, 18.35, and 7.57** points, respectively.
- In terms of latency, the paper claims that under **90% pruning**, CUDA inference latency drops from **231.34 ms** without pruning to **213.40 ms**; and it is additionally **6.09 / 7.31 / 10.96 ms** faster than **SparseVLM / DivPrune / VisPruner**, respectively.
- It also maintains a lead at lower pruning rates: for example, on **R2R with 80% pruning**, this paper reports **SPL 46.44**, higher than **SparseVLM 40.63**, **DivPrune 28.64**, and **VisPruner 43.92**; on **RxR with 80% pruning**, it reports **SPL 43.64**, higher than **30.10 / 23.92 / 40.15**.
- Ablation experiments show that both “semantic importance + diversity” are necessary: on **R2R with 90% pruning**, the full setting achieves **SPL 36.51**; diversity-only gives **36.18**, and semantics-only gives **27.80**, indicating that using only semantics leads to redundancy, while using only diversity drifts away from task-relevant regions.
- The paper also reports real-world deployment on a **Unitree Go2** quadruped robot, claiming reliable, low-latency instruction-following navigation, though the excerpt does not provide quantitative metrics for the robot experiments.

## Link
- [http://arxiv.org/abs/2603.06480v1](http://arxiv.org/abs/2603.06480v1)
