---
source: arxiv
url: http://arxiv.org/abs/2603.07083v1
published_at: '2026-03-07T07:41:28'
authors:
- Michael Hauri
- Friedemann Zenke
topics:
- model-based-rl
- world-models
- reconstruction-free-learning
- self-supervised-learning
- dreamer
- representation-learning
relevance_score: 0.34
run_id: materialize-outputs
language_code: en
---

# Dreamer-CDP: Improving Reconstruction-free World Models Via Continuous Deterministic Representation Prediction

## Summary
This paper proposes Dreamer-CDP, a reconstruction-free world model training method for model-based reinforcement learning under high-dimensional observations. It replaces pixel reconstruction with continuous deterministic representation prediction, and on Crafter is the first to raise this class of reconstruction-free Dreamer variants to performance close to, or even slightly above, standard Dreamer.

## Problem
- Existing world models such as Dreamer often rely on **pixel reconstruction** to learn representations, but this can make the representations focus excessively on visual details irrelevant to decision-making.
- Previous **reconstruction-free** alternatives usually rely on action prediction or view augmentation, but on sparse-reward, long-horizon tasks such as **Crafter** they lag significantly behind reconstruction-based Dreamer.
- This matters because if decoder-based reconstruction can be removed, world models may become more efficient, more focused on task-relevant information, and less computationally burdensome in complex environments.

## Approach
- The core idea is to first encode observations into a **continuous, deterministic embedding** `u_t`, then have the world model hidden state `h_t` predict its next-step representation `\hat{u}_t` instead of reconstructing the next-frame pixels.
- The training objective adds a **JEPA/BYOL-style** representation prediction loss: it uses **negative cosine similarity** to bring the predicted representation close to the true representation, and applies **stop-gradient** on the target branch to prevent collapse.
- Unlike the original Dreamer, Dreamer-CDP **removes the reconstruction loss**, but retains the reward, continuation, and Dreamer’s dynamics/representation KL alignment terms.
- Unlike some related methods, it **does not use an EMA target network**; instead, it lets the sequence model/predictor use a higher learning rate so the dynamics model approaches a fixed point more quickly.
- By design, it simultaneously satisfies **reconstruction-free, non-contrastive, no action prediction, no view augmentation**, learning the world model purely through internal representation prediction.

## Results
- On **Crafter**, Dreamer-CDP achieves a **Crafter score** of **16.2±2.1**. Compared with standard **DreamerV3’s 14.5±1.6**, this is in the same range, and the paper argues that it has **matched Dreamer**'s performance.
- Compared with prior reconstruction-free Dreamer variants, Dreamer-CDP is clearly stronger: **MuDreamer 7.3±2.6**, **DreamerPro 4.7±0.5**, while Dreamer-CDP reaches **16.2±2.1**.
- If the **CDP loss** is removed (equivalent to having no reconstruction and also no such prediction objective), the Crafter score drops to **3.2±1.2**, showing that continuous deterministic representation prediction is critical.
- If the reward head is not allowed to backpropagate into the world model, performance drops to **12.7±1.6**, indicating that reward learning helps, but is not the main source of gains.
- If the **dyn/rep KL alignment terms** are removed, performance drops to **6.3±1.9**, showing that **CDP is necessary but not sufficient**; Dreamer’s latent alignment mechanism must also work jointly.
- For cumulative reward, Dreamer-CDP reaches **9.8±0.4**, below Dreamer’s **11.7±1.9**, but above MuDreamer’s **5.6±1.6**; therefore, its main breakthrough is reflected in **Crafter score** rather than comprehensive superiority across all metrics.

## Link
- [http://arxiv.org/abs/2603.07083v1](http://arxiv.org/abs/2603.07083v1)
