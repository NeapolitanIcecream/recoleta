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
- long-horizon
- temporal-attention
- imitation-learning
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# SeedPolicy: Horizon Scaling via Self-Evolving Diffusion Policy for Robot Manipulation

## Summary
SeedPolicy addresses the long-horizon modeling bottleneck in diffusion policies for robot manipulation, where “seeing longer actually makes performance worse.” It does so with a recursively updatable, gated temporal state module, allowing longer observation windows to genuinely translate into higher success rates, while achieving strong results with far fewer parameters than large-scale VLA models.

## Problem
- Existing Diffusion Policy can model multimodal expert behavior, but as the **observation horizon** increases, performance instead declines, limiting long-horizon manipulation capability.
- Directly stacking multiple image frames makes it difficult to capture complex temporal dependencies; in long tasks, key historical information is easily lost, while noisy frames interfere with decision-making.
- Although standard temporal attention can improve modeling, its computation grows quadratically with sequence length, making it unfavorable for real-time robot control and edge deployment.

## Approach
- Proposes **SEGA (Self-Evolving Gated Attention)**: it maintains a fixed-size latent state that evolves over time, compressing long histories into this state and avoiding direct processing of increasingly long raw frame sequences.
- SEGA contains two streams: one uses the current observation to update the historical state; the other uses the historical state to enhance the current observation in reverse, then passes it to the diffusion action expert to predict the action sequence.
- The core gate, **SEG**, directly uses cross-attention scores as a “relevance signal” to determine how much new information to retain and how much old state to preserve; simply put, it “updates memory only when the current frame is truly useful.”
- Integrating SEGA into Diffusion Policy yields **SeedPolicy**, enabling approximately recurrent long-horizon modeling and extending temporal length with moderate overhead.

## Results
- On **50 manipulation tasks** in **RoboTwin 2.0**, the authors report that SeedPolicy reaches SOTA among IL methods; averaged over CNN and Transformer backbones, it improves over the original DP by **36.8%** in **clean** settings and **169%** in **randomized hard** settings (relative improvement).
- In Table 1, under the **Transformer backbone**: DP improves from **33.10%** (Easy) / **1.44%** (Hard) to SeedPolicy’s **40.08%** / **4.28%**, corresponding to absolute gains of **6.98%** and **2.84%**.
- In Table 1, under the **CNN backbone**: DP improves from **28.04%** (Easy) / **0.64%** (Hard) to SeedPolicy’s **42.76%** / **1.54%**, corresponding to absolute gains of **14.72%** and **0.90%**.
- Compared with **RDT (1.2B parameters)**, SeedPolicy is much smaller in parameter count: **33.36M** (Transformer) or **147.26M** (CNN); the Transformer version is about **36×** smaller than RDT, while in the Easy setting the CNN version’s success rate of **42.76%** is higher than RDT’s **34.50%**.
- The authors state that SeedPolicy outperforms or matches the baseline DP on **45/50** tasks (Transformer) and **44/50** tasks (CNN).
- Grouped by task length, SeedPolicy shows larger advantages on longer tasks: for Transformer, it leads by **+2.9% / +6.4% / +16.0%** on short/medium/long tasks respectively; for CNN, it leads by **+13.6% / +12.9% / +21.9%** respectively, supporting its “horizon scaling” claim.

## Link
- [http://arxiv.org/abs/2603.05117v2](http://arxiv.org/abs/2603.05117v2)
