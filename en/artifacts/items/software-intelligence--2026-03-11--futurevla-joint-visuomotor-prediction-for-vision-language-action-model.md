---
source: arxiv
url: http://arxiv.org/abs/2603.10712v1
published_at: '2026-03-11T12:39:55'
authors:
- Xiaoxu Xu
- Hao Li
- Jinhui Ye
- Yilun Chen
- Jia Zeng
- Xinyi Chen
- Linning Xu
- Dahua Lin
- Weixin Li
- Jiangmiao Pang
topics:
- vision-language-action
- robotics
- world-models
- future-prediction
- multimodal-learning
relevance_score: 0.32
run_id: materialize-outputs
language_code: en
---

# FutureVLA: Joint Visuomotor Prediction for Vision-Language-Action Model

## Summary
FutureVLA proposes a joint visuomotor prediction framework for the problem of "how robots can foresee the future and act better accordingly" in vision-language-action models. Its core idea is to decouple scene-level visual constraints from continuous action dynamics and then fuse them as future priors to guide downstream VLA models.

## Problem
- Existing future-guidance methods either explicitly reconstruct future video, which tends to waste model capacity on task-irrelevant visual details and causes representations to be dominated by visual information.
- Or they learn implicit future representations only from sparse frame pairs, which breaks temporal continuity and mismatches the robot's continuous multi-step action chunks.
- This matters because robot actions are strictly constrained by environmental geometry and affordances; without jointly modeling "what is seen" and "how to move," long-horizon real-world manipulation becomes less stable.

## Approach
- Proposes a two-stage framework: first **Joint Visuomotor Pretraining**, then **Embedding-Guided VLA Post-training**.
- During pretraining, continuous multi-frame video is used as input and compressed into temporal tokens with a frozen 3D-VAE, instead of using only sparse frame pairs, thereby preserving the temporal continuity needed for actions.
- Designs **Joint Visuomotor Gating (JVG)**: the representation is split into a visual stream and a motor stream; the visual stream is responsible only for preserving the initial scene state, while the motor stream is responsible only for continuous physical control, and queries visual constraints on demand through gated cross-attention.
- Training supervision is also decoupled: the visual stream reconstructs the first-frame latent representation, while the motor stream predicts action chunks; the resulting joint visuomotor embeddings are then transferred into downstream VLA models through latent embedding alignment, without modifying the inference architecture.

## Results
- The paper claims that overall, compared with baselines **without joint visuomotor embedding guidance**, FutureVLA improves average performance by **11.4%** on **SimplerEnv** and by **21.7%** on **real-world robot manipulation**.
- In **SimplerEnv / Google robot / Visual Matching**, FutureVLA-GT averages **80.1**, higher than GR00T-N1.5's **35.2**, an absolute gain of **44.9**; FutureVLA-OT averages **77.6**, higher than OpenVLA-OFT's **47.5**, a gain of **30.1**. Among these, **Put in Drawer** shows the most significant increase, from **7.4** to **85.2** (GT).
- In **SimplerEnv / WidowX**, FutureVLA-GT averages **71.9**, outperforming GR00T-N1.5's **61.9**, UniVLA's **47.9**, and Villa-X's **40.8**; FutureVLA-OT reaches **63.6**. The authors also report that compared with versions without JVPM, both GT and OT improve by **9.4** points each (e.g., GT from **62.5** to **71.9**).
- On **LIBERO**, FutureVLA-GT averages **98.3** and FutureVLA-OT averages **98.2**, exceeding UniVLA's **95.2**, \(\pi_0\)'s **94.2**, and GR00T-N1.5's **93.9**. On **Long** tasks, FutureVLA-GT reaches **96.0**, a **4.0**-point improvement over UniVLA's **92.0**.
- Across **four real-robot tasks**, FutureVLA-GT achieves an average success rate of **70.0%**, **26.7%** higher than \(\pi_0\). The paper emphasizes that the gains are especially clear on contact-rich tasks requiring fine-grained continuous control, such as whiteboard wiping, though the excerpt does not provide detailed per-task numbers.

## Link
- [http://arxiv.org/abs/2603.10712v1](http://arxiv.org/abs/2603.10712v1)
