---
source: arxiv
url: http://arxiv.org/abs/2603.11395v1
published_at: '2026-03-12T00:15:11'
authors:
- Abdulaziz Alyahya
- Abdallah Al Siyabi
- Markus R. Ernst
- Luke Yang
- Levin Kuhlmann
- Gideon Kowadlo
topics:
- continual-rl
- world-model
- dreamerv3
- replay-buffer
- catastrophic-forgetting
relevance_score: 0.63
run_id: materialize-outputs
language_code: en
---

# ARROW: Augmented Replay for RObust World models

## Summary
ARROW is a model-based method for continual reinforcement learning: it focuses replay on the world model rather than directly on the policy, and uses a more memory-efficient dual-buffer mechanism to reduce catastrophic forgetting. The paper shows that in continual task sequences such as Atari, where tasks share very little structure, ARROW is significantly more robust than DreamerV3 while maintaining similar forward transfer.

## Problem
- Continual reinforcement learning requires agents to **keep learning new tasks without forgetting old ones**, but common methods suffer from catastrophic forgetting.
- Existing effective methods often rely on **large-scale replay buffers** to mitigate forgetting, which creates clear memory and scalability issues.
- The key question is: **can a more memory-efficient and more strategic replay scheme be used to train the world model, so as to balance stability and plasticity in continual learning?**

## Approach
- ARROW is based on **DreamerV3**: it first trains a **World Model** to predict the environment and rewards, and then trains an actor-critic on trajectories “imagined” by the model.
- The core mechanism is a **dual replay buffer**: a short-term FIFO buffer retains recent experience, while a long-term **global distribution matching** buffer preserves more representative historical samples across tasks.
- The long-term buffer uses **reservoir sampling** to maintain coverage of the global distribution, with the goal of preserving task diversity under limited capacity rather than only remembering recent data.
- To store more diverse trajectories with a small buffer, the paper does not store full episodes, but instead slices experience into **spliced rollouts of length 512**; during training, samples are drawn uniformly in parallel from both buffer types.
- Under the same total memory budget, ARROW uses two buffers each containing **2^18 ≈ 262k observations**, for a total capacity of **2^19 = 524,288 observations**, matching the single-buffer budget of DreamerV3 / TES-SAC.

## Results
- **Atari / default task order / one-cycle**: ARROW achieves forgetting of **0.197**, versus **1.217** for DreamerV3, about **more than 6× lower**; at the same time, ARROW’s **WC-ACC = 0.615**, clearly outperforming both baselines (reported in the paper as negative values).
- **Atari / reverse task order / one-cycle**: ARROW’s forgetting further drops to **0.039**, while DreamerV3 reaches **1.348**; ARROW’s **WC-ACC = 0.618**, again the best.
- **Atari / two-cycle**: ARROW’s **Max-F = 0.012**, indicating almost no forgetting even in the worst case; DreamerV3 has **0.735**, and TES-SAC **0.089**. Meanwhile, ARROW’s **WC-ACC = 0.388**, while both baselines remain negative.
- The paper also claims that on Atari-style tasks with **no shared structure**, ARROW **substantially reduces forgetting** while keeping **forward transfer broadly comparable to the baselines**; DreamerV3 has a slight forward-transfer advantage, but at the cost of severe forgetting.
- Evaluation uses **5 random seeds**, and the figures report the **median and interquartile range**.
- Full quantitative results for **CoinRun (shared structure)** are not shown in the provided excerpt, so its numeric results cannot be listed accurately from the supplied text; however, the paper explicitly states that it also examines transfer and retention under shared structure.

## Link
- [http://arxiv.org/abs/2603.11395v1](http://arxiv.org/abs/2603.11395v1)
