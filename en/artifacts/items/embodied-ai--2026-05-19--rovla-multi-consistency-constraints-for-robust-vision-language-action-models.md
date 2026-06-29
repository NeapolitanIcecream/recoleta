---
source: arxiv
url: https://arxiv.org/abs/2605.19678v1
published_at: '2026-05-19T11:10:20'
authors:
- Jingzhou Luo
- Yifan Wen
- Yongjie Bai
- Xinshuai Song
- Yang Liu
- Liang Lin
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# RoVLA: Multi-Consistency Constraints for Robust Vision-Language-Action Models

## Summary
RoVLA trains a vision-language-action policy to keep its action predictions stable under paraphrased instructions, denoising-stage changes, and perturbed observations. The excerpt claims stronger performance on LIBERO-Plus, RoboTwin 2.0, and real robot tasks, but it does not include success-rate tables or exact gains.

## Problem
- VLA policies can fail when camera view, lighting, background, robot state, or wording changes while the task stays the same.
- This matters for manipulation because a robot that works only under matched train-test conditions will be unreliable in homes, labs, and factories.
- Prior work often improves VLA behavior through more data, post-training, or world modeling, while RoVLA makes consistency under task-preserving changes part of training.

## Approach
- RoVLA uses a dual-system VLA policy: InternVL3.5-2B extracts language and visual tokens, and a 32-layer DiT action generator predicts continuous action chunks with conditional flow matching.
- Instructional Consistency samples semantically equivalent paraphrases during training. On LIBERO and real tasks, Qwen3-8B generates about 15 paraphrases per trajectory; RoboTwin 2.0 already provides 100 equivalent instructions per task.
- Evolutionary Consistency samples two flow-matching timesteps, τ1 and τ2, and penalizes disagreement between their predicted velocity fields for the same action target.
- Observational Consistency perturbs visual semantic features and robot state along gradients that increase the consistency loss, then trains the perturbed branch to match the clean branch with a stop-gradient target.
- The total loss combines supervised flow-matching losses on clean and perturbed inputs with the EC and OC consistency losses, using an adaptive weight based on an EMA of the clean supervised loss.

## Results
- The provided excerpt gives no quantitative success rates, error rates, confidence intervals, or exact baseline margins.
- The paper claims RoVLA outperforms strong baselines and gives better robustness and generalization on LIBERO-Plus, RoboTwin 2.0, and real-world manipulation tasks.
- LIBERO-Plus evaluation covers 7 perturbation dimensions: layout, camera, robot initialization, language, light, background, and sensor noise.
- LIBERO training uses 1,693 base demonstrations and 15,874 LIBERO-Plus perturbation-augmented demonstrations.
- RoboTwin 2.0 evaluation covers 50 dual-arm manipulation tasks, with 2,500 clean demonstrations and 25,000 randomized-environment demonstrations collected for training.
- Real-world testing uses a Franka Research 3 robot, 5 tabletop tasks, and 125 demonstrations total.

## Link
- [https://arxiv.org/abs/2605.19678v1](https://arxiv.org/abs/2605.19678v1)
