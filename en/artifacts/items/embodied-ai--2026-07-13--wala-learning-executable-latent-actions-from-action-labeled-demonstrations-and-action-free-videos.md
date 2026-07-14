---
source: arxiv
url: https://arxiv.org/abs/2607.11397v1
published_at: '2026-07-13T11:02:04'
authors:
- Jiahao Liu
- Zhongpu Xia
- Shuai Tian
- Huangrui Li
- Yuhang Zheng
- Ning Ma
- Xin Fu
- Xiaotian Liu
- Jing Li
- Yixian Li
- ShangQing Zhou
- Zebin Xing
- Linbo Wang
- Chaoyue Li
- Haoran Li
- Dongbin Zhao
topics:
- robot-foundation-model
- vision-language-action
- latent-actions
- world-model
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# WALA Learning Executable Latent Actions from Action-Labeled Demonstrations and Action-Free Videos

## Summary
WALA learns latent actions that connect action-free human videos with executable robot control. It uses future semantic and geometric scene changes as training signals, then deploys only the vision-language policy and action head.

## Problem
- Robot policies depend on action-labeled demonstrations, which are costly to collect and provide limited supervision about what happens after an action.
- Human videos contain physical interactions and future scene changes but usually lack robot action labels, so standard behavior cloning cannot use them directly.
- The problem matters because long-horizon and contact-rich manipulation requires policies to predict object motion, contact effects, and spatial changes, not only map observations to motor commands.

## Approach
- WALA pretrains a latent action encoder and decoder on current observations plus multiple sparsely sampled future observations. The encoder converts future changes into latent action targets.
- It predicts changes in frozen DINOv3 feature space for semantic information and dense depth space for geometry, avoiding raw-pixel reconstruction.
- During policy training, a Qwen3-VL-4B vision-language backbone generates latent actions from multi-view images, language, robot state, and action queries.
- Robot demonstrations supervise executable actions, while both robot and action-free videos supervise latent-action matching and future semantic-geometric dynamics prediction.
- At deployment, WALA removes the future observations, latent-action encoder, depth estimator, DINOv3 encoder, and world-model decoder; only the vision-language backbone and action head run.

## Results
- On RoboTwin 2.0, WALA reaches 90.6% success in the Clean setting and 92.8% in the Random setting. Its Random score is higher than LingBot-VA at 91.5% and Fast-WAM at 91.8%.
- On RoboCasa-GR1-Tabletop, WALA achieves 75.2% average success across 24 tasks, beating the strongest listed baseline, DIAL at 70.2%, by 5.0 percentage points.
- In the RoboCasa ablation, the full method scores 75.2%, compared with 54.2% for the base policy, a gain of 21.0 points. Semantic-geometric world supervision alone reaches 71.0%.
- With 10% of labeled demonstrations, WALA reaches 53.9% versus 18.1% for the base policy. With 40%, 70%, and 100% of labeled data, it reaches 66.5%, 71.2%, and 75.2%, respectively.
- The excerpt reports additional real-robot experiments and action-free video scaling studies, but it does not provide their quantitative results.

## Link
- [https://arxiv.org/abs/2607.11397v1](https://arxiv.org/abs/2607.11397v1)
