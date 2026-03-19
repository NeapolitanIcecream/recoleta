---
source: arxiv
url: http://arxiv.org/abs/2603.04553v1
published_at: '2026-03-04T19:36:08'
authors:
- Tal Daniel
- Carl Qi
- Dan Haramati
- Amir Zadeh
- Chuan Li
- Aviv Tamar
- Deepak Pathak
- David Held
topics:
- world-models
- object-centric-learning
- video-prediction
- latent-actions
- self-supervised-learning
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Latent Particle World Models: Self-supervised Object-centric Stochastic Dynamics Modeling

## Summary
LPWM proposes a self-supervised, object-centric world model that discovers keypoints, bounding boxes, and masks directly from video, and models multi-object stochastic dynamics in latent space. It emphasizes being more efficient and interpretable than full-frame/patch-based video models, and can be conditioned on actions, language, and goal images.

## Problem
- Existing high-fidelity video generation/world models are typically computationally expensive and slow at inference, making them difficult to use directly for decision-making and planning.
- Many video prediction methods use full-frame patch representations, lacking explicit object decomposition, which makes it harder to capture multi-object interactions and align with language semantics.
- Prior object-centric methods often rely on supervision, two-stage training, explicit particle tracking, or only work in simple/simulated scenes, making them hard to scale to complex real-world multi-object videos.

## Approach
- The paper proposes **Latent Particle World Model (LPWM)**: encoding each frame as a set of foreground "particles" plus one background particle, where each particle explicitly represents position, scale, depth, transparency, and appearance features, and training the system end-to-end as a VAE-style world model.
- The core innovation is a **per-particle latent action** mechanism: instead of using one global latent action to explain changes in the whole frame, it assigns each particle a continuous latent action to describe the stochastic transition of that object/local region.
- It introduces a **Context module** (a causal spatiotemporal Transformer) that jointly learns two heads: an inverse-dynamics head that infers latent actions from adjacent frames, and a policy head that predicts a latent action distribution from the current state, with a KL term regularizing the former toward the latter. During training it uses inverse-dynamics latent actions; at inference it can sample from the policy distribution to generate stochastic rollouts.
- The **Dynamics module** is also a causal spatiotemporal Transformer, using particle states and corresponding latent actions to predict the next-step particle distribution; it also removes the explicit particle tracking used in DDLP, enabling all frames to be encoded in parallel and improving scalability.
- The model supports multiple conditioning inputs: external actions, language, goal images, and multi-view inputs; the authors also claim this Context module can transfer to non-object-centric patch-representation architectures.

## Results
- The abstract and introduction claim that LPWM achieves **state-of-the-art object-centric video prediction** on "diverse real-world and synthetic datasets," but the provided excerpt **does not include specific dataset names, metric values, or margins over baselines**.
- The paper explicitly claims LPWM is the first self-supervised object-centric model to simultaneously combine the following capabilities: **trained only on video, supports multi-view training, supports multiple conditioning modes such as actions/language/images, and is trained end-to-end**; this is qualitatively compared in a related-work table against methods such as SCALOR, SlotFormer, DDLP, and PlaySlot.
- The authors further claim the model can be used for decision-making, especially **goal-conditioned imitation learning**, and demonstrate effectiveness in **two complex multi-object environments**; however, the excerpt **does not provide specific imitation-learning success rates, returns, or quantitative comparisons with baselines**.
- The strongest concrete technical claims include: removing explicit particle tracking, supporting parallel encoding of all frames, and sampling per-particle latent actions from a latent policy at inference time to model multimodal stochastic dynamics (such as occlusion, appearance, and random motion).

## Link
- [http://arxiv.org/abs/2603.04553v1](http://arxiv.org/abs/2603.04553v1)
