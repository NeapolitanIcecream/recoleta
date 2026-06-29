---
source: arxiv
url: http://arxiv.org/abs/2604.21241v1
published_at: '2026-04-23T03:17:50'
authors:
- Dachong Li
- ZhuangZhuang Chen
- Jin Zhang
- Jianqiang Li
topics:
- vision-language-action
- robot-manipulation
- spatial-grounding
- flow-matching
- libero-benchmark
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# CorridorVLA: Explicit Spatial Constraints for Generative Action Heads via Sparse Anchors

## Summary
CorridorVLA adds explicit spatial constraints to vision-language-action policies by predicting a few future end-effector movement anchors and using them to shape the action loss. On LIBERO and LIBERO-Plus, this gives consistent gains for both SmolVLA and GR00T with little architectural change.

## Problem
- Many VLA models pass spatial guidance through latent or visual features, so the action head gets location and motion information indirectly.
- In robot manipulation, generated action trajectories can drift away from plausible spatial progress, especially under stochastic generative heads such as flow matching.
- This matters because better spatial guidance can raise task success on long-horizon and contact-heavy manipulation benchmarks such as LIBERO and LIBERO-Plus.

## Approach
- The model predicts **sparse spatial anchors**: a small set of future end-effector 3D delta-positions at selected time steps in an action chunk.
- These anchors define a **corridor** around the target spatial evolution. If a generated trajectory goes outside that tolerance region, the loss pushes it back; if it stays inside, a consistency term still refines it.
- The action output is extended with end-effector delta-position fields (`extra-A`) so the action head and anchor predictor use the same physical quantity.
- Training combines three parts: the base flow-matching loss, an anchor prediction loss, and a corridor regularizer with a buffer term plus an in-corridor cumulative consistency term, weighted more at lower noise levels.
- The method is lightweight: the paper uses `K=3` anchor tokens and keeps the rest of the backbone and training setup mostly unchanged.

## Results
- **LIBERO, SmolVLA:** success rate rises from **86.5%** to **90.95%** for **SmolVLA-Corr**, a gain of **4.45 points**. Category scores move from **72.0/89.0/87.0/98.0** to **85.2/90.8/95.8/92.0** for Long/Goal/Object/Spatial.
- **LIBERO-Plus, SmolVLA:** success rate rises from **45.37%** to **57.74%**, a gain of **12.37 points** (described as **12.4%** in the text). Per-category scores move from **46.53/35.89/66.2/32.85** to **49.27/55.27/72.36/54.04**.
- **LIBERO-Plus, GR00T:** success rate rises from **75.23%** to **83.21%** for **GR00T-Corr**, a gain of **7.98 points**. Per-category scores move from **62.21/68.54/84.55/85.64** to **74.55/85.75/88.4/84.14**.
- **Anchor target choice:** predicting **delta-positions** beats absolute positions on LIBERO 4-in-1, with average success **87.5%** vs **86.5%** for absolute positions and **86.5%** for the base model.
- **Combining components:** on LIBERO, `merge` reaches **89.0%**, `+L_buf` reaches **89.5%**, `+L_cons` reaches **90.4%**, and the full corridor loss reaches **90.95%**, showing both corridor terms help.
- The paper claims the added compute cost is negligible because the method mainly adds **3 future-state prediction tokens** and changes the training objective.

## Link
- [http://arxiv.org/abs/2604.21241v1](http://arxiv.org/abs/2604.21241v1)
