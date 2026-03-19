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
- world-model
- sample-efficiency
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning

## Summary
This paper proposes **EZ-M**, arguing that in online robotic reinforcement learning, priority should be given to scaling the **number of tasks** rather than the sample volume for a single task. The core idea is that under multitask settings, a shared world model can exploit task-invariant physical dynamics across tasks to achieve higher sample efficiency, making it especially suitable for high-dimensional humanoid control.

## Problem
- Existing robot “foundation model” approaches place more emphasis on **large models + large-scale offline data**, but robot learning fundamentally requires **online interaction**; offline data alone is insufficient for continual error correction and adaptation to environmental changes.
- In multitask online reinforcement learning, **model-free** methods are prone to **gradient conflicts / negative transfer** when different tasks require opposite actions in similar states, causing performance to degrade or stagnate as the number of tasks increases.
- Humanoid control is particularly difficult because it is **high-dimensional, contact-rich, and dynamically complex**; if shared physical laws across tasks cannot be efficiently reused, learning costs become very high. This matters because general-purpose robots need to scale reliably across multi-skill scenarios.

## Approach
- Proposes **EfficientZero-Multitask (EZ-M)**: a **multitask model-based reinforcement learning** framework built on EfficientZero that learns a **shared world model** and conditions the policy, value, reward, and dynamics prediction on task embeddings.
- The core mechanism is simple: although different tasks have different objectives, the **laws of physical motion are the same**. Therefore, training the dynamics model on combined data from multiple tasks is equivalent to helping the model better learn “how the world works,” rather than memorizing actions separately for each task.
- Uses **Gumbel search / tree search** to plan actions in latent space, and distills the improved policy obtained from search back into the policy head; it also uses **categorical reward/value modeling** to mitigate inconsistencies in reward scale across tasks.
- Adds two types of consistency constraints to stabilize multitask training: **temporal consistency** keeps the latent states of imagined rollouts close to the true encoded states; **path consistency** constrains value prediction to remain consistent with the recursive relation of “immediate reward + next-state value.”
- On the engineering side, it also uses **separate task replay buffers, balanced task sampling, action masking, and observation padding** to handle differences in observation/action spaces across tasks and reduce task imbalance.

## Results
- On **HumanoidBench**, the authors claim that **EZ-M achieves SoTA**, with **significantly higher sample efficiency** than strong baselines.
- The explicit setup in Figure 1 shows that on **HumanoidBench-Hard**, with **environment interaction limited to 1 million** and **3 random seeds**, EZ-M **matches and surpasses** all strong baselines and “**significantly outperforms all baselines**.”
- The strong conclusion in the abstract and introduction is that as the **number of tasks increases**, EZ-M exhibits **positive transfer**, whereas model-free baselines **degrade or plateau**; this supports the claim that “scaling task count” is a key axis for scalable online robot learning.
- The theory section makes a sample complexity claim: when the number of tasks **K -> ∞**, the **per-task** sample complexity of model-based methods approaches **d_rew**, while that of model-free methods approaches **d_dyn + d_rew**; it further emphasizes that **d_dyn >> d_rew**, indicating that shared dynamics can provide an asymptotic advantage.
- The provided excerpt **does not include more detailed table values** (such as specific average scores, percentage improvements, or per-baseline margins), so a fuller quantitative comparison cannot be listed; however, the strongest verifiable numbers are the **1M interactions** and **3 seeds** setup.

## Link
- [http://arxiv.org/abs/2603.01452v1](http://arxiv.org/abs/2603.01452v1)
