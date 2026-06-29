---
source: arxiv
url: https://arxiv.org/abs/2604.24921v1
published_at: '2026-04-27T19:02:46'
authors:
- Yifei Wei
- Linqing Zhong
- Yi Liu
- Yuxiang Lu
- Xindong He
- Maoqing Yao
- Guanghui Ren
topics:
- vision-language-action
- generalist-robot-policy
- robot-manipulation
- hierarchical-control
- diffusion-policy
- asynchronous-inference
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Libra-VLA: Achieving Learning Equilibrium via Asynchronous Coarse-to-Fine Dual-System

## Summary
Libra-VLA is a vision-language-action policy for robot manipulation that splits action generation into coarse discrete intent and continuous fine control. The paper claims higher success rates on LIBERO and LIBERO-Plus while running the expensive VLM planner less often.

## Problem
- Many VLA policies map images and language straight to high-frequency motor commands, which makes one model handle semantic reasoning and precise control at the same time.
- This matters because manipulation has a natural hierarchy: the robot first needs a broad direction or target, then needs precise pose adjustment for contact and alignment.
- Prior temporal hierarchies shorten long tasks, but they still leave each low-level step as a hard translation from language-vision features to continuous actions.

## Approach
- Libra-VLA factorizes the policy into `P(fine action | coarse action, observation) * P(coarse action | observation, instruction)`.
- The Semantic Planner uses an InternVL2.5-2B VLM with a parallel coarse-action head to predict discrete macro-direction tokens from quantized normalized actions.
- The Action Refiner uses a diffusion transformer plus a SigLIP visual encoder to turn the coarse intent into continuous robot actions.
- Training combines cross-entropy for coarse tokens with diffusion MSE for fine actions, and uses a curriculum that moves from ground-truth coarse tokens to planner-predicted tokens.
- At inference, the planner predicts a longer coarse horizon into a FIFO intent buffer; with `M=2` and action chunk size `5`, it predicts `10` coarse steps while the refiner runs at the control rate.

## Results
- On LIBERO, Libra-VLA reports `97.2%` average success, compared with `96.9%` for pi0.5, `96.5%` for GE-Act, and `96.3%` for DD-VLA.
- LIBERO suite scores are `98.6%` Spatial, `99.4%` Object, `98.0%` Goal, and `92.8%` Long.
- On LIBERO-Plus zero-shot transfer, Libra-VLA reports `79.5%` average success, compared with `69.6%` for OpenVLA-OFT and `61.6%` for pi0-Fast.
- LIBERO-Plus zero-shot category scores are `68.9%` Camera, `48.8%` Robot, `92.7%` Language, `97.9%` Light, `93.4%` Background, `86.3%` Noise, and `77.5%` Layout.
- The paper states that simulation and real-world experiments use no large-scale robot-data pretraining; the excerpt gives no real-world success-rate numbers.
- The paper claims an inverted-U relation between action decomposition granularity and performance, with best performance when planner and refiner learning difficulty is balanced; the excerpt gives no ablation numbers for this claim.

## Link
- [https://arxiv.org/abs/2604.24921v1](https://arxiv.org/abs/2604.24921v1)
