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
- world-model
- latent-planning
- representation-learning
- gradient-based-planning
- self-supervised-learning
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Temporal Straightening for Latent Planning

## Summary
This paper proposes **Temporal Straightening**, which adds trajectory-curvature regularization during world model training so that feasible state evolution in latent space becomes more “straight,” making it better suited for gradient-based planning. The core contribution is to directly connect “good representations” with “good planning geometry,” improving the usefulness of latent goal distances and the stability of planning optimization.

## Problem
- Existing latent world models often rely on pretrained visual features, but these features are not designed for planning and contain information irrelevant or even harmful to control.
- When latent trajectories are highly curved in representation space, Euclidean distance cannot faithfully reflect the “geodesic distance” of reaching the goal along feasible dynamics, causing the goal cost to mislead planning.
- This makes gradient-based action optimization highly non-convex, poorly conditioned, and prone to getting stuck, so many methods are forced to use more computationally expensive search-based planners such as CEM/MPPI.

## Approach
- Jointly train a world model consisting of an observation encoder, an action encoder, and a latent dynamics predictor, using next-step latent-state prediction as the main learning objective.
- For three consecutive latent states $z_t,z_{t+1},z_{t+2}$, compute adjacent “velocity” vectors $v_t=z_{t+1}-z_t$ and $v_{t+1}=z_{t+2}-z_{t+1}$, and minimize $1-\cos(v_t,v_{t+1})$ to penalize local curvature.
- Intuitively, this makes latent trajectories closer to straight lines, bringing latent Euclidean distance closer to the true reachable path distance and making the optimization landscape of terminal error smoother.
- The total training loss is prediction MSE plus the curvature regularizer; to prevent representation collapse, the target branch uses stop-gradient.
- Theoretically, the paper proves under linear dynamics that if transitions are sufficiently “straight,” the effective condition number of the planning Hessian improves and gradient descent converges faster; it also gives the upper bound $\kappa_{\mathrm{eff}}(H)\le \kappa(B)^2((1+\varepsilon)/(1-\varepsilon))^{2(K-1)}$.

## Results
- The paper claims that across a set of goal-reaching tasks, **open-loop gradient planning success rate improves by 20–60%**, and **MPC improves by 20–30%**; these are the key quantitative conclusions given in the abstract.
- Experimental environments include **Wall, PointMaze UMaze, Medium Maze, PushT**, with comparison against **DINO-WM** (based on frozen DINOv2 features).
- The paper shows that after straightening, latent trajectory curvature decreases, the loss landscape in action space becomes closer to convex, and gradient-based planning becomes more stable; however, the provided excerpt does not include full table values.
- In PointMaze visualizations, the latent Euclidean-distance heatmap after straightening more closely matches the true geodesic distance computed by A-star, supporting the key claim that the distance is “more faithful.”
- The authors also observe that prediction alone already provides some “implicit straightening,” but explicit curvature regularization can further reduce curvature and yield better planning performance.
- Based on the provided text, the strongest quantitative evidence is the **20–60% open-loop** and **20–30% MPC** success-rate gains; the rest is mostly visualization and theoretical support, with fewer specific baseline scores.

## Link
- [http://arxiv.org/abs/2603.12231v1](http://arxiv.org/abs/2603.12231v1)
