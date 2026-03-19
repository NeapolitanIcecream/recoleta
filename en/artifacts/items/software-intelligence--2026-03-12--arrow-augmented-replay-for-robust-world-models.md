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
- world-models
- experience-replay
- dreamerv3
- catastrophic-forgetting
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# ARROW: Augmented Replay for RObust World models

## Summary
ARROW is a model-based approach for continual reinforcement learning that reduces catastrophic forgetting by focusing replay on the world model rather than directly on the policy, using a more memory-efficient dual-buffer replay design. The paper shows that in continual Atari and shared-structure CoinRun variants, it preserves old-task capabilities more reliably than baselines under the same replay memory budget.

## Problem
- Continual reinforcement learning requires agents to learn new tasks while retaining capabilities on old ones, but common methods are prone to **catastrophic forgetting**.
- Existing effective methods mostly rely on large-scale model-free replay buffers, which have high memory costs and poor scalability.
- The key question is whether **more memory-efficient strategic replay** can be used to train the world model while preserving stability, plasticity, and transfer ability.

## Approach
- Build ARROW on top of DreamerV3: first learn a **world model** to predict the environment, then use that model to “imagine” trajectories for training the actor-critic; in other words, experience is first taught to the model, and then the model teaches the policy.
- Use two complementary replay buffers: a **short-term FIFO** buffer that stores the most recent experience to support current-task learning, and a **long-term LTDM** buffer that uses reservoir sampling to preserve the global distribution and diversity across tasks.
- To allow a small buffer to cover more behavior patterns, the authors store full episodes as length-**512** **spliced rollouts** rather than storing entire episodes.
- Each buffer stores **2^18 ≈ 262,000** observations, for a total capacity of **2^19 = 524,288** observations; comparisons with DreamerV3 and TES-SAC are made under the **same memory budget**.
- The method **does not require task IDs**, and on tasks without shared structure it combines fixed entropy regularization with a preset reward scale to improve exploration.

## Results
- **Atari, default task order (one-cycle)**: ARROW has forgetting of **0.197**, while DreamerV3 has **1.217**, reducing forgetting by more than **6×**; at the same time, ARROW’s **WC-ACC = 0.615**, higher than the negative values of both baselines.
- **Atari, reversed task order (one-cycle)**: ARROW’s forgetting further drops to **0.039**, while DreamerV3 has **1.348**; ARROW’s **WC-ACC = 0.618**, indicating greater robustness to changes in task order.
- **Atari, two-cycle training (two-cycle)**: ARROW has **Max-F = 0.012**, indicating **almost no worst-case forgetting** between the first and second exposures; DreamerV3 has **0.735**, and TES-SAC has **0.089**.
- **Atari, two-cycle training (two-cycle)**: ARROW’s **WC-ACC = 0.388**, while both baselines remain negative, indicating that ARROW better recovers and maintains prior knowledge when revisiting tasks.
- The paper also states that on **tasks without shared structure**, ARROW shows **substantially less forgetting** than model-based/model-free baselines with replay buffers of the same size, while maintaining **comparable forward transfer**.
- For **CoinRun tasks with shared structure**, the abstract states that evaluation and analysis of forward/backward transfer were also conducted, but the provided excerpt **does not include specific quantitative figures**.

## Link
- [http://arxiv.org/abs/2603.11395v1](http://arxiv.org/abs/2603.11395v1)
