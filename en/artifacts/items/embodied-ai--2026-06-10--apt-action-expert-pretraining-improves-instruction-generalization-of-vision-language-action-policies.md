---
source: arxiv
url: https://arxiv.org/abs/2606.12366v1
published_at: '2026-06-10T17:34:25'
authors:
- Kechun Xu
- Zhenjie Zhu
- Anzhe Chen
- Rong Xiong
- Yue Wang
topics:
- vision-language-action
- robot-foundation-model
- action-expert-pretraining
- instruction-generalization
- manipulation
- sim2real
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# APT: Action Expert Pretraining Improves Instruction Generalization of Vision-Language-Action Policies

## Summary
APT pretrains the continuous action expert in a vision-language-action robot policy before adding language conditioning. The paper claims this improves out-of-distribution instruction following in simulation and real-robot manipulation.

## Problem
- Continuous-action VLA policies often learn visual shortcuts because each trajectory has many vision-action frames but only one language instruction.
- A randomly initialized action expert can send noisy gradients into the pretrained VLM, which weakens the model's language behavior.
- This matters for robot policies that must follow paraphrases, new object names, and composed instructions instead of memorized task labels.

## Approach
- The method factorizes the policy into a vision-action prior π(a|v) and a language-conditioned VLA likelihood, so the action model first learns manipulation from images and actions only.
- Stage 1 freezes the VLM and trains a diffusion-based action expert on vision-action pairs with language masked out.
- Stage 2 injects language tokens and trains the full VLA policy so the pretrained action distribution is steered by the instruction.
- The action expert uses Transformer self-attention over visual, language, proprioceptive, action-history, and noisy-action tokens.
- Layer-wise gated fusion adds intermediate Qwen3-VL features into action-expert layers, with learned gates controlling how much VLM information enters.

## Results
- On LIBERO-PRO, OpenVLA and π0 score 0% average success, π0.5 scores 11%, LangForce scores 14%, APT scores 19%, and APT with VLM finetuning scores 27%.
- On LIBERO-PRO Spatial, APT with VLM finetuning reaches 62% on Pos and 62% on Task, compared with 20% and 1% for π0.5.
- On rigid object pick-place, π0.5 scores 84% SO, 70% UO, 86% UC, and 50% UOUE; APT with two-stage training and VLM finetuning scores 98%, 84%, 92%, and 58%.
- An APT variant with knowledge insulation plus two-stage training scores 96% SO, 74% UO, 90% UC, and 62% UOUE, while using only VLA data and no VL reasoning co-training.
- The paper reports that two-stage action pretraining improves π-style and GR00T-style architectures across almost all tested settings, but the excerpt provides the detailed numbers only in plots.
- Real-world experiments finetune each policy with 30 demonstrations per task and include single-task and compositional generalization; the excerpt does not include the final real-world success rates.

## Link
- [https://arxiv.org/abs/2606.12366v1](https://arxiv.org/abs/2606.12366v1)
