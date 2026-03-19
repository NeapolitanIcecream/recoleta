---
source: arxiv
url: http://arxiv.org/abs/2603.01452v1
published_at: '2026-03-02T05:07:43'
authors:
- Shaohuai Liu
- Weirui Ye
- Yilun Du
- Le Xie
topics:
- model-based-rl
- multi-task-learning
- humanoid-control
- sample-efficiency
- world-models
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning

## Summary
This paper proposes EZ-M, a model-based reinforcement learning method for humanoid control in multi-task online learning, with the core claim that one should scale the **number of tasks** rather than the number of samples for a single task. The authors argue that shared physical dynamics allow multi-task data to jointly train a world model, thereby achieving higher sample efficiency and stronger performance on HumanoidBench.

## Problem
- Existing robot “foundation model” approaches rely more heavily on large parameter counts and offline data, but robots must learn through **online interaction**; offline data alone is insufficient for correcting errors, adapting to changes, and continuously improving.
- In multi-task online reinforcement learning, model-free methods often suffer from **gradient conflict / negative transfer** because different tasks may require opposite actions in similar states, causing performance to degrade or plateau as the number of tasks increases.
- Humanoid control is especially difficult because learning high-dimensional whole-body, contact-rich dynamics is itself the main bottleneck; without efficient sharing of dynamics knowledge, the sample cost becomes very high.

## Approach
- Proposes **EfficientZero-Multitask (EZ-M)**: an extension of EfficientZero-v2 to multi-task online MBRL, using a **shared world model** to learn task-agnostic physical dynamics and then performing task control through task conditioning.
- The intuitive mechanism is that although task rewards and optimal actions differ, the **laws of physics remain unchanged**; therefore, multi-task data can be used together to train the dynamics model, and task diversity instead becomes a form of “dynamics regularization.”
- Specific design choices include learnable task embeddings, action encoding to unify different action spaces, observation padding, action masking, a separate replay buffer for each task, and balanced task sampling.
- During training, Gumbel tree search is used to generate improved policy targets, and the policy is learned in a supervised manner; reward/value use **categorical prediction** to mitigate scale differences across tasks.
- To stabilize multi-step imagination and value learning, two types of consistency constraints are added: **temporal consistency** (predicted latent states aligned with true encoded latent states) and **path consistency** (constraining value ≈ reward + γ·next value).

## Results
- On **HumanoidBench**, the authors claim that EZ-M achieves **state-of-the-art** performance, with significantly higher sample efficiency **without extreme parameter scaling**.
- The explicit conclusion from Figure 1 is that on **HumanoidBench-Hard**, when environment interaction is limited to **1 million**, EZ-M can still **match and surpass strong baselines**; all results are based on **3 random seeds**.
- Both the abstract and introduction claim that as the number of tasks increases, EZ-M exhibits **positive transfer**, while model-free baselines **degrade or plateau**; this supports the idea that “scaling the number of tasks” is a more scalable axis for online robot learning.
- The theoretical section gives an asymptotic conclusion: when the number of tasks **K → ∞**, the per-task sample complexity of model-based methods approaches **d_rew**, while model-free methods approach **d_dyn + d_rew**; the authors assume **d_dyn ≫ d_rew** and use this to argue that multi-task MBRL has a structural sample-efficiency advantage.
- The provided excerpt **lacks more complete quantitative tables / specific percentage improvements in scores**, so it is not possible to accurately list detailed numerical gaps across datasets, metrics, and baselines.

## Link
- [http://arxiv.org/abs/2603.01452v1](http://arxiv.org/abs/2603.01452v1)
