---
source: arxiv
url: http://arxiv.org/abs/2604.07426v1
published_at: '2026-04-08T17:14:21'
authors:
- Prakul Sunil Hiremath
topics:
- model-based-rl
- world-models
- imagination-rollouts
- dexterous-manipulation
- visual-grounding
relevance_score: 0.73
run_id: materialize-outputs
language_code: en
---

# GIRL: Generative Imagination Reinforcement Learning via Information-Theoretic Hallucination Control

## Summary
GIRL is a model-based reinforcement learning method that tries to keep imagined rollouts close to real dynamics over long horizons. It adds an external grounding signal and an adaptive KL trust region, then reports better sample efficiency and lower rollout drift than DreamerV3 and TD-MPC2 on control and manipulation benchmarks.

## Problem
- Latent world-model RL methods such as DreamerV3 train policies inside imagined rollouts, but small model errors grow over time and push imagined states away from the data seen in the real environment.
- This drift matters most on long-horizon, sparse-reward, contact-rich, and visually distracting tasks, where bad imagined states lead to bad value estimates and weak real-world policies.
- Standard KL regularization is usually set by a fixed schedule, so it does not react to when the model is uncertain or when imagined rollouts stop matching real experience.

## Approach
- GIRL adds a grounding vector from a frozen DINOv2 encoder to the latent transition prior. In simple terms, the world model gets a second opinion from a pretrained visual model about what the current observation means.
- A gated residual injects that grounding into the transition prior, and a small projector is trained so imagined latents must stay semantically consistent with the grounding signal through an L2 cross-modal consistency loss.
- GIRL replaces a fixed KL weight with an adaptive trust-region bottleneck. It updates the allowed drift size and the KL multiplier using Expected Information Gain and a Relative Performance Loss signal from real transitions.
- For proprioceptive tasks with no images, ProprioGIRL swaps DINOv2 for a masked state autoencoder over recent joint-state history, giving the same kind of anchor from proprioceptive inputs.
- The paper also gives a value-gap analysis linking the I-ELBO objective to regret through the Performance Difference Lemma and Integral Probability Metrics.

## Results
- On 8 DeepMind Control tasks at 3e6 environment steps, GIRL reports IQM **0.81** with 95% CI **[0.77, 0.84]**, versus DreamerV3 **0.67 [0.63, 0.71]** and TD-MPC2 **0.71 [0.67, 0.75]**.
- On the same DMC suite, GIRL reports DFM(1000) **2.14** versus DreamerV3 **4.81** and TD-MPC2 **3.47**. The paper states latent rollout drift drops by **38–61%** on clean tasks and **49–68%** on distractor tasks relative to DreamerV3.
- GIRL over DreamerV3 on DMC has Probability of Improvement **0.74 [0.70, 0.78]**. On distractor tasks, the IQM gap against DreamerV3 grows from **0.10** on clean tasks to **0.22**.
- On 3 Adroit tasks at 3e6 steps, ProprioGIRL reports IQM **0.63 [0.58, 0.68]**, versus DreamerV3 **0.44 [0.39, 0.49]** and TD-MPC2 **0.58 [0.53, 0.63]**. DFM(500) is **2.28** versus **3.92** for DreamerV3 and **2.81** for TD-MPC2.
- The paper states higher asymptotic return with **40–55% fewer environment steps** on tasks with horizon **>= 500**.
- For compute cost, a distilled-prior variant cuts DINOv2 overhead from **22%** of wall-clock time to **under 4%**, making it closer to vanilla DreamerV3 in runtime.

## Link
- [http://arxiv.org/abs/2604.07426v1](http://arxiv.org/abs/2604.07426v1)
