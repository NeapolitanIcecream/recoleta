---
source: arxiv
url: http://arxiv.org/abs/2604.19734v1
published_at: '2026-04-21T17:57:27'
authors:
- Boyu Chen
- Yi Chen
- Lu Qiu
- Jerry Bai
- Yuying Ge
- Yixiao Ge
topics:
- humanoid-policy-learning
- vision-language-action
- world-model
- cross-embodiment-transfer
- latent-action-tokenization
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# UniT: Toward a Unified Physical Language for Human-to-Humanoid Policy Learning and World Modeling

## Summary
## 摘要
UniT 为人类与人形机器人行为学习一种共享的离散动作语言，并用视觉结果来对齐不同的身体。论文将这个分词器同时用于策略学习和世界模型，让人类数据能够提升人形机器人的控制能力。

## 问题
- 人形机器人基础模型需要大量机器人数据集，但高质量的人形机器人数据稀缺且采集成本高。
- 人类第一视角运动数据很多，但人类和人形机器人的动作空间并不匹配，因为它们的关节、控制模式和自由度不同。
- 现有方法都有明显局限：动作重定向依赖人工且难以扩展；仅基于动作的潜空间会保留特定身体的运动学特征；仅基于视觉的潜空间会把物理意图和外观噪声混在一起。

## 方法
- UniT 从同一个状态转移中构建三个编码器：处理前后帧的视觉分支、处理状态加动作片段的动作分支，以及结合两者的融合分支。
- 这三个分支共享一个残差量化码本，把各自特征转换成相同的离散 token。
- 每个 token 都必须同时重建未来的视觉特征和特定身体的动作。简单说，动作必须解释场景中发生了什么变化，而视觉变化也必须解释发生了什么动作。
- 交叉重建是核心机制：它会把具有相似可见效果的人类和人形机器人行为推向相同的潜在 token，同时滤除身体特定的噪声和无关的图像细节。
- 论文随后在两个系统中使用这些 token：VLA-UniT 预测 UniT token 并将其解码为人形机器人动作；WM-UniT 则把 UniT 动作特征作为共享控制信号，用于动作条件视频预测。

## 结果
- 策略学习在 RoboCasa GR1 的 24 个桌面任务上测试，每个任务评估 50 个 episode，并在全数据（24,000 条机器人轨迹）和小样本（2,400 条机器人轨迹）两种设置下进行。
- 人类到人形机器人的迁移使用 27,419 条 EgoDex basic_pick_place 人类轨迹，与小样本机器人数据混合后，再用机器人数据微调。
- 真实世界策略测试使用 IRON-R01-1.11 人形机器人，动作空间为 50 维，并且 Pick & Place 和 Pouring 每个任务只使用 120 条机器人轨迹。
- 世界模型评估使用来自 RoboCasa 和 DROID 数据集的跨身体数据；DROID 包含来自 564 个场景的 95,599 条轨迹。
- 摘要声称，该方法在数据效率上达到最先进水平，在分布外泛化上更强，在人形机器人策略学习中实现零样本任务迁移，并提升了人形机器人视频生成的可控性。
- 但摘录没有给出具体的定量结果、相对基线的差距或确切的成功率提升，因此仅凭提供的文本无法核实这些结论的强度。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.19734v1](http://arxiv.org/abs/2604.19734v1)
