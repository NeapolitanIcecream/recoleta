---
source: arxiv
url: https://arxiv.org/abs/2606.20246v1
published_at: '2026-06-18T13:57:12'
authors:
- Gia-Binh Nguyen
- Trong-Bao Ho
- Thien-Loc Ha
- Khoa Vo
- "Philip Lund M\xF8ller"
- Quang T. Nguyen
- Long Dinh
- Tuan Dam
- Vu Duong
- Tung M. Luu
- Trung Le
- Tran Nguyen Le
- Minh Vu
- An Thai Le
- Ngan Le
- Daniel Sonntag
- James Zou
- Jan Peters
- Duy M. H. Nguyen
- Ngo Anh Vien
topics:
- vision-language-action
- layer-pruning
- robot-finetuning
- model-compression
- generalist-robot-policy
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Finetuning Vision-Language-Action Models Requires Fewer Layers Than You Think

## Summary
CLP removes redundant transformer layers from pretrained VLA robot policies before fine-tuning. It cuts training and inference cost while keeping, and sometimes improving, manipulation success rates.

## Problem
- Modern continuous-control VLA models such as π0 and GR00T-N1.5 have billions of parameters, which makes downstream fine-tuning expensive and real-time robot inference slow.
- Many existing VLA efficiency methods mainly reduce inference cost, add routing modules, or target older autoregressive action-token models instead of current flow or diffusion action policies.
- The paper asks whether pretrained VLA layers can be removed before fine-tuning so robot labs train smaller policies without giving up task success.

## Approach
- The method, CKA-guided Layer Pruning (CLP), runs one calibration forward pass through a pretrained VLA using a small set of robot episodes.
- It computes Centered Kernel Alignment between adjacent transformer layers in the VLM backbone and the continuous action head. High CKA means two neighboring layers produce similar hidden representations.
- CLP groups contiguous high-similarity layers, keeps the first layer in each group as an anchor, removes the most redundant remaining layers, and reconnects the surviving blocks.
- The pruned model is then fine-tuned with the original VLA training objective, with no auxiliary router, distillation loss, or runtime layer selector.

## Results
- Across π0, GR00T-N1.5, and SmolVLA on LIBERO, CLP reduces model size by 21.3% to 25.9% and trainable parameters by 25.8% to 37.0%.
- On LIBERO training for 60,000 steps, π0 training time drops from 15.5 to 11.2 hours, GR00T-N1.5 drops from 10.7 to 7.4 hours, and SmolVLA drops from 24.75 to 8.83 hours.
- Inference latency on RTX 4070 falls from 211 ms to 152 ms for π0, 121 ms to 85 ms for GR00T-N1.5, and 201 ms to 137 ms for SmolVLA.
- GFLOPs fall from 3073 to 2196.5 for π0, 1010 to 512.4 for GR00T-N1.5, and 598.4 to 536.1 for SmolVLA.
- With only 10% of LIBERO data, CLP reports 84.6% average success for π0, compared with 77.7% for the full π0 baseline and 79.7% for π0-MoLe, with a 1.38× training speedup.
- On SimplerEnv with GR00T-N1.5, average success rises from 16.6% to 20.0%, and training time falls from 22.9 to 15.7 hours. The paper also reports validation on 10 real-world manipulation tasks across 4 robot embodiments, with 15% to 20% gains over full models when using 100 demonstrations.

## Link
- [https://arxiv.org/abs/2606.20246v1](https://arxiv.org/abs/2606.20246v1)
