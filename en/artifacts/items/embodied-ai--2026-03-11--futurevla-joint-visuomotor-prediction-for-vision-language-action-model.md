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
- world-model
- generalist-robot-policy
- sim2real
- robot-manipulation
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# FutureVLA: Joint Visuomotor Prediction for Vision-Language-Action Model

## Summary
FutureVLA targets the “future awareness” problem in robot Vision-Language-Action models, learning a joint visuomotor representation that combines visual constraints and action dynamics at the same time. The core idea is to first learn visual and motor-control information separately, then recombine them through gated interaction, and distill this future prior into downstream VLAs.

## Problem
- Existing VLAs try to incorporate future supervision, but common approaches either reconstruct future frames, which easily wastes capacity on task-irrelevant visual details, or only use sparse frame pairs, which breaks the continuous-time structure that robot actions should naturally have.
- This causes the representation to be dominated by static scene appearance, making it hard to truly capture the joint visuomotor relationship of “how environmental geometry constrains action execution.”
- This problem matters because robot control must not only observe the present but also predict action consequences; if future modeling is inaccurate, long-horizon and contact-rich tasks are more likely to fail.

## Approach
- Proposes a two-stage framework, **FutureVLA**: first joint visuomotor pretraining, then downstream VLA post-training alignment.
- During pretraining, the input is continuous multi-frame video clips rather than sparse frame pairs; a frozen 3D-VAE is first used to compress videos into temporal tokens, preserving dynamic information while reducing redundancy.
- Designs **Joint Visuomotor Gating (JVG)**: the representation is split into a visual stream and an action stream. The visual stream is only responsible for preserving initial scene information; the action stream is only responsible for predicting continuous action chunks, thereby reducing “visual dominance.”
- The action stream queries spatial/geometric constraints from the visual stream on demand through gated cross-attention, effectively meaning “the action decides how to move, while vision determines under what constraints it moves,” ultimately forming joint visuomotor embeddings.
- During post-training, the downstream VLA inference structure is not modified; instead, only a lightweight adapter is used to align intermediate VLA representations to these joint visuomotor embeddings, allowing single-frame-input VLAs to internalize future dynamic priors; the paper also shows compatibility with OFT-style and GR00T-style action heads.

## Results
- The paper claims an average improvement of **11.4%** on **SimplerEnv** and **21.7%** on **real robots** (relative to the baseline “without joint visuomotor embedding guidance”).
- Under **Google robot / SimplerEnv / Visual Matching**, **FutureVLA-GT** averages **80.1**, higher than **GR00T-N1.5 35.2**, an absolute gain of **44.9**; **FutureVLA-OT** averages **77.6**, higher than **OpenVLA-OFT 47.5**, a gain of **30.1**. Among them, **Put in Drawer** improves from **7.4** to **85.2** (GT).
- On **WidowX / SimplerEnv**, **FutureVLA-GT** averages **71.9**, higher than **GR00T-N1.5 61.9**, **UniVLA 47.9**, and **Villa-X 40.8**; **FutureVLA-OT** is **63.6**. The paper also reports in ablations that after introducing JVPM guidance, both architectures improve by an average of **9.4** points over their respective **wo/ JVPM** versions (GT: **62.5→71.9**, OT: **54.2→63.6**).
- On **LIBERO**, **FutureVLA-GT/OT** average **98.3/98.2**, outperforming **UniVLA 95.2**, **pi_0 94.2**, and **GR00T-N1.5 93.9**. On the long-horizon **Long** subset, **FutureVLA-GT 96.0**, higher than **UniVLA 92.0**, **pi_0 85.2**, and **WorldVLA 60.0**.
- On four tasks with a **real Franka robot**, **FutureVLA-GT** achieves an average success rate of **70.0%**, **26.7%** higher than **pi_0**. The abstract also emphasizes a significant **21.7%** gain over the baseline in real-world manipulation, especially on continuous-control/contact-rich tasks (such as whiteboard erasing).

## Link
- [http://arxiv.org/abs/2603.10712v1](http://arxiv.org/abs/2603.10712v1)
