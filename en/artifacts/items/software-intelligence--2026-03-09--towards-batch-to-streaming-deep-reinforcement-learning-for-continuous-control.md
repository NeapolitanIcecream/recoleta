---
source: arxiv
url: http://arxiv.org/abs/2603.08588v1
published_at: '2026-03-09T16:40:06'
authors:
- Riccardo De Monte
- Matteo Cederle
- Gian Antonio Susto
topics:
- reinforcement-learning
- continuous-control
- streaming-rl
- online-learning
- sim2real
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Towards Batch-to-Streaming Deep Reinforcement Learning for Continuous Control

## Summary
This paper proposes two streaming deep reinforcement learning algorithms for continuous control, S2AC and SDAC, to migrate SAC/TD3, which rely on replay buffers and batch updates, to a purely online update setting. The goal is to support continual learning on resource-constrained devices and finetuning from batch to streaming, while maintaining performance close to existing streaming methods.

## Problem
- Existing continuous-control DRL methods such as SAC and TD3 usually rely on replay buffers, mini-batches, and target networks, resulting in high computational overhead that is unsuitable for edge devices or onboard real-time learning.
- Although purely streaming deep RL is better suited for online deployment, existing methods are incompatible with mainstream batch RL pretraining strategies, making them difficult to use in practical finetuning scenarios such as Sim2Real.
- Switching from batch training to streaming finetuning introduces practical issues such as stability, scale shifts, and hyperparameter sensitivity. This matters because real robots often need online adaptation under limited compute budgets.

## Approach
- Proposes **S2AC**: converts SAC into a streaming version by removing the replay buffer, batch updates, and target network, directly updating the soft Q function online using the current sample while retaining maximum-entropy policy optimization.
- Proposes **SDAC**: converts TD3/deterministic actor-critic into a streaming version, using deterministic policy gradients, online Q-learning, and adding Gaussian noise to target actions to smooth value estimation.
- Both methods use the same stabilization design: sparse initialization, LayerNorm, online state normalization, reward scaling, and critic updates with ObGD plus eligibility traces, to mitigate the high noise and large-step instability of single-sample online updates.
- A key mechanism in S2AC is changing the entropy coefficient from fixed \(\alpha\) to \(\alpha/\sigma_r\), which varies with the reward standard deviation, to preserve the relative weighting of “reward vs. entropy” when rewards are dynamically rescaled.
- The paper also discusses how to switch a batch-pretrained policy to streaming finetuning, and claims that these simple modifications made for streaming compatibility can also improve batch SAC/TD3 performance.

## Results
- Experiments are conducted on **MuJoCo Gym** and **DM Control Suite**. In training from scratch, policies are trained for **20M steps**, each experiment uses **10 random seeds**, evaluation is performed every **10,000 steps**, and average return is computed over **10 evaluation episodes**.
- The paper explicitly claims that **S2AC and SDAC achieve performance comparable to the current SOTA streaming baseline Stream AC(\(\lambda\))** across standard continuous-control benchmarks; however, the provided excerpt **does not include specific task-level scores, means/variances, or percentage improvements**.
- Compared with AVG, the authors claim that **S2AC does not require environment-specific tuning of the optimizer/hyperparameters**; meanwhile, **SDAC introduces no environment-specific hyperparameters**, emphasizing the practicality of Q-based streaming algorithms.
- Ablation studies are described as validating two key design choices: the **adaptive entropy coefficient \(\alpha/\sigma_r\)** in S2AC and the **target noise** in SDAC both provide practical benefits for stable training and performance; however, the excerpt **does not provide concrete numerical results**.
- The paper also claims to be **among the first** to systematically study the practical challenges of finetuning from **batch to streaming** and to propose concrete strategies, targeting application scenarios such as **Sim2Real**, **Real2Sim**, and switching under dynamic compute budgets.

## Link
- [http://arxiv.org/abs/2603.08588v1](http://arxiv.org/abs/2603.08588v1)
