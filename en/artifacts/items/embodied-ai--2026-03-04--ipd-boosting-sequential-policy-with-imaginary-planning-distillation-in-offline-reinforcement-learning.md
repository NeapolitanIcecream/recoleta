---
source: arxiv
url: http://arxiv.org/abs/2603.04289v1
published_at: '2026-03-04T17:05:39'
authors:
- Yihao Qin
- Yuanfei Wang
- Hang Zhou
- Peiran Liu
- Hao Dong
- Yiding Ji
topics:
- offline-rl
- decision-transformer
- world-model
- model-predictive-control
- policy-distillation
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# IPD: Boosting Sequential Policy with Imaginary Planning Distillation in Offline Reinforcement Learning

## Summary
IPD is a framework for offline reinforcement learning that enhances Transformer sequential policies with "imaginary planning." It combines a world model, value function, and MPC planning to first generate better virtual trajectories, then distills this planning knowledge into the policy.

## Problem
- The paper addresses the problem that **Decision Transformer-based sequential policies in offline RL struggle to compose optimal behavior from suboptimal static data**, which limits the upper bound of policy performance.
- Traditional Transformer-style methods are more like conditional imitation, **lacking explicit planning and dynamic programming mechanisms**, and therefore make insufficient use of suboptimal data.
- This matters because offline RL cannot rely on online trial and error; if one can only depend on fixed data, then how to extract a better policy from limited, noisy, suboptimal data directly determines real-world usability and safety.

## Approach
- First, learn a **quasi-optimal value function** and **Q-function** from offline data, using an approach close to IQL to reduce OOD overestimation; at the same time, train a world model with **uncertainty estimation**.
- Use the value function to compare real trajectory returns with "imagined returns" to identify **suboptimal states/trajectory segments**; for these segments, use **MPC** inside the world model to generate better imagined rollouts.
- Use an **ensemble probabilistic world model** to characterize aleatoric + epistemic uncertainty, and use **GJS divergence** to measure model disagreement; retain only low-uncertainty imagined data to avoid accumulated model error.
- Train a Transformer sequential policy on the augmented data, and add a **value-guided objective** to distill preferences obtained from the value function/planning into action prediction.
- At inference time, instead of manually setting return-to-go, use the learned **quasi-optimal value function** as the conditioning signal to improve decision stability and performance.

## Results
- The paper claims that on the **D4RL benchmark**, IPD **significantly outperforms** a variety of SOTA **value-based** and **transformer-based** offline RL methods.
- It provides systematic **ablation studies** validating the roles of three key components: **MPC-driven data augmentation**, **value-guided action imitation**, and **return-to-go prediction/replacement**.
- The paper also claims to analyze the relationship between **imaginary data augmentation volume** and performance, and observes a **scaling law**.
- However, in the excerpt currently provided, **no specific numerical results are given**, so it is not possible to explicitly list quantitative metrics such as task names, scores, improvement margins, or baseline gaps. The strongest concrete claim is: IPD achieves consistent performance gains across multiple D4RL tasks and integrates planning throughout both training and inference.

## Link
- [http://arxiv.org/abs/2603.04289v1](http://arxiv.org/abs/2603.04289v1)
