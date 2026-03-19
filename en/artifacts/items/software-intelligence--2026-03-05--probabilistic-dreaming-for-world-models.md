---
source: arxiv
url: http://arxiv.org/abs/2603.04715v1
published_at: '2026-03-05T01:32:40'
authors:
- Gavin Wong
topics:
- world-models
- model-based-rl
- dreamer
- particle-filter
- latent-planning
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Probabilistic Dreaming for World Models

## Summary
This paper proposes ProbDreamer, which introduces particle-filter-style "dreaming" into the Dreamer world model to preserve multiple possible futures in parallel and reduce the averaging bias of continuous Gaussian latent variables over multimodal futures. The authors show on MPE SimpleTag that this method can improve both performance and stability, but more aggressive beam-search and pruning variants instead fail significantly.

## Problem
- Although Dreamer learns a distribution over latent states, during the imagination phase it typically samples only a **single trajectory**, limiting exploration of multiple possible futures.
- When facing **mutually exclusive multimodal futures**, continuous Gaussian latent variables tend to average distinct possibilities such as "left/right" into a nonexistent intermediate state, leading to hesitation or incorrect decisions.
- This matters because the sample efficiency and robustness of world-model RL depend heavily on the quality of imagined futures; if imagination is wrong, policy learning can be systematically misled.

## Approach
- Replace single latent sampling with a **particle filter**: maintain K latent particles at each time step, forming an empirical distribution over future latent states and thereby preserving multiple mutually exclusive hypotheses simultaneously.
- Perform latent rollout in parallel for each particle, so the agent can "dream" multiple futures in one training pass rather than seeing only a single imagined trajectory.
- Further propose **latent beam search**: each particle branches into N candidate actions at every step, producing K×N branches that are then propagated forward by the world model.
- To control computation, the authors use an approximate "**free energy**" score to prune branches: the score is determined jointly by critic-predicted value and disagreement in the prior ensemble (approximating epistemic uncertainty), favoring trajectories with high return and high information gain.
- In implementation, Dreamer-v3 is used as the backbone, but the discrete latent variables are switched back to continuous Gaussian latent variables to test whether "continuous latents + particle representations" can combine smooth gradients with multimodal expressiveness.

## Results
- On **MPE SimpleTag**, the best lightweight version, **ProbDreamer Lite (K=2, N=1, T=10)**, achieves **-8.79 ± 0.68**, outperforming **BaseDreamer 1: -9.21 ± 0.80** and **BaseDreamer 2: -9.74 ± 0.79**; the paper summarizes this as a **4.5% improvement** over standard Dreamer.
- This best ProbDreamer outperforms the baseline on **4 of 5 random seeds** and delivers **28% lower variance in episode returns**, indicating a more robust policy.
- The more complex full version was not successful: **ProbDreamer Full 1 (K=2, N=4, T=10)** reaches only **-53.78 ± 12.14**, and **ProbDreamer Full 2 (K=8, N=1, T=22)** reaches **-26.84 ± 23.03**, both far worse than the baseline.
- Based on this, the authors claim that **particle-based latent-state representation itself is effective**, but **high particle counts, latent beam search, and free-energy pruning** cause severe degradation in the current implementation.
- The paper also gives specific hypotheses for the failures: increasing K from 1 to 2 is beneficial, but increasing it further may "fit noise"; value-based pruning amplifies optimistic hallucinations when there is no correction from real observations; ensemble uncertainty collapses, and removing the curiosity term makes almost no difference.

## Link
- [http://arxiv.org/abs/2603.04715v1](http://arxiv.org/abs/2603.04715v1)
