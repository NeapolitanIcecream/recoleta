---
source: arxiv
url: https://arxiv.org/abs/2605.12334v1
published_at: '2026-05-12T16:16:15'
authors:
- Yucen Wang
- Rui Yu
- Fengming Zhang
- Junjie Lu
- Xinyao Qin
- Tianxiang Zhang
- Kaixin Wang
- Li Zhao
topics:
- vision-language-action
- world-model
- robot-foundation-model
- generalist-robot-policy
- robot-data-scaling
- sim2real
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# Reinforcing VLAs in Task-Agnostic World Models

## Summary
RAW-Dream trains a VLA policy with RL inside a frozen or lightly adapted task-agnostic video world model, using Qwen3-VL as a zero-shot reward judge. The main claim is that broad play-style robot data can replace task-specific world-model and reward-model training for new manipulation tasks.

## Problem
- Current world-model RL methods for VLAs usually train the world model and reward model on target-task rollouts, often thousands of trajectories.
- That data requirement weakens the main benefit of imagined RL, since each new task still needs new robot data before training can start.
- The problem matters for robot foundation models because deployment often brings new objects, layouts, and instructions that were absent during world-model training.

## Approach
- RAW-Dream pre-trains an action-conditioned video world model on broad task-free robot behavior, such as play data or noisy exploratory rollouts, rather than target-task demonstrations.
- The world model uses a Wan 2.1-T2V-1.3B Diffusion Transformer backbone with action conditioning through AdaLN and causal temporal masking.
- The VLA policy is OpenVLA-OFT. It first gets minimal task anchoring through 1-shot SFT, then trains with GRPO in imagined rollouts.
- Rewards come from frozen Qwen3-VL, which gives binary success judgments from the imagined video and text instruction.
- Dual-Noise Verification reruns action sequences with fresh diffusion noise and discards trajectories where Qwen3-VL changes a success judgment to failure, reducing reward hacking from world-model hallucinations.

## Results
- On LIBERO, the 1-shot SFT baseline averages 43.4% success across Spatial, Object, Goal, and Long. RAW-Dream with a zero-shot world model reaches 52.3%, a +8.9 point gain using 10 target demonstrations and 0 target rollouts for world-model training.
- RAW-Dream with Co-Train WM reaches 57.1% average success with 10 target demonstrations, compared with Online RL Short at 47.9% using 522 target episodes with ground-truth simulator rewards.
- RAW-Dream with ID-FT WM reaches 66.0% average success using 510 target data, above WoVR WM at 60.9% using 2,510 target data.
- Per-suite ID-FT WM success rates are 82.0% Spatial, 79.8% Object, 63.4% Goal, and 38.6% Long, compared with 54.6%, 46.4%, 52.2%, and 20.2% for 1-shot SFT.
- For world-model prediction, ID-FT WM uses 500 target rollouts and beats WoVR trained from scratch on 2,500 target rollouts on FVD across all suites: Spatial 23.52 vs 45.39, Object 26.82 vs 92.11, Goal 21.65 vs 41.78, Long 38.84 vs 80.52.
- In real-world robot experiments, the paper reports a +21.7 absolute success-rate gain over a 3-shot SFT baseline per task.

## Link
- [https://arxiv.org/abs/2605.12334v1](https://arxiv.org/abs/2605.12334v1)
