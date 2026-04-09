---
source: arxiv
url: http://arxiv.org/abs/2604.03956v1
published_at: '2026-04-05T04:23:18'
authors:
- Ravi Ranjan
- Agoritsa Polyzou
topics:
- vision-language-action
- robot-unlearning
- embodied-foundation-models
- generalist-robot-policy
- safety
- openvla
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# VLA-Forget: Vision-Language-Action Unlearning for Embodied Foundation Models

## Summary
VLA-Forget targets selective unlearning for vision-language-action robot policies. It removes unsafe, spurious, or sensitive behaviors while trying to keep visual grounding, language conditioning, and action performance intact.

## Problem
- VLA robot policies can memorize bad behavior in several places at once: the visual encoder, the image-language connector, and the action-generating language model.
- Standard unlearning methods for only vision models or only language models often miss part of the unwanted behavior or damage normal robot performance.
- This matters because VLA errors become physical actions, such as following the wrong instruction while still producing a plausible grasp.

## Approach
- The method splits the model into three parts: visual encoder, cross-modal projector, and upper action/reasoning transformer layers.
- It picks visual and projector layers to edit using a ratio-aware score based on forget gradients, retain gradients, parameter scale, and gradient conflict.
- It picks action/reasoning layers using a significance ratio, starting with the most forget-relevant upper layers and adding more only if forgetting is still weak.
- Training uses four losses together: retain loss on kept data, forget loss on target data, mismatch loss to push forgotten outputs away from the original model, and feature preservation loss on retained and boundary examples.
- Updates are done in stages with LoRA adapters and PCGrad: first weaken visual triggers, then break bad visual-language bindings, then suppress residual action priors.

## Results
- In the abstract, the paper claims relative gains over strong baselines of **10% better forgetting efficacy**, **22% better perceptual specificity**, **9% better reasoning/task retention**, and **55% lower post-quantization recovery**.
- On **OpenVLA-7B / Open X-Embodiment**, VLA-Forget reports **FC 93**, **RC 91**, **FAD 0.88**, **RAD 0.21**, **TSR 78**, **SVR 5**. Compared with **NPO**: RC improves **88 -> 91**, TSR **74 -> 78**, RAD drops **0.23 -> 0.21**, SVR drops **8 -> 5**. Compared with **GA**: same FC **93**, but RC improves **60 -> 91** and TSR **40 -> 78**.
- On **OpenVLA-7B / lerobot-pusht_image**, VLA-Forget reports **FC 95**, **RC 94**, **FAD 0.90**, **RAD 0.13**, **TSR 69**, **SVR 4**. Compared with **NPO**: FC **92 -> 95**, RC **90 -> 94**, TSR **65 -> 69**, RAD **0.15 -> 0.13**, SVR **7 -> 4**.
- On **pi0fast-base / Open X-Embodiment**, VLA-Forget reports **FC 94**, **RC 89**, **FAD 0.88**, **RAD 0.22**, **TSR 75**, **SVR 6**. Compared with **NPO**: FC **89 -> 94**, RC **87 -> 89**, TSR **72 -> 75**, RAD **0.24 -> 0.22**. Compared with **GA**: FC **93 -> 94**, RC **57 -> 89**, TSR **38 -> 75**, while SVR stays **6**.
- Across the shown tables, GA usually gets the strongest or tied forgetting score, but VLA-Forget keeps much higher retain utility and task success, which is the paper's main claimed advantage.

## Link
- [http://arxiv.org/abs/2604.03956v1](http://arxiv.org/abs/2604.03956v1)
