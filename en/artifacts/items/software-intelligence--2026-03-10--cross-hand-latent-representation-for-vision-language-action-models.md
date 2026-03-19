---
source: arxiv
url: http://arxiv.org/abs/2603.10158v1
published_at: '2026-03-10T18:50:57'
authors:
- Guangqi Jiang
- Yutong Liang
- Jianglong Ye
- Jia-Yang Huang
- Changwei Jing
- Rocky Duan
- Pieter Abbeel
- Xiaolong Wang
- Xueyan Zou
topics:
- vision-language-action
- dexterous-manipulation
- cross-embodiment
- latent-action-space
- robot-learning
relevance_score: 0.32
run_id: materialize-outputs
language_code: en
---

# Cross-Hand Latent Representation for Vision-Language-Action Models

## Summary
This paper proposes XL-VLA, a vision-language-action model that unifies the actions of multiple dexterous hands into a shared latent space for cross-hand training and transfer. Its core value is reducing the cost of collecting large amounts of demonstration data separately for each new hand type, while improving generalization for real-world robotic dexterous manipulation.

## Problem
- The action space of dexterous hands is defined by the specific hardware joints; different hand types vary greatly in joint count, structure, and actuation, making it difficult for standard VLA models to directly share data and policies.
- As new dexterous hands continue to emerge, collecting large-scale demonstration data separately for each embodiment is both expensive and unscalable.
- Without learning a unified action representation across embodiments, robots struggle to achieve cross-hand reuse, zero-shot transfer, and more robust real-world operation.

## Approach
- The paper proposes a **shared latent action space**: each hand has its own encoder/decoder, but all map into the same latent space, so actions from different hand types are first converted into a "universal action code" and then decoded back into their respective joint commands.
- The latent space is pretrained with a multi-head VAE-style autoencoder using three types of constraints: joint reconstruction loss, a cross-hand fingertip geometric alignment loss based on differentiable forward kinematics, and KL latent regularization.
- This latent-space training is **unpaired and without demonstrations**: it only requires randomly sampling poses within each hand's joint limits, then aligning representations through cross-hand decoding and fingertip geometric consistency.
- In the VLA stage, the model does not directly predict raw joint sequences, but instead predicts the next latent action chunk; the hand-specific encoders/decoders are frozen, and only the VLA action expert is fine-tuned, turning a standard VLA architecture into a hand-agnostic policy.
- The authors also build a real-world dataset: 4 dexterous hands, 10 tasks, 2,000 demonstrations, and about 2M state-action pairs.

## Results
- In cross-embodiment training across 4 hands × 10 tasks, XL-VLA improves the overall average success rate relative to the baseline **\(\pi_0\)** from **0.32 to 0.72**, marked in the table as **+40%** (Table 2, cross-hand average).
- Broken down by hand type: Ability **0.37 → 0.73**, Inspire **0.27 → 0.68**, Paxini **0.35 → 0.78**, XHand **0.29 → 0.70**; this indicates that both structurally similar and substantially different hands benefit.
- By task average: PF **0.20 → 0.70**, SC **0.28 → 0.63**, SoC **0.08 → 0.55**, HB **0.40 → 0.95**, RL **0.10 → 0.43**, PS **0.68 → 0.95**, RB **0.45 → 0.90**, PuS **0.25 → 0.35**, PoS **0.23 → 0.88**, PC **0.55 → 0.90**.
- The paper text also claims that the "average success rate across tasks and hands" can improve from **0.55 to 0.90 (+0.35)**, but this is not fully consistent with the figures reported in Table 2; the strongest reliable conclusion is that XL-VLA consistently outperforms standard VLA in raw joint space across all hands and tasks.
- The authors further claim that the method supports **zero-shot generalization to unseen hand-task combinations**, and also brings gains when jointly trained across different robotic systems (xArm and G1 humanoid), but the provided excerpt does not include the full corresponding quantitative tables.

## Link
- [http://arxiv.org/abs/2603.10158v1](http://arxiv.org/abs/2603.10158v1)
