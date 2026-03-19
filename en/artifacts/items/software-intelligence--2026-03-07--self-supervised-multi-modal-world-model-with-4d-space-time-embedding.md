---
source: arxiv
url: http://arxiv.org/abs/2603.07039v1
published_at: '2026-03-07T05:13:20'
authors:
- Lance Legel
- Qin Huang
- Brandon Voelker
- Daniel Neamati
- Patrick Alan Johnson
- Favyen Bastani
- Jeff Rose
- James Ryan Hennessy
- Robert Guralnick
- Douglas Soltis
- Pamela Soltis
- Shaowen Wang
topics:
- world-model
- self-supervised-learning
- multimodal-learning
- spatiotemporal-embedding
- earth-observation
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Self-Supervised Multi-Modal World Model with 4D Space-Time Embedding

## Summary
DeepEarth proposes a self-supervised multimodal world model, using Earth4D to unify positions and time on Earth into learnable representations. Its core claim is that strong representations can be learned using only spatiotemporal coordinates plus a small amount of semantic information, and that it can outperform heavier pretrained multimodal baselines on ecological forecasting tasks.

## Problem
- A method is needed to represent space and time uniformly at a **global scale** for learning multimodal patterns in Earth observation data.
- Existing methods struggle to simultaneously cover **very large spatial ranges, long time spans**, and **high precision**, while also remaining scalable in memory and computation.
- This matters because ecological forecasting, environmental monitoring, and world-model construction all depend on stable spatiotemporal representations; if the representation is inadequate, it is hard to generalize across different locations, seasons, and events.

## Approach
- Proposes **Earth4D**: mapping continuous `(latitude, longitude, elevation, time)` into 4D spatiotemporal positional embeddings, extending multi-resolution hash encoding.
- Instead of using a full 4D grid directly, Earth4D combines four parallelizable 3D grids: `xyz`, `xyt`, `yzt`, and `xzt`, to represent spatiotemporal structure more efficiently.
- In **DeepEarth**, Earth4D embeddings are fused with outputs from modality encoders such as vision, language, and sensors, then used as tokens input to an autoencoder and trained self-supervised via **masked reconstruction**.
- To reduce hash collisions, the authors introduce **learned hash probing**, allowing the model to learn better hash index assignments and thereby improve representation quality.
- In the LFMC experiments, the model makes predictions using only `(x,y,z,t) + species`, validating the expressive power of the spatiotemporal encoding itself.

## Results
- On **Globe-LFMC 2.0** (official split: **76,467** training, **13,297** test), **Earth4D (Learned Hashing)** achieves **MAE 11.7pp, RMSE 18.7pp, R² 0.783**.
- Compared with the pretrained multimodal baseline **Galileo** (inputs include remote sensing, weather, terrain, coordinates, and species), which achieves **MAE 12.6pp, RMSE 18.9pp, R² 0.72**, Earth4D performs better despite using fewer inputs, with an absolute **0.9pp** reduction in MAE and a **0.063** improvement in R².
- The error distribution plot shows a **median absolute error of 7.1pp** on the test set, and claims that temporal forecasting can track seasonal changes from **2017–2023** well.
- Compared with standard hash encoding **without learned probing** (**RMSE 26.0pp, MAE 16.6pp, R² 0.58**), adding learned probing improves performance to **18.7pp / 11.7pp / 0.783**, corresponding to a **29.5%** reduction in MAE and a **35.0%** increase in R².
- Under an extreme compression setting, the model is reduced from **800M parameters** to **5M parameters** (**99.3%** reduction, **93%** memory reduction), while still achieving **MAE 15.0pp, R² 0.668**; it also claims **4× faster training** and **14.7% higher R²** than the 800M no-probing baseline.
- The appendix also claims that learned probing reduces validation loss on RGB reconstruction by **18%**, and reduces hash collisions by **33%** for the **1M points** setting.

## Link
- [http://arxiv.org/abs/2603.07039v1](http://arxiv.org/abs/2603.07039v1)
