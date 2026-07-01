---
source: arxiv
url: https://arxiv.org/abs/2606.31382v1
published_at: '2026-06-30T09:10:31'
authors:
- Fengnian Zhang
- Tao Huang
- Siyu Xu
- Zhong Jin
- Chang Xu
topics:
- vision-language-action
- robot-policy-compression
- vlm-to-vla-adaptation
- parameter-pruning
- libero-benchmark
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Revisiting Parameter Redundancy in Vision-Language-Action Models: Insights from VLM-to-VLA Adaptation

## Summary
The paper studies which VLM parameters still matter after a VLM is adapted into a VLA robot policy. It claims that pruning based on VLM-to-VLA weight changes can shrink OpenVLA and pi_0.5 by 12%–30% while keeping about 90% of original LIBERO success without fine-tuning.

## Problem
- VLA models inherit large VLM backbones, which raises memory and compute cost for robot deployment.
- Common pruning methods damage robot policies and then use LoRA, RL, or SVD corrections; this hides whether the removed weights were redundant.
- The paper asks whether weight changes during VLM-to-VLA adaptation identify attention heads and FFN channels that matter for action generation.

## Approach
- The authors compare paired models: Prismatic to OpenVLA, and PaLI-Gemma to pi_0.5.
- They compute relative L2 weight divergence between the VLM and VLA weights for shared modules.
- They rank attention heads and FFN channels by divergence, then prune highest-divergence or lowest-divergence subsets without fine-tuning to measure the direct effect on LIBERO success rate.
- They handle vision, language, and projector modules separately because the same divergence signal has different meaning across modules.
- They use the observed module patterns to build a joint pruning scheme that removes parameters while avoiding post-pruning recovery.

## Results
- On LIBERO-Spatial with OpenVLA, baseline success rate is 84.7%. Pruning 20% of LLM FFN channels by lowest divergence drops pre-fine-tuning success to 1.5%, while 20% highest-divergence pruning keeps 76.3%.
- In the same OpenVLA setting, LoRA recovery for 10k steps raises damaged models back to high success: 20% lowest-divergence pruning goes from 1.5% to 86.5%, and 50% lowest-divergence pruning goes from 0.0% to 81.0%.
- OpenVLA DINOv2 shows opposite behavior by submodule: pruning 12.5% highest-divergence attention heads gives 1.6% SR, while pruning 20% lowest-divergence FFN channels gives 0.0% SR.
- OpenVLA language modules also show strong sensitivity: pruning 12.5% lowest-divergence Llama2 attention heads gives 0.0% SR, while highest-divergence attention-head pruning keeps 84.3% SR.
- For pi_0.5, the excerpt reports that pruning highest-divergence FFN channels in both vision and language keeps about 95.0% SR, while removing lowest-divergence channels causes large drops.
- The final claim is 12%–30% parameter reduction on OpenVLA and pi_0.5 while maintaining about 90% of original LIBERO performance without post-pruning recovery; existing pruning criteria are reported to collapse under the same no-recovery setting.

## Link
- [https://arxiv.org/abs/2606.31382v1](https://arxiv.org/abs/2606.31382v1)
