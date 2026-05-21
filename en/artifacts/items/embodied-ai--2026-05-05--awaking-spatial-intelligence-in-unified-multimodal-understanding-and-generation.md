---
source: arxiv
url: https://arxiv.org/abs/2605.04128v1
published_at: '2026-05-05T15:49:47'
authors:
- Lin Song
- Wenbo Li
- Guoqing Ma
- Wei Tang
- Bo Wang
- Yuan Zhang
- Yijun Yang
- Yicheng Xiao
- Jianhui Liu
- Yanbing Zhang
- Guohui Zhang
- Wenhu Zhang
- Hang Xu
- Nan Jiang
- Xin Han
- Haoze Sun
- Maoquan Zhang
- Haoyang Huang
- Nan Duan
topics:
- spatial-reasoning
- multimodal-foundation-model
- image-generation
- image-editing
- world-models
relevance_score: 0.56
run_id: materialize-outputs
language_code: en
---

# Awaking Spatial Intelligence in Unified Multimodal Understanding and Generation

## Summary
JoyAI-Image is a unified image understanding, generation, and editing model that adds stronger spatial reasoning to a Qwen3-VL-based MLLM and a 16B-parameter diffusion transformer.

## Problem
- Current unified visual models often connect understanding, generation, and editing weakly, so image edits and generated views do not reliably use scene geometry.
- The paper targets layout, depth, object relations, viewpoint change, and cross-view consistency, which matter for controllable image editing and may help later vision-language-action systems and world models.

## Approach
- The model uses Qwen3-VL-8B-Instruct as the MLLM for image/text understanding and instruction parsing.
- For generation and editing, the MLLM outputs hidden-state features that condition a 16B MMDiT diffusion model; a Wan-2.1 VAE compresses images into latent tokens.
- The authors build OpenSpatial, a 3D box-centered data engine that turns scans and web videos into spatial QA pairs using 3D oriented boxes, projected masks, visibility checks, and multi-view consistency checks.
- Training uses about 11.3M samples, including 6.1M general-understanding samples, 3.4M spatial-understanding samples, 1.4M instruction-rewriting samples, and 137.4K spatial-editing samples.
- The MLLM is fine-tuned with supervised learning plus KL distillation on general data only, so it keeps general skills while learning new spatial skills.

## Results
- On 9 spatial benchmarks, JoyAI-Image-Und reports a 64.4 spatial average, up +5.3 points over Qwen3-VL-8B-Instruct at 59.1 and equal to Gemini-2.5-Pro at 64.4.
- The largest gains over the base model are AllAngles +11.5, 3DSR_C +7.7, MMSI +7.7, ERQA +4.9, and VSI +4.5.
- On general benchmarks, it keeps similar performance: MMBench_CN 83.7 versus base 83.3, MathVista 74.4 versus 75.0, MMStar 71.3 versus 70.1, and OCRB 87.9 versus 90.3.
- OpenSpatial contains about 3M entries across 5 spatial capability groups and 19 sub-tasks; the full spatial training subset is reported as 3.4M samples.
- The excerpt claims state-of-the-art or competitive results for generation, long-text rendering, and editing, but it does not provide the detailed numeric generation/editing tables in the supplied text.

## Link
- [https://arxiv.org/abs/2605.04128v1](https://arxiv.org/abs/2605.04128v1)
