---
source: arxiv
url: http://arxiv.org/abs/2604.16585v1
published_at: '2026-04-17T15:12:15'
authors:
- Noureddine Kermiche
topics:
- world-model
- discrete-latents
- action-conditioned-planning
- self-supervised-learning
- topological-representation
relevance_score: 0.8
run_id: materialize-outputs
language_code: en
---

# The Global Neural World Model: Spatially Grounded Discrete Topologies for Action-Conditioned Planning

## Summary
GNWM is a world model that maps observations into a discrete 2D grid and predicts future grid states conditioned on actions. The paper claims this discrete topology reduces rollout drift and produces interpretable state maps without pixel reconstruction or BYOL-style target networks.

## Problem
- Continuous latent world models can drift during autoregressive rollout: small prediction errors accumulate, latents blur, and long-horizon planning loses physical structure.
- Existing anti-collapse methods for predictive self-supervised learning often depend on extra training machinery such as target networks, stop-gradient paths, contrastive negatives, or covariance penalties.
- For planning, the authors want a state space that is discrete enough to stay stable over time but still trainable end to end with gradient descent.

## Approach
- GNWM encodes each input into a 2D latent grid, then applies a fixed Gaussian spatial convolution. This spreads activation to nearby cells so neighboring states stay close on the grid.
- The smoothed grid is converted into a probability distribution. A predictor takes the current latent state plus action and predicts the next latent state, while the target branch encodes the actual next observation.
- Training uses three losses: a similarity loss to match predicted and target next states, a batch-level uniform-use loss to avoid collapse, and a peaking loss that pushes each state toward sparse near-one-hot activation.
- At inference time, the model can "snap" the predicted distribution to its argmax grid cell before the next recurrent step. The paper presents this as an error-correction step that prevents drift in long rollouts.
- The authors test the method on four toy settings: passive single-ball video, action-conditioned random-walk control, two-ball factorization, and a synthetic grammar sequence task.

## Results
- Passive observation on a **15x15 grid** used **173 of 225 neurons** in a contiguous organized block, which the paper presents as evidence against codebook collapse.
- In **100-step autoregressive rollouts**, a continuous baseline decayed to **standard deviation 0.066**, while GNWM with grid snapping maintained **0.016**. The excerpt does not name the baseline architecture beyond calling it a continuous baseline.
- In the active control random-walk setting with **4 actions** (up, down, left, right), the model allocated **41 active neurons**, matching the empirical visitation distribution according to the authors.
- In the abstract sequence task with **40 unique 32D word embeddings**, the model used **exactly 40 active neurons** and clustered them by grammatical role: noun, verb, adjective, object.
- The paper also claims successful separation of two independently moving balls into two latent channels, but the excerpt gives no numeric score for this experiment.
- Evidence is limited to small synthetic environments and descriptive metrics. The excerpt does not report standard planning benchmarks, robot tasks, real-world data, or comparisons against established world-model baselines on common datasets.

## Link
- [http://arxiv.org/abs/2604.16585v1](http://arxiv.org/abs/2604.16585v1)
