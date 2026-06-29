---
source: arxiv
url: https://arxiv.org/abs/2606.10305v1
published_at: '2026-06-09T01:46:23'
authors:
- Qianzhong Chen
- Hau Zheng
- Justin Yu
- Suning Huang
- Jiankai Sun
- Ken Goldberg
- Chuan Wen
- Pieter Abbeel
- Yide Shentu
- Philipp Wu
- Mac Schwager
topics:
- vision-language-action
- robot-reward-modeling
- long-horizon-manipulation
- self-improving-robots
- robot-data-scaling
- mixture-of-experts
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# SARM2: Multi-Task Stage Aware Reward Modeling for Self Improving Robotic Manipulation

## Summary
## 摘要
SARM2 是一个用于长时程机器人操作的多任务稠密奖励模型，配合 SPIRAL 这一基于策略的 VLA 改进循环，使用自主 rollout。论文声称，它在 10 任务基准上的奖励精度更高，并在折叠短裤和清理白板任务上带来大幅真实机器人成功率提升。

## 问题
- 长时程 VLA 微调仍然依赖昂贵的示范，行为克隆在策略偏离示范分布后很难恢复。
- 稀疏奖励对多阶段机器人任务的信用分配很弱，而大型 VLM 奖励模型又太粗，难以反映逐步进展。
- 现有的阶段感知奖励模型虽然可以很准确，但通常需要任务专属的阶段标签，并且每个任务都要重新训练。

## 方法
- SARM2 根据最近的机器人观测预测当前动作原语，输入包括 3 个摄像头视角、本体感知、冻结的 SigLIP-2 特征，以及一个 4 层因果 Transformer。
- 阶段估计器把每个片段分到 22 个类别：21 个动作原语加 1 个空类别。原语数据来自 100 个真实世界操作任务的 200 小时数据，其中 66 小时平衡数据用于原语训练。
- 另一个 6 层因果 Transformer 价值模型估计距离完成的归一化剩余步数，范围是 [-1, 0]。
- 价值头使用多门控 Mixture-of-Experts 解码器。预测出的原语选择一个门，门再把状态路由到共享的 MLP 专家。
- SPIRAL 以经过 BC 微调的 VLA 为起点，用大约 100 条带标注的 rollout 对奖励模型做一次适配，然后交替进行自主 rollout 收集、SARM2 重新标注，以及残差式 TD3 风格的 RL 更新。

## 结果
- 在 10 任务奖励基准上，SARM2 的总体示范 MSE 最好，为 0.020；对比方法包括 ReWiND 的 0.036、TOPReward 的 0.107、Robometer 的 0.093，以及 LoRA 微调后的 Robometer 的 0.043。
- 在经典子集 S1 上，SARM2 的示范 MSE 为 0.006。在非常规子集 S2 上，示范 MSE 为 0.031。
- 去掉阶段估计器后，总体示范 MSE 从 0.020 升到 0.034。去掉多门控设计后，MSE 升到 0.026。
- 在 rollout 排序上，SARM2 在 Folding Shorts 上的 rho 达到 0.833，在 Cleaning Whiteboard 上达到 0.667，这是更难的白板任务中的最佳分数。
- 结合 SPIRAL 后，Folding Shorts Flat 的成功次数提升到 12/12，Folding Shorts Crumpled 在三轮后达到 8/12。
- 在 Cleaning Whiteboard 上，使用 SARM2 的 SPIRAL 达到 18/20 成功和 97.5% 进度；对比之下，微调后的 Robometer 奖励是 13/20 和 97.5% 进度，而仅用示范的 RL-Dense 是 10/20 和 81.3% 进度。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.10305v1](https://arxiv.org/abs/2606.10305v1)
