---
source: arxiv
url: https://arxiv.org/abs/2605.12369v1
published_at: '2026-05-12T16:38:40'
authors:
- Xiaosong Jia
- Bowen Yang
- Zuhao Ge
- Xian Nie
- Yuchen Zhou
- Cunxin Fan
- Yufeng Li
- Yilin Chai
- Chao Jing
- Zijian Liang
- Qingwen Bu
- Haidong Cao
- Chao Wu
- Qifeng Li
- Zhenjie Yang
- Chenhe Zhang
- Hongyang Li
- Zuxuan Wu
- Junchi Yan
- Yu-Gang Jiang
topics:
- vision-language-action
- robot-foundation-models
- attention-specialization
- robot-manipulation
- robot-generalization
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# GuidedVLA: Specifying Task-Relevant Factors via Plug-and-Play Action Attention Specialization

## Summary
GuidedVLA improves VLA robot policies by assigning action-decoder attention heads to object grounding, skill phase recognition, and depth-based geometry.

## Problem
- End-to-end VLA training can make action tokens attend to background textures, camera artifacts, or other spurious cues, which hurts out-of-domain success.
- The paper targets the action decoder, where task factors are usually learned implicitly and can vary across heads and scenes.
- This matters for manipulation because small errors in target object, sub-skill, or 3D pose can cause task failure.

## Approach
- GuidedVLA adds a ControlNet-style residual attention branch to a pretrained VLA policy, with zero-initialized fusion so the base policy behavior is preserved at the start of training.
- Object heads are trained to put attention mass on ground-truth object masks from Qwen3-VL prompts, SAM2 propagation, and human verification.
- Skill heads are trained with a KL loss to predict soft labels for task phases, such as pick and place, over a future horizon.
- Depth heads attend only to keys and values from a frozen depth encoder, so specific heads receive 3D structure without depth labels.
- The total loss combines the base flow-matching action loss with object and skill auxiliary losses; depth guidance is structural rather than loss-based.

## Results
- On LIBERO-Plus, GuidedVLA with all heads reaches 75.4% average success, above its π0 base model at 68.2%, DreamVLA at 69.9%, OpenVLA-OFT at 69.6%, and RIPT-VLA at 68.4%.
- LIBERO-Plus ablations show each factor helps: object head 73.4%, skill head 72.5%, depth head 71.7%, all heads 75.4%.
- On LIBERO-Plus perturbations, the full model improves over π0 on camera 73.7% vs 62.3%, robot state 51.4% vs 39.8%, lighting 94.6% vs 86.0%, background 89.0% vs 82.8%, layout 79.9% vs 69.6%, and long-horizon tasks 66.2% vs 60.1%.
- On RoboTwin 2.0, the full model reports 90.63% average success across 8 manipulation tasks under randomized unseen settings; the excerpt does not provide the π0 average for that benchmark.
- In real-world trials across 6 tasks with 20 trials each, GuidedVLA improves average success over the base policy: in-domain 75.8% vs 55.8%, scene 67.5% vs 44.2%, and lighting 79.2% vs 57.5%.
- The annotation pipeline reports 92% of episodes needing no human correction and 50 episodes annotated in about 4 minutes, compared with about 43.5 minutes manually.

## Link
- [https://arxiv.org/abs/2605.12369v1](https://arxiv.org/abs/2605.12369v1)
