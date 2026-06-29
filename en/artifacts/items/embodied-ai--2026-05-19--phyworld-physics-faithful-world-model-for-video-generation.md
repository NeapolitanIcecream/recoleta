---
source: arxiv
url: https://arxiv.org/abs/2605.19242v1
published_at: '2026-05-19T01:28:52'
authors:
- Pu Zhao
- Juyi Lin
- Timothy Rupprecht
- Arash Akbari
- Chence Yang
- Rahul Chowdhury
- Elaheh Motamedi
- Arman Akbari
- Yumei He
- Chen Wang
- Geng Yuan
- Weiwei Chen
- Yanzhi Wang
topics:
- world-model
- video-generation
- physics-simulation
- preference-optimization
- physical-ai
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# PhyWorld: Physics-Faithful World Model for Video Generation

## Summary
PhyWorld is a video generation world model that post-trains Wan2.2-I2V-A14B to make video continuations more stable and more physically plausible. The paper targets Physical AI simulation, but it evaluates generated video quality and physics scores rather than robot control or action-conditioned policy learning.

## Problem
- Physical AI needs safe, scalable simulators because training early robot policies in the real world can be slow, costly, and unsafe.
- Large video generators can synthesize diverse futures, but they often drift in color, object identity, and motion speed across frames.
- Standard video benchmarks miss many physics errors, so the paper adds per-law evaluation for collisions, fluids, shadows, rolling, ballistic motion, and related events.

## Approach
- PhyWorld starts from Wan2.2-I2V-A14B and adds video-to-video continuation: the input clip is encoded with Wan-VAE, a binary mask separates preserved frames from frames to generate, and the final conditioning frame gives CLIP context through cross-attention.
- Stage 1 fine-tunes with flow matching on filtered OpenVid-1M clips, using CLIP frame similarity and UniMatch optical flow to remove near-static, flickering, abrupt, or erratic-motion videos.
- Stage 2 uses Direct Preference Optimization on physics preference pairs. A LoRA adapter is trained while the base denoiser stays frozen as the reference model.
- The DPO data comes from a 250-prompt text/image-to-video physics benchmark with 2,000 pre-rated videos, about 350 human raters, about 4,500 cleaned annotations, and a 1,000-pair training subset sampled from 2,202 eligible pairs.
- Evaluation uses standard video-quality scoring plus a Qwen3.5-9B video-language judge fine-tuned to score 1-5 Likert ratings for general quality and per-law physics correctness.

## Results
- On VBench, PhyWorld reports an average score of 0.769, compared with 0.756 or lower for state-of-the-art baselines.
- On the paper's physical-faithfulness benchmark, PhyWorld reports an average score of 3.09, compared with 2.99 for the strongest baseline.
- The benchmark contains 250 prompts and scores physics categories including collision/rebound, destruction/deformation, fluids/liquids, shadow/reflection, chain or multi-stage events, rolling/sliding, and throwing/ballistic motion.
- The DPO sweep reports beta=100 as the selected setting at step 250, with Spearman +0.520 versus +0.020 for beta=30, and final implicit reward margin +0.200 versus +0.075.
- The excerpt does not report robot task success, planning performance, sim-to-real transfer, or action-conditioned control metrics.

## Link
- [https://arxiv.org/abs/2605.19242v1](https://arxiv.org/abs/2605.19242v1)
