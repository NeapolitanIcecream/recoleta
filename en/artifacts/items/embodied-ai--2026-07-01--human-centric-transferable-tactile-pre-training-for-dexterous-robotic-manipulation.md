---
source: arxiv
url: https://arxiv.org/abs/2607.01067v1
published_at: '2026-07-01T15:26:26'
authors:
- Chi Zhang
- Penglin Cai
- Ziheng Xi
- Haoqi Yuan
- Hao Luo
- Wanpeng Zhang
- Sipeng Zheng
- Chaoyi Xu
- Zongqing Lu
topics:
- vision-language-action
- dexterous-manipulation
- tactile-pretraining
- human-to-robot-transfer
- robot-data-scaling
- cross-embodiment
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Human-Centric Transferable Tactile Pre-Training for Dexterous Robotic Manipulation

## Summary
TTP pre-trains a vision-language-action robot policy on large human tactile-action data, then adapts it to dexterous robot manipulation. The main concrete contribution in the excerpt is H-Tac, a 160-hour dataset with tactile, action, vision, and language signals.

## Problem
- Contact-rich manipulation needs tactile feedback because vision can miss force, slip, occlusion, and small contact changes.
- Robot tactile datasets are small because tactile hardware differs across hands and teleoperation for dexterous contact tasks is costly.
- Existing tactile VLA work often adds touch during post-training, which limits how much contact dynamics the model can learn before robot task training.

## Approach
- The authors collect H-Tac: 160 hours of egocentric human and robot-related tactile-action data covering 300+ tasks and 135k+ episodes.
- TTP uses BeingH-0.5 as the base VLA model and adds a tactile expert that predicts future tactile readings alongside an action expert that predicts future action chunks.
- Human and robot data share a 200-dimensional action space and a 351-taxel UniTacHand tactile space, so pre-training and post-training use the same target formats.
- Training uses flow matching for both actions and tactile futures, with losses for action prediction and tactile prediction.
- A manifold-preserving gate compares observation features against action and tactile anchors using sliced Wasserstein distance, then reduces context updates when the features look unreliable.

## Results
- H-Tac totals 160 hours, 300+ tasks, and 135k+ episodes.
- HOI-Tac contributes about 11.5M frames, about 106 hours, and 124.8K sequences from public hand-object, hand-face, and hand-scene datasets.
- DeskTask-Tac contributes 37.2 hours at 30 Hz, 947 episodes, and about 4M frames from real desktop bimanual tasks.
- InternData-Tac contributes 17.8 hours at 30 Hz, 9,563 episodes, and about 1.9M frames across Genie1, Lift2, and Split ALOHA robot configurations.
- The excerpt claims better performance in simulation and real-robot tactile tasks, plus cross-embodiment transfer, but it gives no downstream success rates, metric tables, or named baseline numbers.

## Link
- [https://arxiv.org/abs/2607.01067v1](https://arxiv.org/abs/2607.01067v1)
