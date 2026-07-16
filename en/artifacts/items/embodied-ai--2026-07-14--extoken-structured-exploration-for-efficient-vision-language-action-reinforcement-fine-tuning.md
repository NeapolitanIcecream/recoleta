---
source: arxiv
url: https://arxiv.org/abs/2607.12931v1
published_at: '2026-07-14T16:04:41'
authors:
- Yilun Kong
- Yunpeng Qing
- Guozheng Ma
- Haoyu Wang
- Li Shen
- Zhi Hou
- Dacheng Tao
topics:
- vision-language-action
- robot-reinforcement-learning
- structured-exploration
- robot-data-scaling
- sample-efficiency
- dexterous-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# ExToken: Structured Exploration for Efficient Vision-Language-Action Reinforcement Fine-tuning

## Summary
ExToken improves the sample efficiency of vision-language-action reinforcement fine-tuning by conditioning rollouts on diverse behavioral tokens learned from offline demonstrations. It reports higher success rates and faster convergence than standard VLA-RL under constrained simulated and real-world interaction budgets.

## Problem
- VLA reinforcement learning often wastes costly environment interactions because stochastic exploration collapses into repetitive action modes and similar trajectories.
- This matters because physical rollouts require time, hardware access, human intervention, and safety resources; collecting more redundant trajectories does not reliably improve learning.

## Approach
- ExToken embeds each demonstration trajectory with a pretrained video encoder and applies K-means clustering; each cluster centroid becomes a discrete token representing a behavioral mode.
- The VLA policy receives a token during supervised warm-up and RL rollout collection, with different sampled tokens steering it toward different action patterns and broader state-action coverage.
- A SigLIP-based state-conditioned Token Selector predicts the appropriate token from the initial image and language instruction. It is trained with supervised cluster labels and jointly optimized with the policy using REINFORCE.
- During deployment, the selector chooses the most likely token deterministically, resolving the mismatch between randomized training exploration and inference.

## Results
- On four LIBERO suites with 512 rollouts per optimization step for 100 RL steps, ExToken reaches 98.2% average success, versus 96.8% for the matched RLinf-GRPO baseline; on LIBERO-Long it reaches 97.8% versus 95.2%.
- In a controlled exploration study, retaining 512 diversified trajectories matches the performance of 1,024 standard rollouts and outperforms standard training with 512 rollouts, supporting trajectory diversity as the key sample-efficiency factor.
- In real-world tasks evaluated with only 20 rollouts per task per iteration, ExToken improves the average original-setting score over Evo-RL by 6.25% across Fold clothes, Wipe table with towel, Pour water, and Insert pen into pen holder.
- Under object, background, and lighting changes, ExToken typically loses 5–10 percentage points, while the reported baselines often lose 10–25 points.
- With 256 rollouts per optimization step, ExToken achieves 93.4% success, compared with 90.3% for RLinf-GRPO at the same reduced budget and performance comparable to RLinf-GRPO using 512 rollouts; ExToken becomes less stable at 128 rollouts.
- The paper reports stable performance for token counts K=3 and K=6, with a slight decline at K=10; the excerpt provides no single quantitative metric for the increase in trajectory-space coverage.

## Link
- [https://arxiv.org/abs/2607.12931v1](https://arxiv.org/abs/2607.12931v1)
