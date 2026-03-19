---
source: arxiv
url: http://arxiv.org/abs/2603.12231v1
published_at: '2026-03-12T17:49:47'
authors:
- Ying Wang
- Oumayma Bounou
- Gaoyue Zhou
- Randall Balestriero
- Tim G. J. Rudner
- Yann LeCun
- Mengye Ren
topics:
- world-models
- latent-planning
- representation-learning
- trajectory-regularization
- gradient-based-planning
relevance_score: 0.31
run_id: materialize-outputs
language_code: en
---

# Temporal Straightening for Latent Planning

## Summary
This paper proposes a representation learning regularization method for latent planning called “temporal straightening,” which improves distance metrics in world models and the stability of gradient-based planning by making latent trajectories more temporally “straight.” The core idea is to jointly train an encoder and a dynamics predictor while penalizing curvature in the directions of adjacent latent velocities.

## Problem
- Although latent world models can compress high-dimensional observations and support planning, their latent spaces are often **highly curved**, making the planning objective non-convex and gradient optimization difficult.
- Pretrained visual features (such as DINOv2) are semantically strong, but **they are not designed for planning**, and may retain information that is irrelevant or even harmful to control.
- When latent trajectories are curved, **Euclidean distance cannot faithfully reflect the geodesic distance along reachable paths**, thereby misleading goal-reaching planning.

## Approach
- Construct a jointly learned world model: a perception encoder maps observations to latent, an action encoder embeds actions, and a predictor uses past latent states and actions to predict the next latent state.
- In addition to the standard prediction loss, introduce a **curvature regularization term**: take three consecutive latent frames, compute two velocity vectors $v_t=z_{t+1}-z_t$ and $v_{t+1}=z_{t+2}-z_{t+1}$, and minimize $1-\cos(v_t,v_{t+1})$.
- Intuitively, this is equivalent to encouraging trajectories to bend less locally, making the “straight-line distance” in latent more closely match the true feasible trajectory distance, and thereby making the planning objective easier to optimize.
- During training, the total loss is the prediction error plus a weighted curvature loss, and stop-gradient is used to prevent representation collapse.
- The paper also provides a linear dynamics analysis: if the transition is close to “straight” ($\|A-I\|_2\le \epsilon$), then the planning Hessian has a better condition number, implying faster and more stable convergence for gradient descent.

## Results
- The paper claims that on a suite of goal-reaching tasks, **open-loop gradient planning success rates improve by 20%–60%**, with significant gains relative to non-straightened representations.
- Under the **MPC** setting, success rates also improve by **20%–30%**.
- Theoretically, under linear dynamics, if the transition is $\varepsilon$-straight, then the effective condition number of the planning Hessian satisfies: $\kappa_{\mathrm{eff}}(H)\le \kappa(B)^2\left(\frac{1+\varepsilon}{1-\varepsilon}\right)^{2(K-1)}$; when $\varepsilon\le 1/2$, it further holds that $\kappa_{\mathrm{eff}}(H)\le \kappa(B)^2 e^{6\varepsilon K}$.
- The experiments cover **Wall, PointMaze UMaze, Medium Maze, PushT**, with **DINO-WM / frozen DINOv2 features** as the main comparison baselines.
- Qualitative results in the paper show that after straightening, the latent trajectory is smoother, the loss landscape in action space is closer to convex, and latent Euclidean distance is more consistent with A-star geodesic distance.
- The abstract and body excerpt do not provide a complete itemized table of values for each dataset, but the clearest quantitative claims are the above **20–60% (open-loop)** and **20–30% (MPC)** success rate improvements.

## Link
- [http://arxiv.org/abs/2603.12231v1](http://arxiv.org/abs/2603.12231v1)
