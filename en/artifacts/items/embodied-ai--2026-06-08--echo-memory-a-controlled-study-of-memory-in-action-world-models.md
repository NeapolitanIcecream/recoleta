---
source: arxiv
url: https://arxiv.org/abs/2606.09803v1
published_at: '2026-06-08T17:54:10'
authors:
- Wayne King
- Zeyue Xue
- Yuxuan Bian
- Jie Huang
- Haoran Li
- Yaowei Li
- Yaofeng Su
- Yuming Li
- Haoyu Wang
- Shiyi Zhang
- Songchun Zhang
- Yuwei Niu
- Sihan Xu
- Junhao Zhuang
- Haoyang Huang
- Nan Duan
topics:
- action-world-models
- memory-mechanisms
- video-diffusion
- state-space-models
- revisit-consistency
- evaluation-protocol
relevance_score: 0.64
run_id: materialize-outputs
language_code: en
---

# Echo-Memory: A Controlled Study of Memory in Action World Models

## Summary
Echo-Memory is a controlled study of memory mechanisms for action-conditioned video world models. It finds that replay quality and revisit memory can rank methods differently, with block-wise state-space recurrence scoring highest on open-domain return.

## Problem
- Action world models can change a scene or replace a salient object when the camera leaves and later returns, even when local video looks plausible.
- Prior memory comparisons mix changes in backbone, training, retrieval, sampling, and metrics, so the memory mechanism is hard to isolate.
- This matters because camera-following video is not enough for a world model; the model must preserve object identity and scene state across generated segments.

## Approach
- The study fixes the video diffusion-transformer backbone, optimizer, camera-action representation, sampler, training recipe, and evaluation pipeline.
- It varies only the memory profile: raw context, compression-based memory, spatial summaries with different read-out paths, and state-space recurrence.
- The shared input interface uses a first frame, text prompt, historical context, and a per-frame 12D relative-RT camera-action sequence.
- Training uses 81-frame segments at 352×640 resolution, AdamW, 8 A100-80G GPUs, 5k steps, target-frame-only supervision, and a 10% overlap-drop policy.
- Evaluation has three branches: replay PSNR/SSIM/LPIPS, in-domain loop return PSNR/SSIM/LPIPS, and open-domain return scored by Qwen3-VL-30B-A3B on a 0-100 VLM scale.

## Results
- Raw context is a strong baseline: open-domain VLM rises from 12.25 for anchor-only I2V to 50.75 with K=5 and 58.63 with K=20.
- Block-wise State-Space gets the best open-domain return score in the main table: 69.00 O-V, compared with 58.63 for Context K=20 and 34.75 for legacy-hybrid State-Space.
- Replay metrics do not predict revisit memory: Spatial Memory has high replay PSNR at 13.60 but low open-domain VLM at 6.00.
- Context K=20 has the best main-table replay SSIM and LPIPS: 0.449 SSIM and 0.496 LPIPS, while its open-domain VLM is 58.63.
- In-domain return also ranks methods differently: State-Space legacy hybrid has 12.23 ID-PSNR, while Context K=20 has 11.07 ID-PSNR but better open-domain VLM.
- The VLM-judge sanity check reports correlations above 0.90 with Claude Opus 4.6, GPT-5.5, and a human anchor; Pearson correlations are 0.93, 0.94, and 0.96 versus Qwen3-VL.

## Link
- [https://arxiv.org/abs/2606.09803v1](https://arxiv.org/abs/2606.09803v1)
