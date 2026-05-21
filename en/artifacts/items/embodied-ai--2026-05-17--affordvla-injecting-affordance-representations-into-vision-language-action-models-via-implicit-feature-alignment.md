---
source: arxiv
url: https://arxiv.org/abs/2605.17517v1
published_at: '2026-05-17T16:02:05'
authors:
- Weijie Kong
- Zhian Su
- Wei Yu
- Huixu Dong
topics:
- vision-language-action
- robot-foundation-model
- affordance-learning
- generalist-robot-policy
- robot-manipulation
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# AffordVLA: Injecting Affordance Representations into Vision-Language-Action Models via Implicit Feature Alignment

## Summary
AffordVLA trains a VLA policy to attend to task-relevant contact regions by aligning its internal visual features with affordance features from a frozen teacher. The teacher is used only during training, so inference keeps the same policy path and adds no stated runtime cost.

## Problem
- VLA policies often recognize the right object but act on the wrong part, such as grasping a skillet body instead of its handle.
- Existing affordance methods often feed masks, heatmaps, or detector outputs into the policy at inference time, which needs extra affordance labels, adds latency, and can fail when the detector fails.
- The problem matters because clutter, distractors, and complex textures can lower manipulation success when the policy attends to global appearance instead of functional interaction regions.

## Approach
- A zero-shot affordance teacher takes an RGB image and language instruction, uses Qwen3-VL to convert the task into part-level affordance prompts, then uses a SAM3-based open-vocabulary perception module to produce task-conditioned affordance features.
- The VLA backbone is based on π0.5 with a Gemma-2B language backbone and SigLIP-So400m visual encoder; an action Transformer predicts continuous action chunks with conditional flow matching.
- During training, AffordVLA aligns the VLA’s intermediate visual tokens with the teacher’s affordance feature tokens using cosine similarity after resizing, normalization, and a two-layer MLP projection.
- The alignment is applied to layer 12 of an 18-layer understanding model, using teacher features with dimension 256 and VLA visual features with dimension 2048.
- The final loss combines action prediction loss and affordance alignment loss with λ = 0.5; the frozen teacher is removed for inference.

## Results
- On RoboTwin, the paper claims state-of-the-art performance, beating the previous best baseline by 20.5% in the Easy setting and 12.8% in the Hard setting.
- The affordance teacher has about 0.8B parameters and processes 1008 × 1008 images; it is used only during training.
- The understanding expert has about 3.0B parameters with 18 layers, and the action expert has about 0.3B parameters with 18 Transformer layers.
- Inference uses 10 flow-matching denoising steps and an action chunk horizon of H = 30.
- The excerpt claims improved real-world manipulation in unstructured environments, better data efficiency, and zero additional inference overhead, but it does not provide real-world success-rate numbers in the provided text.

## Link
- [https://arxiv.org/abs/2605.17517v1](https://arxiv.org/abs/2605.17517v1)
