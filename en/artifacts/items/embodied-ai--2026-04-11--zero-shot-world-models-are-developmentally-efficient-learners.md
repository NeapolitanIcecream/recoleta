---
source: arxiv
url: http://arxiv.org/abs/2604.10333v1
published_at: '2026-04-11T19:32:33'
authors:
- Khai Loong Aw
- Klemen Kotar
- Wanhee Lee
- Seungwoo Kim
- Khaled Jedoui
- Rahul Venkatesh
- Lilian Naing Chen
- Michael C. Frank
- Daniel L. K. Yamins
topics:
- world-model
- self-supervised-video
- zero-shot-vision
- physical-reasoning
- developmental-learning
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# Zero-shot World Models Are Developmentally Efficient Learners

## Summary
This paper introduces the Zero-shot World Model (ZWM), a self-supervised visual predictor that aims to learn flexible physical scene understanding from limited natural video and solve tasks without task-specific training. The main claim is that a model trained on child egocentric video can perform optical flow, depth, segmentation, and simple physical reasoning zero-shot, while staying competitive with strong supervised systems.

## Problem
- The paper targets two gaps in current visual learning: poor data efficiency on natural child-like video and weak zero-shot task use from learned representations.
- Standard self-supervised vision models often need labeled readouts for each downstream task, which does not match how children appear to reuse one general visual system across tasks.
- This matters for both cognitive modeling and AI because a system that learns broad physical understanding from limited real-world experience would reduce dependence on curated data and task-specific supervision.

## Approach
- ZWM trains a masked two-frame predictor on video pairs. It sees the first frame fully, but only about 10% of patches from the second frame, and learns to reconstruct the full second frame.
- This asymmetric masking is meant to force the model to separate appearance information from motion and scene dynamics, using dense content from frame 1 and sparse motion clues from frame 2.
- After training, the model is queried zero-shot by making a small input change, running the predictor on the original and perturbed inputs, and comparing the outputs. The difference is used to extract a target quantity such as motion, depth, or object membership.
- The paper describes this as approximate causal inference: move one patch on an object, see what else changes in the prediction, and use that propagated change to recover object segmentation or other structure.
- More complex tasks are built by composing simpler extractions, such as deriving optical flow first, then using stereo flow for relative depth, or hypothetical motion plus flow for segmentation and intuitive physics.

## Results
- Training data: BabyZWM is trained only on BabyView child egocentric video, with **868 hours** total from **34** children. The paper says this is about **3 months of waking experience**.
- Model scale and setup: ZWM uses ViT backbones at **170M** and **1B** parameters, trains on frame gaps of **150-450 ms**, inputs of **256x256**, and reveals **10%** of second-frame patches.
- Optical flow: the paper claims **state-of-the-art** or near-state-of-the-art zero-shot flow performance. On **TAP-Vid-DAVIS**, BabyZWM is described as competitive with supervised **CoTracker3**, **DPFlow**, and **SeaRAFT**, and it matches supervised baselines on occlusion detection. On **TAP-Vid-Kubric**, it is strong but slightly below supervised models trained on synthetic data. Exact scores are not provided in the excerpt.
- Relative depth: on **UniQA-3D**, both ZWM and BabyZWM achieve **over 90% accuracy** zero-shot. The paper says they beat **Gemini-1.5**, **GPT-4-Turbo**, and **GPT-4o**, are comparable to supervised **MiDaS-CNN** and self-supervised **MonoDepth2** monocular methods, and trail only a supervised binocular model.
- Object segmentation: on **SpelkeBench**, BabyZWM is said to rival supervised **Mask2Former** variants and perform slightly below **SAM2**. The excerpt gives no exact segmentation numbers.
- Intuitive physics: on the authors' short-timescale physical reasoning benchmark, **ZWM, BabyZWM, and V-JEPA2 approach 100% performance across all categories**, while **Baby V-JEPA2** does not. The benchmark covers cohesion, support, force transfer, and force separation.
- Data efficiency: a **single-child** version trained on **132 hours** from one child performs similarly to the full BabyZWM across most tasks. An age-ordered single-pass training setup also performs similarly, suggesting tolerance to continual-learning style curricula.
- Ablation: symmetric masking variants (**45%-45%** and **90%-90%**) perform substantially worse than the standard asymmetric setup, supporting the claim that temporally factored masking helps zero-shot abstraction and data efficiency. Many headline comparisons are qualitative in the excerpt because full tables are not included.

## Link
- [http://arxiv.org/abs/2604.10333v1](http://arxiv.org/abs/2604.10333v1)
