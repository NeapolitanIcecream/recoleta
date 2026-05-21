---
source: arxiv
url: https://arxiv.org/abs/2604.24622v2
published_at: '2026-04-27T15:51:40'
authors:
- Fan Du
- Feng Yan
- Jianxiong Wu
- Xinrun Xu
- Weiye Zhang
- Weinong Wang
- Yu Guo
- Bin Qian
- Zhihai He
- Fei Wang
- Heng Yang
topics:
- vision-language-action
- robot-foundation-model
- flow-matching
- efficient-inference
- robot-manipulation
- coarse-to-fine-generation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# CF-VLA: Efficient Coarse-to-Fine Action Generation for Vision-Language-Action Policies

## Summary
CF-VLA makes flow-based VLA action sampling faster by replacing long iterative generation from Gaussian noise with a two-step coarse initialization and fine correction. It targets real-time robot manipulation where each extra action-generation step adds latency.

## Problem
- Flow-based VLA policies such as $\pi_{0.5}$ can model continuous, multimodal robot actions, but they need many inference steps to turn Gaussian noise into valid actions.
- Low-step sampling hurts action quality because one short trajectory must both find the action manifold and correct local errors.
- This matters for closed-loop robot control, where action latency can reduce success on contact-rich, long-horizon, or bimanual tasks.

## Approach
- CF-VLA splits action generation into two stages with NFE=2: a coarse stage builds an action-prior-guided starting point, and a fine stage applies one local correction.
- The coarse stage samples Gaussian noise $\epsilon_1$, predicts a conditional posterior over endpoint velocity $q_\theta(u \mid o, \epsilon_1)$, and forms $\tilde{\epsilon}=\epsilon_1-\hat{u}$.
- The coarse posterior is trained with a KL loss against a target Gaussian centered on the endpoint velocity $u_{t_1}=\epsilon_1-a$ with variance $\sigma_{noise}^2I$.
- The fine stage predicts the residual update from $\tilde{\epsilon}$ to the ground-truth action using an MSE loss at a fixed refinement time $t_f$.
- Training uses two phases: a warm-up phase with endpoint and proxy-refinement losses, then joint training with $\mathcal{L}_{fine}+\lambda\mathcal{L}_{coarse}$.

## Results
- On LIBERO with NFE=2, CF-VLA reports 96.5 average success, compared with 93.6 for reproduced MIP on the $\pi_{0.5}$ architecture, 92.7 for MIP on the $\pi_0$ architecture, and 94.8 for reproduced $\pi_{0.5}$ at NFE=2.
- LIBERO suite scores for CF-VLA are 98.0 Spatial, 99.2 Object, 96.6 Goal, and 92.0 Long.
- Against $\pi_{0.5}$ at NFE=10 on LIBERO, CF-VLA has a lower average score, 96.5 vs 96.9, but exceeds it on Object, 99.2 vs 98.2, while using 2 function evaluations instead of 10.
- The paper claims a 75.4% reduction in action sampling latency.
- In real-robot experiments, CF-VLA reports 83.0 average success, beating MIP by 19.5 percentage points and $\pi_{0.5}$ by 4.0 points.
- The excerpt states that CF-VLA matches or surpasses the NFE=10 $\pi_{0.5}$ baseline on several CALVIN and LIBERO metrics, but the provided CALVIN table is truncated, so exact CALVIN numbers are unavailable here.

## Link
- [https://arxiv.org/abs/2604.24622v2](https://arxiv.org/abs/2604.24622v2)
