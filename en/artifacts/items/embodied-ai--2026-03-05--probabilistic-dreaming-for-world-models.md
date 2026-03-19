---
source: arxiv
url: http://arxiv.org/abs/2603.04715v1
published_at: '2026-03-05T01:32:40'
authors:
- Gavin Wong
topics:
- world-model
- model-based-rl
- dreamer
- particle-filter
- uncertainty-estimation
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# Probabilistic Dreaming for World Models

## Summary
This paper proposes ProbDreamer, which introduces particle-filter-style probabilistic “dreaming” into the Dreamer world model so it can preserve multiple possible futures at once instead of imagining only a single trajectory. In a simple RL setting with multimodal future prediction, it brings modest but stable improvements in performance and robustness, while also exposing clear limitations in active pruning and uncertainty estimation.

## Problem
- Existing Dreamer models do learn a latent-state distribution, but during imagination they typically sample only a **single latent state** and roll out a **single imagined trajectory**, missing the diversity of mutually exclusive futures.
- Continuous Gaussian latents have desirable gradient properties, but when facing **multimodal futures** such as “go left / go right,” a unimodal Gaussian may average them into a nonexistent “intermediate state,” leading to indecision or errors.
- This matters because the sample efficiency and robustness of world-model RL depend heavily on whether the agent can correctly represent uncertain, multimodal futures during imagination and learn a policy from them.

## Approach
- The baseline is built on Dreamer-v3, but the discrete categorical latents are changed back to **continuous Gaussian latents** to test whether the smooth optimization advantages of continuous latents can be combined with the multi-hypothesis representation power of probabilistic methods.
- A **particle filter** replaces single-sample imagination: at each time step, K latent particles are retained and propagated in parallel, forming an empirical approximation of the future latent distribution and thereby maintaining multiple mutually exclusive hypotheses simultaneously.
- **Latent beam search** lets each particle branch over N candidate actions, producing K×N imagined branches and expanding action-exploration coverage during imagination.
- **Free-energy-style pruning** is used to control computation: branches are scored using critic-predicted value and epistemic uncertainty approximated by prior-ensemble disagreement, retaining trajectories with high value / high information gain. The objective is written as \(F_t^k = V_\phi(h_t^k,z_t^k) + \beta \sigma_{ens}^2\).
- Evaluation is conducted on MPE SimpleTag; during training, each round collects \(10^3\) real environment steps, followed by \(2\times10^4\) steps of latent imagination; 150 rounds of Bayesian Optimization are used to search hyperparameters, from which 6 finalists are selected and compared across 5 random seeds and 100 fixed test episodes.

## Results
- On **MPE SimpleTag**, the best model is **ProbDreamer Lite 1** (\(K=2, N=1, T=10\)) with a score of **-8.79 ± 0.68**; this outperforms **BaseDreamer 1** at **-9.21 ± 0.80** and **BaseDreamer 2** at **-9.74 ± 0.79** (the paper notes that **0 is perfect performance**).
- The paper explicitly claims that, relative to standard Dreamer, **ProbDreamer Lite improves score by 4.5% on average** and yields **28% lower episode return variance**, indicating a more robust policy.
- At the seed level, the authors state that the Lite version outperforms BaseDreamer on **4 of 5 seeds**, and in qualitative analysis it shows faster switching in predator strategy from “CHASE” to “INTERCEPT,” whereas the baseline is more prone to brief hesitation.
- The more complex **Full ProbDreamer** did not succeed: for example, **ProbDreamer Full 1** (\(K=2,N=4,T=10\)) achieves only **-53.78 ± 12.14**, and **ProbDreamer Full 2** (\(K=8,N=1,T=22\)) reaches **-26.84 ± 23.03**, both significantly worse than the baseline, indicating that beam search + pruning severely degrades performance in this implementation.
- The results also show that more particles are not always better: moving from **\(K=1\)** to **\(K=2\)** helps, but higher **\(K\)** may lead to “particle saturation.” The authors speculate this is related to the task having mainly only **2 predator strategy modes**.
- Regarding uncertainty modeling, the paper does not provide separate quantitative ablation numbers, but it explicitly reports that ensemble disagreement collapses quickly and that removing the curiosity term makes little difference, indicating that the current free-energy pruning and epistemic uncertainty estimation do not deliver the expected benefits.

## Link
- [http://arxiv.org/abs/2603.04715v1](http://arxiv.org/abs/2603.04715v1)
