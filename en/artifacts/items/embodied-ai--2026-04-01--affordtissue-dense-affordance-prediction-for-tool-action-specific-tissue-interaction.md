---
source: arxiv
url: http://arxiv.org/abs/2604.01371v1
published_at: '2026-04-01T20:29:54'
authors:
- Aiza Maksutova
- Lalithkumar Seenivasan
- Hao Ding
- Jiru Xu
- Chenhao Yu
- Chenyan Jing
- Yiqing Shen
- Mathias Unberath
topics:
- surgical-robotics
- affordance-prediction
- vision-language
- dense-heatmap-prediction
- safe-manipulation
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# AffordTissue: Dense Affordance Prediction for Tool-Action Specific Tissue Interaction

## Summary
AffordTissue predicts dense heatmaps of safe tissue interaction regions for a specific surgical tool and action before contact happens. The paper frames this as a safety layer and policy input for surgical automation in cholecystectomy.

## Problem
- Current surgical learning systems and VLA-style models can imitate actions, but they do not show where a tool should safely interact with tissue for a given action.
- Semantic segmentation marks anatomy, not action-specific interaction zones, so it cannot answer where a hook should dissect or where a clipper should clip.
- This matters because clinical deployment needs controllable, inspectable spatial guidance and a way to stop early if the tool moves toward unsafe tissue.

## Approach
- The model takes a short text prompt with a surgical triplet `{surgery type, tool type, action type}` and a temporal video window of 256 past frames with stride 8, about 10.6 seconds of context.
- A frozen SigLIP 2 text encoder embeds the prompt, and a frozen Video Swin Transformer encodes tool motion and tissue dynamics from the video.
- A DiT-style decoder with adaptive layer normalization (AdaLN) fuses the text and video embeddings and predicts per-pixel logits for a dense affordance heatmap on the target frame.
- Training uses manually annotated safe interaction polygons converted into Gaussian-centered heatmaps. The dataset has 15,638 clips from 103 cholecystectomy videos and covers 6 tool-action pairs across 4 instruments: hook, grasper, scissors, and clipper.
- The paper also introduces this dataset as the first benchmark for tissue affordance prediction in this setting.

## Results
- On the main benchmark, AffordTissue reports DICE **0.124**, PCK@0.05 **0.517**, PCK@0.1 **0.667**, HD **79.763 px**, and ASSD **20.557 px**.
- Against baselines, ASSD improves from **60.184 px** for **Molmo-VLM** to **20.557 px** for AffordTissue, and from **81.138 px** for **SAM3** to **20.557 px**. Qwen-VLM (8B) reports **111.271 px** ASSD.
- Boundary alignment is much stronger than the baselines: PCK@0.05 is **0.517** for AffordTissue versus **0.128** for SAM3, **0.095** for Molmo-VLM, and **0.031** for Qwen-VLM (8B).
- The paper states the strongest competitor, Molmo-VLM, has **192.76%** worse ASSD and **62.34%** worse HD relative to AffordTissue.
- Ablations show the language signal is important: removing the language encoder raises ASSD from **20.557** to **43.135 px** and HD from **79.763** to **170.482 px**.
- Conditioning inputs matter: removing the tool specification increases ASSD to **27.302 px**, removing the action increases ASSD to **22.087 px**, and removing previous frames increases ASSD to **24.973 px**. Replacing AdaLN with cross-attention raises ASSD to **28.736 px**.

## Link
- [http://arxiv.org/abs/2604.01371v1](http://arxiv.org/abs/2604.01371v1)
