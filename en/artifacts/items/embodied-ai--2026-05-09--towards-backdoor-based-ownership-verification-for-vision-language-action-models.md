---
source: arxiv
url: https://arxiv.org/abs/2605.09005v1
published_at: '2026-05-09T15:44:19'
authors:
- Ming Sun
- Rui Wang
- Xingrui Yu
- Lihua Jing
- Hangyu Du
- Zhenglin Wan
- Xu Pan
- Ivor Tsang
topics:
- vision-language-action
- model-watermarking
- ownership-verification
- robot-policy-security
- libero-benchmark
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Towards Backdoor-Based Ownership Verification for Vision-Language-Action Models

## Summary
GuardVLA is a watermarking method for vision-language-action models that verifies whether a released robot policy was copied after fine-tuning. It trains the model on images carrying a secret steganographic message, then checks for that watermark with swapped verification modules rather than by changing robot actions.

## Problem
- VLA models are costly to train and easy to reuse after open release, so owners need evidence that a deployed model came from their model.
- Standard ownership tests are weak for VLAs because different robot policies can complete the same task with similar action traces.
- A verification method must preserve normal task success and avoid trigger behavior that causes unsafe robot actions.

## Approach
- During watermark embedding, the owner adds a fixed 6-bit secret message to embodied visual observations with an image steganography encoder, then fine-tunes the protected VLA on those inputs.
- The method also trains a clean model on normal data and a noise model on images with random messages, so the verifier can learn the target watermark signal.
- A trigger projector and classifier head are co-trained with binary cross-entropy and triplet loss; the clean model is the anchor, the noise model is the positive, and the watermarked model is separated as the negative.
- At audit time, the verifier first checks task success rate in benign mode, then swaps in the trigger projector and classifier head to compute watermark identification confidence (WIC).

## Results
- On LIBERO with OpenVLA-OFT, watermarked WIC was 100.00% on Spatial, 99.72% on Goal, 100.00% on Object, and 99.99% on LIBERO-10; clean WIC was 0.01%, 0.00%, 0.60%, and 0.00%.
- On LIBERO with VLA-Adapter, watermarked WIC was 99.94%, 99.85%, 100.00%, and 99.90% across Spatial, Goal, Object, and LIBERO-10; clean WIC stayed at 0.12%, 0.50%, 0.04%, and 0.01%.
- On pi_0.5, the watermarked model reached 99.85% WIC, while clean and noise models were 0.03% and 0.01%.
- Benign success rates stayed close to clean baselines: OpenVLA-OFT Object rose from 98.2% to 99.4%, VLA-Adapter LIBERO-10 rose from 89.8% to 93.4%, and pi_0.5 LIBERO-10 rose from 90.8% to 94.2%.
- After downstream adaptation from LIBERO-10 to LIBERO-Spatial, SR stabilized near 99% while WIC stayed close to 100%; after reducing visual inputs to one view, SR stabilized around 85%-87% while WIC stayed close to 100%.

## Link
- [https://arxiv.org/abs/2605.09005v1](https://arxiv.org/abs/2605.09005v1)
