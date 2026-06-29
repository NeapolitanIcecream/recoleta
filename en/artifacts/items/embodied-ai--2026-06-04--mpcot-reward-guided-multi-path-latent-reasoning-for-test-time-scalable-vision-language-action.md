---
source: arxiv
url: https://arxiv.org/abs/2606.06245v1
published_at: '2026-06-04T14:48:44'
authors:
- Boyang Zhang
- Lianlei Shan
topics:
- vision-language-action
- latent-reasoning
- test-time-scaling
- robot-manipulation
- long-horizon-control
- world-model-supervision
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# MPCoT: Reward-Guided Multi-Path Latent Reasoning for Test-Time Scalable Vision-Language-Action

## Summary
MPCoT adds test-time latent reasoning to OpenVLA-OFT for long-horizon vision-language-action control. It claims higher LIBERO and CALVIN success rates while keeping the same 8-step action output and generating no reasoning tokens.

## Problem
- VLA policies often decode actions in one pass, which gives little room to correct uncertain choices during long instruction chains.
- Explicit chain-of-thought can add reasoning depth, but it adds token latency and routes continuous control through text.
- The problem matters because early robot action errors can compound across multi-step manipulation tasks.

## Approach
- MPCoT starts with M latent action hypotheses from the same observation and language instruction.
- A shared residual refiner updates each hypothesis for K steps, so larger K adds compute without adding new refiner parameters.
- A learned scorer assigns soft weights to the M refined hypotheses, then the model averages them before the unchanged OpenVLA-OFT action head.
- During training, candidate branches get path-preference supervision from expert-action consistency, world-model/VLM progress, and success feedback.
- At inference, MPCoT uses only the learned latent scorer; it does not query rewards, success labels, rollouts, or the world-model/VLM evaluator.

## Results
- On LIBERO with one policy for all 4 suites, MPCoT improves OpenVLA-OFT average success rate from 96.8% to 98.9% and Long success rate from 95.3% to 98.9%.
- On LIBERO with one policy per suite, MPCoT reaches 99.0% average success rate and 97.8% Long success rate, compared with AVA-VLA at 98.3% average and 96.2% Long.
- On CALVIN ABC→D, MPCoT reaches 99.8%, 98.9%, 96.8%, 93.7%, and 89.4% success for 1-step through 5-step chains, with average sequence length 4.92.
- On CALVIN 4-step and 5-step tasks, MPCoT beats AVA-VLA by 3.8 and 5.3 points, and beats OpenVLA-OFT by 13.3 and 16.5 points.
- The best fixed setting, K=5 and M=4, improves LIBERO Long from 95.3% to 98.9% while raising measured latency from 24 ms to 38 ms and adding zero reasoning-token overhead.
- Reward-guided path supervision raises Path Consistency from 68.5% to 84.3% and improves CALVIN 4-step success from 90.8% to 93.7% compared with the no-reward multi-path variant.

## Link
- [https://arxiv.org/abs/2606.06245v1](https://arxiv.org/abs/2606.06245v1)
