---
source: arxiv
url: https://arxiv.org/abs/2606.07383v1
published_at: '2026-06-05T15:21:41'
authors:
- Huixi Intelligence
- ':'
- Chen Zhang
- Chenyang Zhou
- Guanglei Ding
- Guanghui He
- Haibin Gao
- Jiajia Chen
- Jianyong Zhang
- Lianyi Yu
- Ningyi Xu
- Ping Xu
- Qingchen Li
- Yingjun Hu
- Yijia Zhang
- Yuxi Liu
topics:
- vision-language-action
- robot-foundation-model
- edge-deployment
- robot-data-scaling
- cross-embodiment
- real-time-control
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# RhinoVLA Technical Report

## Summary
RhinoVLA is a deployment-focused vision-language-action model for real-time robot manipulation on edge hardware. It reduces visual-token cost with Qwen3-VL and aligns mixed robot datasets with a shared 72D state-action interface.

## Problem
- VLA policies are hard to run in closed loop on onboard robot hardware because VLM context processing and action generation add too much latency.
- The paper identifies VLM visual and context tokens as a main cost driver: GEMM-heavy MLP projections scale linearly with token count when model dimensions stay fixed.
- Cross-robot training is also hard because datasets use different camera layouts, action vector meanings, control units, and robot-specific dynamics.

## Approach
- RhinoVLA uses a 2.13B-parameter Qwen3-VL backbone because it represents a 224×224 image with 64 merged visual tokens, compared with 256 image tokens for PaliGemma-224 used in π0.5.
- A 0.40B-parameter continuous Action Expert generates action chunks with flow matching and conditions on Qwen3-VL KV cache, robot state, masks, noisy action chunks, flow time, and robot instance ID.
- A View Registry tags each image with camera role and modality, such as head/rgb or left_wrist/rgb, so camera identity is explicit across datasets.
- A unified 72D physical state-action slot space gives fixed meanings to action dimensions, while binary masks exclude missing or invalid robot dimensions from supervision.
- Robot-instance LoRA modules add low-cost robot-specific corrections inside the Action Expert while keeping the 72D output interface and deployment graph shared.

## Results
- RhinoVLA reaches 11.69 Hz end-to-end inference on the Huixi R1 edge SoC, above the stated 10 Hz closed-loop control target.
- The paper claims downstream task performance comparable to π0.5 at a similar parameter scale, but the excerpt does not provide task-level accuracy numbers or dataset-specific scores.
- On Jetson AGX Orin, the paper reports π0.5 end-to-end latency of about 858.3 ms: 69.3 ms for the vision encoder, 528.0 ms for the VLM backbone, and 257.0 ms for the Action Expert.
- In that π0.5 latency breakdown, the VLM backbone and Action Expert together account for more than 90% of runtime.
- Operator analysis reports that VLM MLP projections gate_proj, up_proj, and down_proj account for about 74.7% of VLM latency, while attention projections account for about 7.2%.
- The Qwen3-VL visual-token design cuts per-image visual tokens by 4× versus PaliGemma-224 under the cited 224×224 setting, which is the main claimed source of VLM-side speedup.

## Link
- [https://arxiv.org/abs/2606.07383v1](https://arxiv.org/abs/2606.07383v1)
