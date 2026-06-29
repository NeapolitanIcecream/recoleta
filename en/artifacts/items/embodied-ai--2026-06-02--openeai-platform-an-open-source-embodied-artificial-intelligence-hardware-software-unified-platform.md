---
source: arxiv
url: https://arxiv.org/abs/2606.03392v1
published_at: '2026-06-02T09:34:08'
authors:
- Jinyuan Zhang
- Luoyi Fan
- Leiyu Wang
- Yeqiang Wang
- Yicheng Zhu
- Cewu Lu
- Nanyang Ye
topics:
- vision-language-action
- robot-foundation-model
- open-robot-hardware
- robot-data-scaling
- real-world-manipulation
- generalist-robot-policy
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# OpenEAI-Platform: An Open-source Embodied Artificial Intelligence Hardware-Software Unified Platform

## Summary
OpenEAI-Platform pairs a $790 open 6+1 DoF arm with OpenEAI-VLA, a Qwen3-VL-4B robot policy trained with public robot and multimodal data. It targets reproducible real-world manipulation, where closed hardware, private training data, and mismatched dataset formats limit comparison and data collection.

## Problem
- Real-world VLA work often depends on private datasets and incomplete training code, so other groups cannot reproduce or extend results.
- Commercial 6+1 DoF arms cost about $1.5k-$40k+ and expose limited low-level control, which blocks cheap data collection and controller research.
- Open robot datasets use different state/action conventions, which makes cross-dataset pretraining and transfer harder.

## Approach
- OpenEAI-Arm is a 6+1 DoF desktop manipulator; its link geometry is chosen by NSGA-III over MDH parameters using manipulation operability and endurance efficiency objectives.
- The controller combines dynamics feedforward PID, friction compensation, rolling action-chunk interpolation, and jerk-bounded S-curve timing to turn VLA action chunks into smooth joint commands.
- OpenEAI-VLA uses Qwen3-VL-Instruct 4B with learnable query tokens that compress image, text, and instruction features into fixed-length conditioning.
- An 18-layer Diffusion Transformer action head with 32 attention heads predicts continuous action chunks through conditional flow matching.
- Training has two stages: pretrain on converted Open X-Embodiment subsets, then fine-tune on small OpenEAI-Arm demonstrations mixed with COCO, VQA-v2, and PixMo-Points.

## Results
- OpenEAI-Arm material cost is $0.79k, compared with $8.60k for ARX R5 and $2.16k for AgileX Piper in the table.
- The arm weighs 3.3 kg, compared with 3.9 kg for ARX R5 and 4.2 kg for Piper.
- Manipulation operability is 0.547, nearly matching ARX R5 at 0.546 and above Piper at 0.179.
- Endurance efficiency is 0.567, above ARX R5 at 0.529 and below Piper at 0.846.
- The evaluation covers 4 real-world tasks: Clean Table, Make Tea, Fold Towel, and Fold T-shirt.
- The excerpt claims OpenEAI-VLA has success rates comparable to π0 while using limited public pretraining data, but the provided text does not include the success-rate numbers.

## Link
- [https://arxiv.org/abs/2606.03392v1](https://arxiv.org/abs/2606.03392v1)
