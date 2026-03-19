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
- object-centric-world-model
- latent-particles
- self-supervised-video-modeling
- stochastic-dynamics
- latent-actions
relevance_score: 0.75
run_id: materialize-outputs
language_code: en
---

# Latent Particle World Models: Self-supervised Object-centric Stochastic Dynamics Modeling

## Summary
LPWM proposes a self-supervised, object-centric world model that discovers keypoints, bounding boxes, and masks directly from video, and predicts stochastic multi-object dynamics in latent space. It emphasizes end-to-end training, scalability to real-world multi-object scenes, and conditioning on actions, language, or goal images.

## Problem
- Existing high-fidelity video generation/world models are typically computationally expensive and slow at inference, making them less suitable for applications such as decision-making and robotics.
- Common patch-level representations lack explicit semantic object decomposition, making it difficult to naturally model multi-object interactions or align with language.
- Previous object-centric video prediction methods are often limited to simple or simulated environments, and frequently rely on explicit tracking, two-stage training, or global latent actions, making them hard to scale to complex real-world stochastic dynamics.

## Approach
- Uses DLP-style **latent particles** to represent each frame: each particle explicitly encodes position, scale, depth, transparency, and appearance features, plus a background particle, enabling object structure discovery from unlabeled videos.
- Proposes a new **Context module**: a causal spatiotemporal Transformer that learns a latent action for **each particle**, rather than assigning one global latent action to the whole frame; it includes an inverse dynamics head and a latent policy head, where the former infers latent actions from adjacent frames and the latter provides a prior distribution over latent actions based on the current state.
- Uses the latent policy distribution to regularize the inverse dynamics distribution, and samples directly from this prior at inference time, allowing the model to generate **stochastic, multimodal** future trajectories rather than only deterministic predictions.
- The dynamics module is also a causal spatiotemporal Transformer, which injects each particle's latent action into the state transition via AdaLN, predicts particles at the next time step, and then renders them back to images through a decoder.
- The entire system is trained **end-to-end** as a sequential VAE using only video, while also supporting action, language, goal image, and multi-view conditioning by mapping global conditions into local latent actions for each particle.

## Results
- The paper claims that LPWM achieves **state-of-the-art object-centric video prediction** on **multiple real-world and synthetic multi-object datasets**, and can also be used for decision-making tasks such as **goal-conditioned imitation learning**.
- It explicitly claims to be the **first** self-supervised object-centric model that is “trained only from video, supports multi-view training, and simultaneously supports multiple conditioning modalities such as actions/language/goal images.”
- Compared with DDLP, LPWM removes the requirement for **explicit particle tracking**, allows **parallel encoding of all frames**, and introduces per-particle continuous latent actions to handle stochastic transitions such as occlusion, appearance/disappearance, and random motion.
- The provided excerpt **does not include specific quantitative numbers** (such as PSNR/SSIM/FVD, percentage improvements on named datasets, imitation learning success rates, etc.), so precise metrics, baseline gaps, or statistical significance cannot be reported.
- The strongest concrete conclusion is that LPWM can perform both **stochastic video modeling** and **goal-conditioned imitation learning**, while also supporting multiple forms of control such as **language-conditioned video generation** and **latent-action-conditioned video prediction**.

## Link
- [http://arxiv.org/abs/2603.04553v1](http://arxiv.org/abs/2603.04553v1)
