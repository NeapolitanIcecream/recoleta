---
source: arxiv
url: http://arxiv.org/abs/2604.09244v1
published_at: '2026-04-10T11:58:39'
authors:
- Zihao Zheng
- Sicheng Tian
- Zhihao Mao
- Lingyue Zhang
- Chenyue Li
- Ziyun Zhang
- Hong Gao
- Yuchen Huang
- Yutong Xu
- Guojie Luo
- Xiang Chen
topics:
- vision-language-action
- token-pruning
- multimodal-robotics
- 3d-perception
- inference-acceleration
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# 2D or 3D: Who Governs Salience in VLA Models? -- Tri-Stage Token Pruning Framework with Modality Salience Awareness

## Summary
This paper studies token pruning for vision-language-action models that use both 2D images and 3D point clouds. The main claim is that pruning should follow how 2D and 3D salience changes across preprocessing, semantic reasoning, and action rollout, which gives faster inference with small accuracy loss.

## Problem
- Multi-visual-modal VLA models add 3D tokens to 2D inputs, which raises sequence length and slows inference. The paper says these models often run at **3 to 5 Hz**, below the roughly **20 to 30 Hz** needed for real-time control.
- Existing token pruning methods were built for 2D-only VLA models, so they miss how useful **2D and 3D tokens differ by modality, semantic region, and time step**.
- In robot control, pruning the wrong tokens can hurt task success. The paper shows naive pruning can cause large drops, such as **55.00% to 6.67%** on Close Box when pruning 2D tokens at **50%**.

## Approach
- The method builds a **tri-stage token pruning framework** around the three stages of MVLA inference: data preprocessing, semantic synthesis, and action iteration.
- In stage 1, it measures modality salience from the model's final-layer features using **L1 norms** and computes separate salience scores for **2D** and **3D** tokens. These scores set different pruning thresholds for the two modalities.
- In stage 2, it groups patches into semantic sets such as **background, robot, and object** using attention-based clustering, then measures how much 2D and 3D matter inside each set. The paper also decomposes 3D attention into overlapping and unique parts to estimate the unique value of 3D tokens.
- In stage 3, it tracks how modality salience changes over action steps and adds **temporal segmentation plus salience prediction** so pruning can adapt during execution.
- The final pruning policy combines these three signals to choose which 2D and 3D tokens to keep.

## Results
- The abstract claims **up to 2.55× inference speedup** with **minimal accuracy loss** and only **5.8% overhead**.
- In the paper's stage-1 analysis on **RLBench** tasks with the **MLA** model, pruning **3D** tokens is often less harmful than pruning **2D** tokens, which supports modality-aware pruning. Example: on **Close Box**, baseline success rate is **55.00%**; with **50% 2D pruning** it drops to **6.67%**; with **50% 3D pruning** it is **40.00%**.
- Some tasks improve after 3D pruning in the naive study. Examples at **50% pruning**: **Close Fridge** goes from **56.66%** to **70.00%**, **Close Laptop** from **80.00%** to **90.00%**, and **Sweep Dustpan** from **66.67%** to **96.67%**.
- The stage-1 salience metric reports much higher 2D salience than 3D salience across listed tasks, with examples such as **90.16% vs 9.84%** on Close Box, **81.47% vs 18.53%** on Close Fridge, and **90.38% vs 9.62%** on Close Laptop.
- For stage 2 and stage 3, the excerpt gives qualitative claims: 3D salience is higher than 2D in **robot** and **object** semantic regions, and modality salience changes over time during manipulation. The excerpt does not provide full end-to-end benchmark tables for these stages beyond the abstract-level speedup claim.

## Link
- [http://arxiv.org/abs/2604.09244v1](http://arxiv.org/abs/2604.09244v1)
