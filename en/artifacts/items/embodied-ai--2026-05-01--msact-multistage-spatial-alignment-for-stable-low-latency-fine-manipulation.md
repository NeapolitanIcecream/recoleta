---
source: arxiv
url: https://arxiv.org/abs/2605.00475v1
published_at: '2026-05-01T07:35:15'
authors:
- Xianbo Cai
- Hideyuki Ichiwara
- Masaki Yoshikawa
- Tetsuya Ogata
topics:
- bimanual-manipulation
- fine-manipulation
- spatial-attention
- action-chunking
- imitation-learning
- low-latency-control
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# MSACT: Multistage Spatial Alignment for Stable Low-Latency Fine Manipulation

## Summary
MSACT adds explicit 2D attention-point tracking to ACT for bimanual fine manipulation. It raises real-world success while keeping ACT-level inference latency.

## Problem
- Fine manipulation needs fast control and stable visual localization; drift can cause missed contacts, failed handovers, and bad timing.
- ACT is fast and data-efficient, but its visual features do not enforce spatial consistency.
- Larger VLA models and diffusion policies can add compute or sampling delay, which hurts 50 Hz robot control.

## Approach
- The policy keeps ACT's action chunking, temporal ensembling, ResNet image encoder, and CVAE training loss.
- A multistage spatial attention module extracts 6 normalized 2D points from each of the top and front cameras, then turns the 12 points into Transformer tokens.
- The attention maps come from 3 CNN stages, are averaged, and pass through a temperature-controlled 2D softmax to produce coordinates.
- During training, the decoder predicts future action chunks and future attention-point sequences.
- A self-supervised L1 alignment loss compares predicted future points with points re-extracted from future ground-truth frames, so no manual keypoint labels are needed.

## Results
- On 400 real-world ALOHA trials across 4 tasks, MSACT reports 53.00% overall success with 99% CI [46.58, 59.33], compared with ACT at 23.25% [18.27, 29.10], SmolVLA at 15.25%, π0.5 at 13.00%, and Diffusion Policy at 0.00%.
- Inference latency stays close to ACT: MSACT is 45.40 ± 5.00 ms, ACT is 45.34 ± 1.03 ms, SmolVLA is 91.23 ± 1.34 ms, π0.5 is 112.1 ± 0.40 ms, and Diffusion Policy is 158.1 ± 14.9 ms.
- The paper reports a statistically significant gain over ACT on aggregated real-world outcomes using Fisher's exact test, p < 0.001.
- Real-world final-stage success improves over ACT on Detach Network Cable from 26% to 72%, Thread Velcro from 8% to 21%, and Open Match Box from 38% to 63%; Insert Tea Bag matches SmolVLA at 56% and exceeds ACT at 21%.
- On simulated Cube Transfer using human data, final Transfer success rises from ACT's 50% to 76%; with scripted data it rises from 86% to 100%.
- On simulated Bimanual Insertion, final Insert success rises from ACT's 20% to 26% with human data and from 32% to 49% with scripted data.

## Link
- [https://arxiv.org/abs/2605.00475v1](https://arxiv.org/abs/2605.00475v1)
