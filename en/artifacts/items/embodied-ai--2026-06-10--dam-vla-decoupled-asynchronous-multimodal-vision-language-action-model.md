---
source: arxiv
url: https://arxiv.org/abs/2606.12105v1
published_at: '2026-06-10T13:59:07'
authors:
- Pankhuri Vanjani
- Zhuoyue Li
- Jakub Suliga
- Moritz Reuss
- Gianluca Geraci
- Xinkai Jiang
- Rudolf Lioutikov
topics:
- vision-language-action
- robot-foundation-model
- asynchronous-control
- multimodal-sensing
- force-torque
- dexterous-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# DAM-VLA: Decoupled Asynchronous Multimodal Vision Language Action model

## Summary
DAM-VLA claims that VLA policies work better when vision, language, force, and proprioception update at their own rates. It reports 95.2% average success on seven real robot manipulation tasks while running smooth 100 Hz control.

## Problem
- Standard VLA models process all inputs on one clock, which wastes compute on slow signals like language and vision and misses fast contact signals like force and torque.
- This matters for contact-rich manipulation because force spikes can happen at 100 to 500 Hz, while RGB frames carry useful changes closer to 3 to 10 Hz.
- Synchronous action generation waits for a full observation bundle, which adds latency and limits reactive control.

## Approach
- DAM-VLA keeps a latent buffer for each modality. Language is encoded once, vision updates sparsely, and force plus proprioception update at the control rate.
- The action head reads all buffers at every control step, so action output can continue even when slow modalities have no new input.
- Vision uses a short-term memory buffer: 16 visual frames at 25 Hz, about 0.64 seconds of context.
- Force and proprioception use dense histories: 96 samples at 100 Hz, about 0.96 seconds of contact and state context.
- New modality information enters the X-VLA action expert through gated cross-attention modules, which leave the pretrained self-attention weights unchanged.

## Results
- On seven real Franka manipulation tasks with 15 trials per task, DAM-VLA reaches 95.2% average success versus 40.95% for X-VLA_25, the strongest synchronous baseline. That is a +54.25 percentage point gain and about 2.32x higher success.
- Naive high-frequency synchronous X-VLA_100 drops to 21.9% average success, below X-VLA_25 at 40.95%, showing that upsampling visual frames to 100 Hz hurts performance in this setup.
- DAM-VLA succeeds on tasks where X-VLA_25 fails or nearly fails: Handwash 100.0% vs 0.0%, Lego 93.3% vs 0.0%, Socket 80.0% vs 6.7%, and Button 93.3% vs 13.3%.
- The strongest concatenation baseline, X-VLA_AFM, uses force and memory but reaches 54.3% average success, far below DAM-VLA at 95.2%.
- Ablations show additive gains: async alone 40.0%, async plus visual memory 58.1%, async plus force 66.7%, and full DAM-VLA 95.2%.
- The reported controller runs at 100 Hz. Replanning rates are about 1 Hz for X-VLA_25, 3.5 Hz for X-VLA_100, and 5.5 Hz for DAM-VLA with s=22; a 200 Hz controller test reports about 8 to 17 Hz replanning depending on s.

## Link
- [https://arxiv.org/abs/2606.12105v1](https://arxiv.org/abs/2606.12105v1)
