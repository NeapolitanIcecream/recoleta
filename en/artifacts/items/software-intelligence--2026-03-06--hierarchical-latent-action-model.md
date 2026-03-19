---
source: arxiv
url: http://arxiv.org/abs/2603.05815v1
published_at: '2026-03-06T01:59:07'
authors:
- Hanjung Kim
- Lerrel Pinto
- Seon Joo Kim
topics:
- latent-action-models
- hierarchical-learning
- skill-discovery
- robot-learning
- imitation-learning
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# Hierarchical Latent Action Model

## Summary
HiLAM aims to automatically discover high-level skills with variable durations from video-only data without action labels, rather than merely capturing fragmented short-term motions. It hierarchically compresses low-level latent actions extracted by an existing latent action model into latent skills, enabling stronger long-horizon pretraining for robotic control.

## Problem
- Existing Latent Action Models typically model changes only between adjacent or short-range frames. They are good at low-level motion but struggle to capture long-horizon, reusable high-level skills.
- Skills in real videos have non-fixed durations; if one forces fixed windows or a predefined skill set, behaviors that are essentially the same but executed at different speeds will be encoded as different representations.
- This matters because action annotation is expensive, while large amounts of unlabeled human/robot videos actually contain rich skill structure that, if leveraged, could improve long-horizon control and data efficiency.

## Approach
- First, a pretrained inverse dynamics model (IDM) is used to extract a sequence of low-level latent actions from unlabeled videos, turning “watching videos” into “looking at a sequence of latent action tokens.”
- On top of this, it introduces two-layer H-Net-style dynamic chunking: boundaries are determined automatically through feature dissimilarity between neighboring tokens, and variable-length segments of low-level latent actions are compressed into shorter high-level latent skill representations.
- The training objective has three parts: a next-latent-action prediction loss, a visual constraint using a pretrained forward dynamics model (FDM) for future-frame reconstruction, and a ratio regularizer to prevent degenerate chunking.
- After training, the chunked stage-wise representations are expanded back into a per-timestep skill sequence; then a hierarchical policy is trained: the high-level policy predicts latent skills, and the low-level policy predicts latent actions conditioned on observations + skills. Finally, the low-level policy is fine-tuned with a small amount of ground-truth actions to map to real robot actions.

## Results
- On the four LIBERO suites (Spatial/Object/Goal/Long), the paper claims HiLAM consistently outperforms the SOTA baseline BAKU; the figure does not provide exact per-suite values, but the qualitative conclusion is consistent superiority.
- On the hardest LIBERO-Long, with only **10%** expert demonstrations for fine-tuning, BAKU achieves a **23%** success rate while HiLAM reaches **45%**, nearly doubling it.
- On LIBERO-Long, with **50%** demonstrations, HiLAM reaches **84%**, roughly comparable to BAKU using **100%** of the data, indicating clearly higher data efficiency.
- On LIBERO-Long, with **100%** demonstrations, HiLAM reaches a **94%** success rate and significantly surpasses BAKU.
- Ablations show that without large-scale pretraining and training only the hierarchical policy, HiLAM achieves only **0.67** success rate; whereas the best setting (human video pretraining, latent skill using **stage-2**, latent action using **stage-0**) reaches **0.94**.
- A flat-policy BAKU with latent conditioning also improves, but the best result reaches only **0.91** (human pretraining, latent action=stage-0), still below HiLAM’s **0.94**; under robot-video pretraining, HiLAM’s best is about **0.90**, also outperforming most corresponding BAKU settings.

## Link
- [http://arxiv.org/abs/2603.05815v1](http://arxiv.org/abs/2603.05815v1)
