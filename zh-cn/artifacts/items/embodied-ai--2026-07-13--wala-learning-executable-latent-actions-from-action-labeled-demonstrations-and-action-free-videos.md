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
language_code: zh-CN
---

# WALA Learning Executable Latent Actions from Action-Labeled Demonstrations and Action-Free Videos

## Summary
## 摘要
WALA 学习连接无动作标注人类视频与可执行机器人控制的潜在动作。它利用未来场景的语义和几何变化作为训练信号，部署时只运行视觉语言策略和动作头。

## 问题
- 机器人策略依赖带动作标注的示范数据，这类数据采集成本高，而且无法充分监督动作之后发生的变化。
- 人类视频包含物理交互和未来场景变化，但通常没有机器人动作标签，因此标准行为克隆无法直接使用这些视频。
- 这个问题与长时程、接触丰富的操作任务有关。此类任务要求策略预测物体运动、接触影响和空间变化，不能只把观测映射为电机指令。

## 方法
- WALA 使用当前观测和多个稀疏采样的未来观测，预训练潜在动作编码器和解码器。编码器将未来变化转换为潜在动作目标。
- 模型在冻结的 DINOv3 特征空间中预测语义变化，并在稠密深度空间中预测几何变化，从而避免原始像素重建。
- 在策略训练期间，Qwen3-VL-4B 视觉语言骨干网络根据多视角图像、语言、机器人状态和动作查询生成潜在动作。
- 机器人示范为可执行动作提供监督；机器人视频和无动作标注视频共同监督潜在动作匹配以及未来语义几何动力学预测。
- 部署时，WALA 移除未来观测、潜在动作编码器、深度估计器、DINOv3 编码器和世界模型解码器；运行时只保留视觉语言骨干网络和动作头。

## 结果
- 在 RoboTwin 2.0 上，WALA 在 Clean 设置下达到 90.6% 的成功率，在 Random 设置下达到 92.8%。Random 得分高于 LingBot-VA 的 91.5% 和 Fast-WAM 的 91.8%。
- 在 RoboCasa-GR1-Tabletop 上，WALA 在 24 项任务中的平均成功率达到 75.2%，比列出的最强基线 DIAL 的 70.2% 高 5.0 个百分点。
- 在 RoboCasa 消融实验中，完整方法得分为 75.2%，基础策略为 54.2%，提升 21.0 个百分点。仅使用语义几何世界监督时，得分达到 71.0%。
- 使用 10% 的带标注示范数据时，WALA 的得分为 53.9%，基础策略为 18.1%。使用 40%、70% 和 100% 的带标注数据时，得分分别为 66.5%、71.2% 和 75.2%。
- 摘要还提到额外的真实机器人实验和无动作标注视频扩展研究，但没有提供这些实验的定量结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.11397v1](https://arxiv.org/abs/2607.11397v1)
