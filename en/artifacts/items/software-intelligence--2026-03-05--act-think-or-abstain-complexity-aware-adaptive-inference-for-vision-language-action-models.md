---
source: arxiv
url: http://arxiv.org/abs/2603.05147v1
published_at: '2026-03-05T13:14:41'
authors:
- Riccardo Andrea Izzo
- Gianluca Bardaro
- Matteo Matteucci
topics:
- vision-language-action
- adaptive-inference
- ood-detection
- robot-safety
- uncertainty-estimation
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Act, Think or Abstain: Complexity-Aware Adaptive Inference for Vision-Language-Action Models

## Summary
This paper proposes a complexity-aware adaptive inference framework for Vision-Language-Action (VLA) models that automatically chooses to execute directly, think further, or abstain from execution based on the current state. Its core value is improving generalization and safety while avoiding uniformly applying high-cost reasoning to simple tasks.

## Problem
- Existing VLAs often improve generalization through mechanisms such as chain-of-thought reasoning, but this **indiscriminately increases** computational cost and inference latency.
- These methods typically lack explicit judgment of task complexity and uncertainty, making them prone to being **overconfident on out-of-distribution tasks and causing catastrophic failure**.
- Robot deployment must balance **real-time performance, generalization, and safety** at the same time, and fixed inference strategies struggle to satisfy all three.

## Approach
- The pretrained vision-language backbone of the VLA is transformed from a “passive feature extractor” into a “complexity detector”: embeddings are extracted from visual, textual, and fused representations.
- PCA is first used to reduce features to 64 dimensions, then **GMM** (global distribution) and **1-NN/kNN** (local anomaly) are used to score sample novelty/OOD level.
- These scores are combined into a small vector and fed into a lightweight MLP, which outputs three routing decisions: **Act** (execute known tasks directly), **Think** (trigger additional reasoning for ambiguous tasks), and **Abstain** (stop execution when clearly OOD).
- The Think branch is triggered only once at the first timestep of each episode, enhancing action generation by adding scene cues and subgoals into the prompt.
- During training, LIBERO is treated as ID, LIBERO-PRO as partially OOD, and OOD samples from other tabletop manipulation datasets are introduced; mixup is also used to synthesize intermediate-state features to learn the “Think” boundary.

## Results
- In experiments on **LIBERO / LIBERO-PRO** and a real robot, the authors claim the method is effective; the abstract reports that the **vision-only configuration reaches 80% F1-score using only 5% of the training data**, establishing it as a reliable and efficient task complexity detector.
- Under full-data evaluation, **MLP + GMM (vision-only)** achieves **Macro F1 = 84.34%**, the best configuration; by comparison, **MLP + kNN (vision)** reaches **73.90%**.
- The **baseline MLP** trained directly on raw features achieves only **63.81% Macro F1**; moreover, **86% of “Think” samples are misclassified as “Act”**, indicating overconfidence on ambiguous scenarios.
- Multimodality is not always better: **MLP + GMM(all) + kNN ensemble** achieves **71.41% F1**, while **text-only** reaches only **54.76% F1**, suggesting that text/fused features weaken complexity discrimination.
- In terms of data efficiency, the authors test training ratios of **{0.1%, 1%, 5%, 10%, 25%}** and claim that **5% of the data (fewer than roughly 1,000 samples and close to convergence)** is already near peak performance; the baseline, by contrast, remains around **F1≈0.60** at all data scales.
- An ablation on the number of GMM components shows the best setting is **k=3**; the paper also claims that in the vision-only GMM confusion matrix, leakage from **fully OOD to the “Act” path is 0**, reinforcing the safety claim.

## Link
- [http://arxiv.org/abs/2603.05147v1](http://arxiv.org/abs/2603.05147v1)
