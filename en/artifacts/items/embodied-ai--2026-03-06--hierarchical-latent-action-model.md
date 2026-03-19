---
source: arxiv
url: http://arxiv.org/abs/2603.05815v1
published_at: '2026-03-06T01:59:07'
authors:
- Hanjung Kim
- Lerrel Pinto
- Seon Joo Kim
topics:
- latent-action-model
- hierarchical-policy
- skill-discovery
- actionless-video
- robot-learning
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Hierarchical Latent Action Model

## Summary
HiLAM aims to learn longer-horizon latent skills from **action-unlabeled videos**, rather than only recovering low-level actions between adjacent frames. It takes short-term action sequences extracted by an existing latent action model and further compresses them into variable-length high-level skills by chunking, for hierarchical robot policy pretraining.

## Problem
- Existing Latent Action Models (LAMs) mostly model **short-horizon frame transitions**. They can capture low-level motion, but often overlook the more important **long-horizon skill structure** in videos.
- This matters because training robots and world models requires large amounts of data, while **data with action labels is expensive and scarce**. There is plenty of unlabeled video, but if only short-term motion can be extracted, the higher-level behavioral information in it is wasted.
- Methods that define skills using fixed windows, fixed skill sets, or language alone struggle to handle the fact that **real skill durations are variable, execution speeds differ, and behaviors are diverse**.

## Approach
- The core idea is simple: first use a **pretrained inverse dynamics model (IDM)** to turn actionless videos into a sequence of low-level latent actions, then use a **hierarchical sequence model** to automatically split that sequence into segments, with each segment corresponding to a high-level latent skill.
- HiLAM uses **H-Net's dynamic chunking**: if adjacent token features differ greatly, a new segment is started at that position. This enables **automatic discovery of skill boundaries**, without manual annotation and without requiring fixed skill lengths.
- Training does three things: predict the next latent action (latent next-token prediction), use a **pretrained forward dynamics model (FDM)** to reconstruct future frames from the predicted actions in order to preserve “actionness,” and add chunk ratio regularization to avoid degenerate segmentation.
- After learning skills, the authors train a **hierarchical policy**: the high-level policy predicts latent skills from the current observation and language, and the low-level policy then predicts low-level actions from the observation and that skill; finally, only the low-level policy is fine-tuned to output real robot actions.
- This design reuses an existing LAM as the low-level extractor, making it computationally better suited for handling **long-horizon trajectories**.

## Results
- In data-efficiency experiments on **LIBERO-Long**, using only **10%** of expert demonstrations for fine-tuning, **BAKU = 23%** success rate, while **HiLAM = 45%**, nearly doubling it.
- On **LIBERO-Long**, with **50%** demonstrations, **HiLAM = 84%**, reaching a level comparable to **BAKU using 100% data**; with **100%** demonstrations, **HiLAM = 94%**, significantly higher than BAKU.
- The paper claims it **consistently outperforms** the strong baseline **BAKU** across all four suites: **LIBERO-Spatial / Object / Goal / Long**, but the excerpt does not provide the full numeric table for each suite.
- The LIBERO-Long ablation in **Table 1** shows that the best setting is **human video pretraining + stage-2 latent skill + stage-0 latent action**, with success rate **0.94**; corresponding numbers are **BAKU + human pretraining + z^0 latent action = 0.91**, and **HiLAM without large-scale pretraining = 0.67**.
- Under robot video pretraining, HiLAM is also effective: **z^1 skill + z^0 action = 0.90**, **z^2 skill + z^0 action = 0.90**; this indicates the method does not depend on a single data source.
- Non-hierarchical BAKU with latent conditioning also improves (e.g. **0.87 / 0.91**), but still trails the best HiLAM at **0.94**, supporting the authors’ claim that **high-level skills + hierarchical policy** is more effective.

## Link
- [http://arxiv.org/abs/2603.05815v1](http://arxiv.org/abs/2603.05815v1)
