---
source: arxiv
url: https://arxiv.org/abs/2605.08612v1
published_at: '2026-05-09T02:15:10'
authors:
- Kewei Chen
- Yayu Long
- Shuai Li
- Mingsheng Shang
topics:
- vision-language-action
- robot-security
- backdoor-attacks
- openvla
- adversarial-tuning
- robot-manipulation
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# ATAAT: Adaptive Threat-Aware Adversarial Tuning Framework against Backdoor Attacks on Vision-Language-Action Models

## Summary
ATAAT attacks OpenVLA-style vision-language-action robot policies by planting visual backdoors that survive instruction tuning. Its main claim is that separating benign and backdoor gradients raises targeted attack success above 80% at a 5% poisoning rate while keeping normal task success high.

## Problem
- VLA robot policies depend on visual perception, so a supply-chain attacker can add a trigger that changes robot actions during deployment.
- Standard backdoor attacks fail on VLAs because benign instruction tuning and malicious target-action training push model updates in conflicting directions.
- This matters because persistent backdoors can stay hidden under normal tests and activate on physical objects, spatial states, or human cues.

## Approach
- The paper defines gradient interference with cosine similarity between benign-task gradients and backdoor-task gradients.
- In data poisoning, ATAAT builds poisoned images with a visible trigger plus a small invisible perturbation generated with a proxy feature extractor, so poisoned samples steer training into a separate feature direction.
- In white-box fine-tuning, ATAAT finds dormant neurons using activation statistics on clean data, then uses a binary mask so only those parameters learn the backdoor.
- The triggers can be simple visual objects or semantic conditions such as an open drawer, crossed cutlery, or a person wearing a watch.

## Results
- On LIBERO-Spatial data poisoning with OpenVLA-7B, ATAAT reports 88.8% benign SR and 83.5% TASR; adapted BadVLA reports 17.5% SR and 13.1% TASR, and BadNet reports 4.5% SR and 0.8% TASR.
- On LIBERO-Object data poisoning, ATAAT reports 90.1% SR and 85.9% TASR; adapted BadVLA reports 16.1% SR and 12.8% TASR.
- In fine-tuning poisoning, ATAAT reports 78.1% SR and 72.5% TASR on LIBERO-Spatial, versus 52.1% SR and 39.2% TASR for adapted BadVLA.
- In fine-tuning poisoning on LIBERO-Object, ATAAT reports 79.3% SR and 74.8% TASR, versus 50.8% SR and 37.7% TASR for adapted BadVLA.
- The paper says the method works with a 5% poisoning rate and tracks gradient cosine similarity: BadVLA stays near -0.4 after about 400 steps, while ATAAT stays near 0.
- Real-robot tests are described for fixed objects, pointing hands, object states, and human attributes, but the excerpt does not provide real-world success percentages.

## Link
- [https://arxiv.org/abs/2605.08612v1](https://arxiv.org/abs/2605.08612v1)
