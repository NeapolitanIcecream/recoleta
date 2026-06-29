---
source: arxiv
url: https://arxiv.org/abs/2605.21854v1
published_at: '2026-05-21T01:02:41'
authors:
- Zhi Liu
topics:
- vision-language-action
- robot-policy-alignment
- flow-matching
- dpo
- parameter-efficient-finetuning
- inference-optimization
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# CrossVLA: Cross-Paradigm Post-Training and Inference Optimization for Vision-Language-Action Models

## Summary
CrossVLA studies DPO post-training across autoregressive and flow-matching vision-language-action models, with a practical surrogate log-probability for continuous action chunks. Its strongest claims are DoRA+DPO gains on OpenVLA LIBERO tasks and a negative result showing prefix KV caching is a poor speedup target for flow-matching VLAs.

## Problem
- VLA post-training has focused on autoregressive action-token models such as OpenVLA, while flow-matching models such as pi_0.5 lack a cheap log-probability needed for DPO.
- Robot policy adaptation needs methods that work across discrete-token and continuous-action backbones without full retraining.
- Inference speed work for VLAs often targets prefix KV caching, but flow-matching policies spend most time in action denoising.

## Approach
- For flow-matching VLAs, the paper replaces exact chunk log-likelihood with negative flow-matching MSE over sampled time points, using it as a surrogate log-probability inside standard DPO.
- It defines a common VLA interface for log-probability, reference log-probability, sampling, observation encoding, and action generation across OpenVLA and pi_0.5.
- It compares LoRA and DoRA as parameter-efficient DPO adapters, with DoRA separating weight magnitude and direction.
- It measures pi_0.5 inference latency by stage and tests chunk-level caching plus token-level prefix KV caching.
- It also trains a frozen-SigLIP projection head with multi-view and temporal InfoNCE on LIBERO frames.

## Results
- On OpenVLA over LIBERO 4-suite, DoRA+DPO reaches 73.2% mean success versus 62.75% SFT, a +10.4 percentage point gain across 600 trials and 3 environment seeds.
- Per-suite DoRA+DPO gains over OpenVLA SFT are Object +20.0 pp, Long-horizon +11.0 pp, Goal +8.0 pp, and Spatial +2.7 pp; Object is 76.0% across all three seeds, 38/50 each time.
- Compared with LoRA where multiseed results are available, DoRA is Object 76% vs 75%, Goal 78% vs 77%, and Long-horizon 64% vs 64%.
- The flow-matching DPO surrogate trains stably on pi_0.5; completed LIBERO Spatial and Object runs stay at their saturated SFT levels, 100% and 98%.
- pi_0.5 latency is about 280 ms per sample_actions call: image preprocessing about 5 ms, prefix forward about 60 ms or 21.4%, and the 10-step denoise loop about 220 ms or 78.6%.
- Prefix-style caching performs poorly on pi_0.5: chunk caching drops LIBERO Spatial success from 50/50 to 40/50 and increases wall time from 1258 s to 1796 s; token-level prefix caching reports failed runs at 0/1 and 0/2 under cache-hit settings. The projection-head pretraining reaches 99.5% k-NN recall@1 on 6000 LIBERO frames, 36x random.

## Link
- [https://arxiv.org/abs/2605.21854v1](https://arxiv.org/abs/2605.21854v1)
