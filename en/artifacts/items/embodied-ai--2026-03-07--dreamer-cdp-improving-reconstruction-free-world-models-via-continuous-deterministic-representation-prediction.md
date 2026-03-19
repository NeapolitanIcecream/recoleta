---
source: arxiv
url: http://arxiv.org/abs/2603.07083v1
published_at: '2026-03-07T07:41:28'
authors:
- Michael Hauri
- Friedemann Zenke
topics:
- model-based-rl
- world-model
- dreamer
- self-supervised-learning
- reconstruction-free
relevance_score: 0.38
run_id: materialize-outputs
language_code: en
---

# Dreamer-CDP: Improving Reconstruction-free World Models Via Continuous Deterministic Representation Prediction

## Summary
Dreamer-CDP proposes a **reconstruction-free** world model training method that replaces pixel reconstruction with continuous deterministic representation prediction, raising the performance of this class of methods on Crafter to be comparable with Dreamer. The core conclusion is: predicting only internal discrete states is not enough, but after adding JEPA-style continuous representation prediction, an effective world model can be learned without reconstruction.

## Problem
- Existing Dreamer-style MBRL methods usually rely on **pixel reconstruction** to learn representations, but this can make the representation focus excessively on task-irrelevant visual details.
- Existing reconstruction-free alternatives (such as action prediction and view augmentation) lag significantly behind reconstruction-based Dreamer on long-horizon, sparse-reward benchmarks like **Crafter**.
- This matters because if decoding/reconstruction objectives can be removed, world models may become more efficient, more focused on task-relevant information, and impose a lower computational burden in complex visual environments.

## Approach
- Split DreamerV3’s observation encoding into two parts: first map the image to a **continuous deterministic embedding** `u_t`, then have a stochastic encoder combine it with the hidden state to produce the latent variable `z_t`.
- Remove the original **observation reconstruction loss** and add a JEPA/BYOL-style prediction head that uses the hidden state `h_t` to predict the future continuous representation `\hat{u}_t = g(h_t)`.
- Use **negative cosine similarity** as the training objective to align the predicted representation with the true representation: `L_CDP = -cos(SG(u_t), \hat{u}_t)`; the target branch stops gradients to avoid collapse.
- Retain Dreamer’s reward, continuation, and `L_dyn/L_rep` alignment terms; the authors also stabilize training by giving the sequence model/predictor a higher learning rate instead of using an EMA target network.
- Intuitively, this method does not try to “reconstruct pixels,” but to “predict the next high-level feature,” enabling the model to learn abstract dynamics that are more useful for control.

## Results
- On **Crafter**, Dreamer-CDP achieves a **16.2 ± 2.1** Crafter score, roughly on par with reconstruction-based **DreamerV3 14.5 ± 1.6**; Dreamer with prioritized experience replay reaches **19.4 ± 1.6**.
- Compared with existing reconstruction-free methods, Dreamer-CDP is clearly stronger: **MuDreamer 7.3 ± 2.6**, **DreamerPro 4.7 ± 0.5**, while Dreamer-CDP reaches **16.2 ± 2.1**.
- If `L_CDP` is removed (equivalent to having no reconstruction and no continuous representation prediction), performance drops to **3.2 ± 1.2**, showing that continuous deterministic representation prediction is critical.
- If gradients from the reward prediction head to the world model are removed, the score becomes **12.7 ± 1.6**, indicating that reward learning helps, but is not the main source of performance.
- If the `L_dyn/L_rep` alignment terms are removed, performance drops to **6.3 ± 1.9**, showing that **CDP itself is necessary but not sufficient** and still requires Dreamer’s latent alignment mechanism.
- In terms of cumulative reward, Dreamer-CDP reaches **9.8 ± 0.4**, below Dreamer’s **11.7 ± 1.9** but above MuDreamer’s **5.6 ± 1.6**; experiments are based on **1M environment steps**, **a single Nvidia V100**, and **n=7**.

## Link
- [http://arxiv.org/abs/2603.07083v1](http://arxiv.org/abs/2603.07083v1)
