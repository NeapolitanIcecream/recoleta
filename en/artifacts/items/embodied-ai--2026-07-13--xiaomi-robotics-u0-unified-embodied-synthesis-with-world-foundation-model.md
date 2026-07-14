---
source: arxiv
url: https://arxiv.org/abs/2607.11643v1
published_at: '2026-07-13T14:57:58'
authors:
- Xinghang Li
- Jun Guo
- Qiwei Li
- Long Qian
- Hang Lai
- Yueze Wang
- Hongyu Yan
- Jiahang Cao
- Xi Chen
- Jingen Qu
- Jiaxi Song
- Nan Sun
- Hanye Zhao
- Futeng Liu
- Wanli Peng
- Heyun Wang
- Yunhong Wang
- Caoyu Xia
- Jack Zhao
- Diyun Xiang
- Hangjun Ye
- Heng Qu
- Huaping Liu
- Jason Li
topics:
- embodied-foundation-model
- world-model
- robot-data-scaling
- vision-language-action
- sim2real
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# Xiaomi-Robotics-U0: Unified Embodied Synthesis with World Foundation Model

## Summary
Xiaomi-Robotics-U0 is a 38-billion-parameter multimodal model that unifies image generation, embodied scene synthesis, scene transfer, and robot video prediction. It uses a world foundation model to generate consistent robot observations and synthetic manipulation trajectories for policy training.

## Problem
- General image and video models produce inconsistent geometry, viewpoints, robot states, and interaction dynamics when applied to robotics.
- Robot-specific adaptation often uses smaller, repetitive datasets and can weaken the visual knowledge and generalization learned during large-scale pre-training.
- Reliable embodied generation matters because robot policies need physically compatible multi-view observations and diverse future trajectories for training and out-of-distribution performance.

## Approach
- Start from the EMU3.5 model, based on a Qwen-3-32B decoder-only Transformer, and train all tasks with one multimodal next-token prediction objective.
- Co-train general text-to-image and image-editing data with embodied scene generation, multi-view embodied transfer, subtask prediction, and manipulation video generation.
- Use structured controls for workspace, target objects, irrelevant objects, lighting, and background, plus depth and robot-action signals to preserve geometry and interaction states.
- Train on both sparse and dense video sequences at 1, 3, and 5 FPS to model long-horizon task progress and fine-grained manipulation dynamics.
- Add FlashAR+ decoding, which generates image tokens along anti-diagonals in parallel; the paper reports up to 82.9x faster 1024x1024 image generation than serial next-token decoding.

## Results
- The model uses 9.5 million single-step samples containing 56.4 billion tokens and 2.6 million video clips containing 49.6 billion tokens.
- It improves the out-of-distribution success rate of the downstream \(\pi_{0.5}\) policy on challenging real-world manipulation tasks from 36.9% to 63.2% with generated data.
- It reports higher human-evaluation scores than GPT-Image-2.0 for embodied scene generation and embodied transfer.
- It ranks first on the World Arena benchmark for embodied video generation and claims state-of-the-art results on single-step and sequential embodied generation tasks.
- The excerpt gives no detailed human-evaluation scores, World Arena scores, task-by-task baselines, or statistical significance results.

## Link
- [https://arxiv.org/abs/2607.11643v1](https://arxiv.org/abs/2607.11643v1)
