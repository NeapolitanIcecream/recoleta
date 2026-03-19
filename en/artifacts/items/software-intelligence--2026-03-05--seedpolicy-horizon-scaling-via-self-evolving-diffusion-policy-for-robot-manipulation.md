---
source: arxiv
url: http://arxiv.org/abs/2603.05117v2
published_at: '2026-03-05T12:42:53'
authors:
- Youqiang Gui
- Yuxuan Zhou
- Shen Cheng
- Xinyang Yuan
- Haoqiang Fan
- Peng Cheng
- Shuaicheng Liu
topics:
- robot-manipulation
- diffusion-policy
- imitation-learning
- temporal-attention
- long-horizon-control
relevance_score: 0.31
run_id: materialize-outputs
language_code: en
---

# SeedPolicy: Horizon Scaling via Self-Evolving Diffusion Policy for Robot Manipulation

## Summary
SeedPolicy addresses the problem in diffusion-based imitation learning for long-horizon robotic manipulation where “seeing longer actually makes performance worse” by introducing SEGA, a temporal module that can recursively update historical state. It compresses long histories into a fixed-size latent state and uses attention-generated gates to filter irrelevant frames, allowing the diffusion policy to continue benefiting as the observation horizon grows.

## Problem
- Existing Diffusion Policy can model multi-modal expert behavior, but its performance degrades as the observation history becomes longer, limiting long-horizon manipulation.
- Directly stacking image frames cannot effectively model complex temporal dependencies, while standard temporal attention incurs quadratic computational cost as the horizon length increases.
- Robot visual streams contain large amounts of temporally sparse and irrelevant information, such as background changes, occlusions, and noise; writing all of it into history can contaminate decision-making.

## Approach
- Proposes **SEGA (Self-Evolving Gated Attention)**: it maintains a fixed-size latent state that evolves over time, using it to compress long-term history instead of endlessly stacking raw frames.
- In the **state update stream**, the previous state serves as the Query and extracts relevant information from the current observation to produce an intermediate new state.
- It uses cross-attention scores to directly generate the **Self-Evolving Gate (SEG)**, which determines “how much new information to write” and “how much old state to retain,” thereby suppressing irrelevant temporal noise.
- In the **state retrieval stream**, the current observation queries the historical state in reverse order to obtain enhanced observation features, which are then fed to the diffusion action expert to predict future 14-DoF action sequences.
- Integrating SEGA into Diffusion Policy forms **SeedPolicy**, enabling scalable long-horizon modeling with relatively moderate additional overhead.

## Results
- On **50 manipulation tasks** in RoboTwin 2.0, SeedPolicy outperforms DP and other IL baselines; the training setup uses **50 demonstrations per task, 600 epochs, 100 rollout evaluations, and averages over 3 independent trials**.
- In Table 1, under the **Easy** setting: DP-Transformer **33.10%** → SeedPolicy-Transformer **40.08%** (**+6.98** points, about **+21.1%** relative improvement); DP-CNN **28.04%** → SeedPolicy-CNN **42.76%** (**+14.72** points, about **+52.5%** relative improvement).
- Under the **Hard** setting: DP-Transformer **1.44%** → SeedPolicy-Transformer **4.28%** (**+2.84** points, about **+197.2%** relative improvement); DP-CNN **0.64%** → SeedPolicy-CNN **1.54%** (**+0.90** points, about **+140.6%** relative improvement). The paper abstract also reports averages across CNN and Transformer: compared with DP, **+36.8%** in clean settings and **+169%** in randomized hard settings.
- Compared with the large model RDT: RDT has **1.2B** parameters, while SeedPolicy-Transformer has only **33.36M** and SeedPolicy-CNN has **147.26M**; under Easy, SeedPolicy-CNN at **42.76%** exceeds RDT at **34.50%**, but under Hard, RDT at **13.72%** still outperforms SeedPolicy.
- In terms of task coverage, SeedPolicy outperforms or matches the baseline on **45/50** tasks (Transformer) and **44/50** tasks (CNN).
- The gains are most pronounced on long tasks: when grouped by task length, the absolute improvements over baseline on short/medium/long tasks are Transformer **+2.9/+6.4/+16.0** points and CNN **+13.6/+12.9/+21.9** points, supporting its core claim that “the longer the horizon, the greater the advantage.”

## Link
- [http://arxiv.org/abs/2603.05117v2](http://arxiv.org/abs/2603.05117v2)
