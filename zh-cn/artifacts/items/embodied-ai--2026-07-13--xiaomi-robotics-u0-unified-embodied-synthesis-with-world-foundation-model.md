---
source: arxiv
url: https://arxiv.org/abs/2607.11643v1
published_at: '2026-07-13T14:57:58'
authors:
- Xinghang Li
- Jun Guo
- Qiwei Li
- Long Qian
- Hang Lai
- Yueze Wang
- Hongyu Yan
- Jiahang Cao
- Xi Chen
- Jingen Qu
- Jiaxi Song
- Nan Sun
- Hanye Zhao
- Futeng Liu
- Wanli Peng
- Heyun Wang
- Yunhong Wang
- Caoyu Xia
- Jack Zhao
- Diyun Xiang
- Hangjun Ye
- Heng Qu
- Huaping Liu
- Jason Li
topics:
- embodied-foundation-model
- world-model
- robot-data-scaling
- vision-language-action
- sim2real
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# Xiaomi-Robotics-U0: Unified Embodied Synthesis with World Foundation Model

## Summary
## 摘要
Xiaomi-Robotics-U0 是一个拥有 380 亿参数的多模态模型，统一支持图像生成、具身场景合成、场景迁移和机器人视频预测。该模型使用世界基础模型生成一致的机器人观测结果和用于策略训练的合成操作轨迹。

## 问题
- 通用图像和视频模型应用于机器人领域时，容易生成几何结构、视角、机器人状态和交互动态不一致的结果。
- 面向机器人的适配通常使用规模较小且重复度较高的数据集，可能削弱大规模预训练获得的视觉知识和泛化能力。
- 可靠的具身生成很重要，因为机器人策略需要物理上兼容的多视角观测结果，以及用于训练和提升分布外性能的多样化未来轨迹。

## 方法
- 以基于 Qwen-3-32B 仅解码器 Transformer 的 EMU3.5 模型为基础，使用一个多模态下一词元预测目标训练所有任务。
- 将通用文生图和图像编辑数据，与具身场景生成、多视角具身迁移、子任务预测和操作视频生成数据共同训练。
- 使用工作空间、目标物体、无关物体、光照和背景等结构化控制，同时加入深度和机器人动作信号，以保持几何结构和交互状态。
- 在 1、3 和 5 FPS 下使用稀疏及稠密视频序列进行训练，以建模长时程任务进展和细粒度操作动态。
- 加入 FlashAR+ 解码，在反对角线上并行生成图像词元；论文报告称，与串行下一词元解码相比，1024x1024 图像生成速度最高提升 82.9 倍。

## 结果
- 模型使用了 950 万个单步样本，包含 564 亿个词元，以及 260 万个视频片段，包含 496 亿个词元。
- 在具有挑战性的真实世界操作任务中，使用生成数据后，下游 \\(\\pi_{0.5}\\) 策略的分布外成功率从 36.9% 提升到 63.2%。
- 在具身场景生成和具身迁移的人类评测中，模型得分高于 GPT-Image-2.0。
- 在具身视频生成的 World Arena 基准测试中排名第一，并声称在单步和序列具身生成任务上取得了当时最佳结果。
- 摘录没有提供详细的人类评测分数、World Arena 分数、逐任务基线或统计显著性结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.11643v1](https://arxiv.org/abs/2607.11643v1)
