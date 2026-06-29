---
source: arxiv
url: http://arxiv.org/abs/2604.10055v2
published_at: '2026-04-11T06:37:47'
authors:
- Yuhan Xie
- Yuping Yan
- Yunqi Zhao
- Handing Wang
- Yaochu Jin
topics:
- vision-language-action
- robot-robustness
- multimodal-perturbations
- curriculum-learning
- sim-benchmark
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# STRONG-VLA: Decoupled Robustness Learning for Vision-Language-Action Models under Multimodal Perturbations

## Summary
STRONG-VLA improves the robustness of vision-language-action models by splitting fine-tuning into a perturbation-hardening stage and a clean-data re-alignment stage. The paper also introduces a 28-type multimodal perturbation benchmark and shows gains across OpenVLA, OpenVLA-OFT, and pi0 on LIBERO and a real robot setup.

## Problem
- Vision-language-action models fail when camera input is corrupted or instructions contain noise, distractors, or adversarial edits. In robotics, small early mistakes can turn into full task failure.
- Existing robustness training usually mixes clean and perturbed data in one objective. The paper argues that this creates conflicting gradients: clean data needs sensitivity to details, while perturbed data pushes the policy toward invariance.
- This matters for deployment because real robots face sensor noise, occlusion, geometric shifts, and instruction corruption at the same time.

## Approach
- STRONG-VLA uses two training stages instead of one joint robustness objective.
- Stage I trains on perturbed data with a curriculum that increases perturbation difficulty over time. It first hardens language, then vision.
- The curriculum measures perturbation severity with simple modality-specific scores: text corruption ratio for language, and normalized image distortion, occlusion area, or geometric displacement for vision.
- Stage II fine-tunes the Stage I model on clean task data to recover task fidelity while keeping the robustness learned under perturbations.
- The paper also builds a benchmark with 28 perturbation types: 12 textual and 16 visual, including held-out evaluation-only perturbations for zero-shot robustness tests.

## Results
- On LIBERO, STRONG-VLA improves average task success under seen and unseen perturbations across three backbones: OpenVLA by up to +12.60% seen and +7.77% unseen; OpenVLA-OFT by +14.48% seen and +13.81% unseen; pi0 by +16.49% seen and +5.58% unseen.
- Clean performance is mostly preserved: OpenVLA changes from baseline by -1.00 points on clean inputs, OpenVLA-OFT by -0.75, and pi0 by +2.75.
- Large per-perturbation gains appear on textual attacks. Examples: OpenVLA-OFT gains +84.75 on prefix adversarial injection and +82.50 on role spoofing; pi0 gains +58.25 on role spoofing; OpenVLA gains +39.50 on suffix linguistic corruption.
- Gains also appear on visual and multimodal cases. Examples: pi0 gains +36.25 on image shift and +44.75 on suffix corruption plus random occlusion; OpenVLA-OFT gains +44.00 on prefix injection plus random occlusion; OpenVLA gains +26.75 on suffix corruption plus random occlusion.
- Zero-shot robustness improves on held-out perturbations marked evaluation-only, including semantic drift, contextual distractors, and dynamic visual artifacts. Some perturbations still show small drops, such as OpenVLA on dynamic uniform noise (-6.25) and OpenVLA-OFT on dynamic uniform noise (-2.75).
- The abstract states that real-world experiments on an AIRBOT platform support the method's practical value, but the excerpt does not provide those numbers.

## Link
- [http://arxiv.org/abs/2604.10055v2](http://arxiv.org/abs/2604.10055v2)
