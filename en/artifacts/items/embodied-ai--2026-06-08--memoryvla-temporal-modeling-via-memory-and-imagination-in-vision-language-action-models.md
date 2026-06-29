---
source: arxiv
url: https://arxiv.org/abs/2606.09827v1
published_at: '2026-06-08T17:59:53'
authors:
- Hao Shi
- Weiye Li
- Bin Xie
- Yulin Wang
- Renping Zhou
- Tiancai Wang
- Xiangyu Zhang
- Ping Luo
- Gao Huang
topics:
- vision-language-action
- robot-foundation-model
- temporal-modeling
- world-model
- long-horizon-manipulation
- robot-memory
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# MemoryVLA++: Temporal Modeling via Memory and Imagination in Vision-Language-Action Models

## Summary
MemoryVLA++ adds long-term memory and latent future prediction to a vision-language-action robot policy. It targets manipulation tasks where the robot must remember earlier interactions or anticipate object motion before acting.

## Problem
- Many VLA policies, including OpenVLA and π0, mainly use the current image, so they fail when the present view does not reveal the task state.
- Button pressing needs memory because the scene can look similar before and after the press; conveyor grasping needs future prediction because object motion changes the best grasp time.
- Directly adding past frames or predicted RGB video is costly and can add redundant or control-irrelevant visual data.

## Approach
- A 7B Prismatic VLM encodes the current RGB observation and language instruction into perceptual tokens for visual detail and a cognitive token for task semantics.
- A Perceptual-Cognitive Memory Bank stores past perceptual and cognitive tokens, retrieves relevant history with cross-attention, fuses it through learned gates, and merges similar adjacent entries when memory reaches capacity.
- A 1.5B Stable Video Diffusion world model, adapted on manipulation videos, predicts future dynamics in latent space through partial denoising rather than decoding future RGB frames.
- Memory-augmented tokens guide the integration of imagined future latents, producing temporal tokens that combine current perception, past memory, and future cues.
- A diffusion action expert uses these tokens to predict action sequences for single-arm or dual-arm manipulation.

## Results
- The paper reports experiments on 5 simulation benchmarks and 3 real-robot task categories across 3 robots, covering nearly 200 tasks.
- In simulation, MemoryVLA++ reaches 98.4% success on Libero and 74.0% on SimplerEnv, with a maximum SimplerEnv gain of 16.7 percentage points over baselines.
- On long-horizon temporal tasks, it reaches 44.4% success on Mikasa-Robo and a 4.29 score on Calvin, with a 15.0 percentage-point gain on Mikasa-Robo over the baseline.
- On Libero-Plus, it reaches 82.7% success under task and environment variations.
- In real-robot tests, it scores 85% on general manipulation, 83% on long-horizon memory-dependent tasks, and 77% on long-horizon imagination-dependent tasks.
- The reported real-robot gains over the baseline are +9, +26, and +28 percentage points for those three task groups.

## Link
- [https://arxiv.org/abs/2606.09827v1](https://arxiv.org/abs/2606.09827v1)
