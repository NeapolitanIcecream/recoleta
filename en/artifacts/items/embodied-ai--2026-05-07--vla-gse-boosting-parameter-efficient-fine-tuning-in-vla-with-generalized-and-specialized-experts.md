---
source: arxiv
url: https://arxiv.org/abs/2605.06175v2
published_at: '2026-05-07T12:56:58'
authors:
- Yuhua Jiang
- Junjie Lu
- Xinyao Qin
- Xiaoyu Chen
- Kaixin Wang
- Feifei Gao
- Li Zhao
topics:
- vision-language-action
- parameter-efficient-finetuning
- robot-manipulation
- mixture-of-experts
- svd-initialization
- libero-plus
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# VLA-GSE: Boosting Parameter-Efficient Fine-Tuning in VLA with Generalized and Specialized Experts

## Summary
VLA-GSE improves parameter-efficient fine-tuning for vision-language-action models by adding SVD-initialized shared and routed low-rank experts to a frozen VLM backbone. It reports higher LIBERO-Plus zero-shot success than full fine-tuning and PEFT baselines while training 2.51% of model parameters.

## Problem
- VLA models need to adapt pretrained vision-language backbones to low-level robot actions, but robot datasets are limited and control requires precise behavior.
- Full fine-tuning can overfit robot data and damage pretrained vision-language ability.
- Standard PEFT methods such as LoRA preserve more VLM knowledge, but the paper claims they under-adapt on precise manipulation tasks.

## Approach
- VLA-GSE keeps most of the VLM backbone frozen and trains a structured low-rank update plus an action head.
- For each frozen weight matrix, it runs SVD. The leading singular components initialize an always-active generalized expert, and later disjoint singular segments initialize specialized experts.
- A top-k router selects specialized experts per input, while the generalized expert is always used.
- Expert-wise gradient scale balancing sets each specialized expert scale inversely to the trace of its assigned singular values, so experts with different spectral magnitudes get comparable update sizes.
- Backbone weight adjustment subtracts the expected initialized expert contribution from the frozen weight, so the block matches the original backbone in expectation at initialization.

## Results
- VLA-GSE trains 114.04M of 4,551.85M parameters, or 2.51%; 48.41M are GSE parameters and 65.62M are action-head parameters.
- On LIBERO-Plus zero-shot evaluation, VLA-GSE reaches 81.2% average success, above ABot-M0 at 80.5%, VLANeXt at 80.1%, and OpenVLA-OFT at 69.6%.
- In a same-backbone fine-tuning comparison, VLA-GSE reaches 81.2% versus FFT at 74.9%, LoRA at 69.2%, MoLoRA at 76.2%, and GOAT at 76.8%; the gains are +6.3 points over FFT and +4.4 points over GOAT.
- LIBERO-Plus perturbation scores for VLA-GSE are 64.4% Camera, 68.5% Robot, 88.8% Language, 97.3% Light, 97.3% Background, 79.4% Noise, and 82.6% Layout.
- The paper reports 82.5% real-world manipulation success across four tasks and four distribution shifts, +16.7 points over FFT.
- The paper states that VLA-GSE keeps pretrained multimodal understanding close to LoRA after VLA fine-tuning, while FFT and co-trained VLA baselines lose more VLM capability; the excerpt does not include the exact benchmark table values.

## Link
- [https://arxiv.org/abs/2605.06175v2](https://arxiv.org/abs/2605.06175v2)
