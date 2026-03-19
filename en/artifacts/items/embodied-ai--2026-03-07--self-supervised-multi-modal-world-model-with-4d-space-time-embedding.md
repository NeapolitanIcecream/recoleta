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
- spatiotemporal-encoding
- earth-observation
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# Self-Supervised Multi-Modal World Model with 4D Space-Time Embedding

## Summary
DeepEarth proposes a self-supervised multimodal world model and introduces Earth4D, a planetary-scale 4D spatiotemporal positional encoder, to learn unified representations of Earth observation data. Its core claim is that, using only spatiotemporal coordinates and a small amount of metadata, it can outperform baseline models that use more modalities and larger pre-training datasets on ecological forecasting tasks.

## Problem
- Existing Earth observation/world models struggle to represent continuous 4D spatiotemporal information while simultaneously operating at **global scale, long time horizons, and high spatial-temporal precision**.
- Multimodal Earth data (images, text, sensors, remote sensing) have complex distributions, and without strong spatiotemporal inductive bias, unified modeling and prediction are limited.
- This matters because ecological forecasting and disaster risk assessment (such as wildfire-related vegetation moisture content) depend on accurately modeling “what will happen, where, and when.”

## Approach
- Proposes **Earth4D**: extending traditional 3D multi-resolution hash encoding to 4D by using four parallelizable 3D grids (xyz, xyt, yzt, xzt) to approximately model the joint spatiotemporal structure of (latitude, longitude, elevation, time).
- Each grid uses a multi-resolution hash table, allowing coverage of **planetary scale, across centuries** under a fixed memory budget, and claims to achieve **sub-meter, sub-second** precision.
- DeepEarth fuses Earth4D spatiotemporal embeddings with outputs from modality encoders (such as vision/language encoders) into tokens, and performs **masked reconstruction**-style self-supervised training in an autoencoder context window to learn joint distributions and support generative reconstruction/simulation.
- To mitigate hash collisions, the authors add **learned hash probing**, enabling the model to learn better hash assignments from candidate indices, improving representation efficiency and downstream performance.

## Results
- On the **Globe-LFMC 2.0** ecological forecasting benchmark, Earth4D achieves **MAE 11.7pp, RMSE 18.7pp, R² 0.783** for **Live Fuel Moisture Content** prediction.
- Compared with the baseline **Galileo (pre-trained)**, whose inputs include **remote sensing imagery + weather + terrain + (x,y,z,t) + species type** and achieves **MAE 12.6pp, RMSE 18.9pp, R² 0.72**, Earth4D performs better using only **(x,y,z,t) + species name**.
- The test set contains **13,297** samples; the figure reports a median absolute error of **7.1pp**, and shows good tracking of seasonal variation over the **2017–2023** period.
- Ablation results show that standard hash encoding without learned probing yields **RMSE 26.0pp, MAE 16.6pp, R² 0.58**; adding learned probing improves this to **RMSE 18.7pp, MAE 11.7pp, R² 0.783**, i.e. a **29.5% reduction in MAE** and a **35.0% increase in R²**.
- An extreme compressed version reduces the model from **800M parameters** to **5M parameters** (**99.3%** reduction, hash capacity 2^14), yet still achieves **MAE 15.0pp / R² 0.668**, with **R² 14.7% higher** than the 800M no-probing baseline, while delivering **4× faster training** and **93% lower memory usage**.
- The appendix also claims that, on an RGB reconstruction task, learned probing further reduces validation loss by **18%**; and attributes the performance gains to a **33% reduction in hash collisions under a 1M-point simulation**.

## Link
- [http://arxiv.org/abs/2603.07039v1](http://arxiv.org/abs/2603.07039v1)
