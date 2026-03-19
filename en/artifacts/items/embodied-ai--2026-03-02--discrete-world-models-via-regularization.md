---
source: arxiv
url: http://arxiv.org/abs/2603.01748v1
published_at: '2026-03-02T11:17:38'
authors:
- Davide Bizzaro
- Luciano Serafini
topics:
- world-model
- discrete-latents
- representation-regularization
- unsupervised-learning
- symbolic-planning
relevance_score: 0.83
run_id: materialize-outputs
language_code: en
---

# Discrete World Models via Regularization

## Summary
DWMR proposes a **reconstruction-free, contrastive-free** method for learning discrete world models, directly compressing images into Boolean bits through regularization while learning action-conditioned transitions. It targets environments with combinatorial/symbolic structure, emphasizing more informative and plannable discrete state representations.

## Problem
- Existing discrete world models typically rely on **pixel reconstruction** to prevent latent collapse, but reconstruction often focuses on visual details rather than action-relevant dynamics.
- Another class of methods relies on **contrastive learning, reward, or value signals**, which increases training complexity and is not well suited to purely unsupervised, goal-agnostic world model learning.
- The authors aim to answer: **can fully unsupervised learning, using only a prediction loss plus regularization tailored to Boolean latents, learn non-collapsed, predictable, approximately symbolic discrete states and transitions?** This matters because Boolean states are better suited to search, planning, exact state matching, and combinatorial generalization.

## Approach
- An **encoder** maps observation images into a Boolean latent variable of length K; an **action-conditioned predictor** uses the current latent variable and action to predict the next latent variable.
- The core training objective is not pixel reconstruction, but **next-latent-state prediction + four types of regularization**: increasing the variance of each bit (avoiding constant bits), reducing correlations between bits, reducing third-order coskewness (suppressing higher-order coupling), and adding an action locality prior (only a small number of bits flip at each step).
- Intuitively, this treats the ideal representation as a binary code that is **mutually independent, close to Bernoulli(0.5), and changed only locally by actions**, thereby avoiding representational degeneration without a decoder.
- Training uses a **two-step update**: first train the predictor using only hard bits so it adapts to the discrete inputs used at test time; then use soft probabilities for joint backpropagation to optimize the full objective for both encoder and predictor.
- The target next state is produced by an **EMA target encoder** to improve training stability for discrete rollouts.

## Results
- The paper claims that on two benchmarks with combinatorial structure, DWMR learns **more accurate representations and transitions** than **reconstruction-based alternatives**: the benchmarks are **MNIST 8-puzzle** and **IceSlider**, tested on both **clean images** and settings with added **Gaussian noise N(0, 0.5)**.
- In terms of data scale, 8-puzzle uses **30,000** training transitions, **6,000** validation, and **6,000** test; IceSlider uses **40,000** training, **10,000** validation, and **10,000** test.
- Representation quality is evaluated with a **linear probe** after freezing the encoder, using **mean per-cell F1-score** as the metric, and reporting both direct encoding (**Enc.**) and one-step imagined rollout (**Im.**) results.
- The paper also explicitly claims that the proposed **two-step training procedure**, compared with the **straight-through estimator** or fully soft-value training, achieves **comparable or better accuracy**.
- In addition, DWMR can be combined with an auxiliary reconstructor as **DWMR+AE / DWMR+β-VAE**, and the authors claim this combination brings **further improvements**.
- However, in the provided excerpt, **the final main-table numerical results are not given** (such as the mean/variance F1 for each method on each dataset, or relative percentage improvements), so it is not possible to state exactly “how many points it outperforms the baselines by.”

## Link
- [http://arxiv.org/abs/2603.01748v1](http://arxiv.org/abs/2603.01748v1)
