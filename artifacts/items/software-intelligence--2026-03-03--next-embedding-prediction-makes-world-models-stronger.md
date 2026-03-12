---
source: arxiv
url: http://arxiv.org/abs/2603.02765v1
published_at: '2026-03-03T04:04:28'
authors:
- George Bredis
- Nikita Balagansky
- Daniil Gavrilov
- Ruslan Rakhimov
topics:
- model-based-rl
- world-models
- representation-learning
- temporal-transformer
- partial-observability
relevance_score: 0.64
run_id: materialize-outputs
---

# Next Embedding Prediction Makes World Models Stronger

## Summary
本文提出 NE-Dreamer：一种不做像素重建的世界模型强化学习方法，直接预测“下一时刻的编码嵌入”，以学习更适合长期记忆和部分可观测环境的状态表示。作者声称它在 DMLab 的记忆/导航任务上明显强于 DreamerV3 和多种 decoder-free 基线，同时在 DMC 上不退化。

## Problem
- 现有基于世界模型的 MBRL 在高维、部分可观测环境中，需要学到能跨时间保持信息的潜状态，否则无法做好长期预测与控制。
- 传统 Dreamer 类方法依赖像素重建，训练负担重，容易把容量浪费在纹理等与决策无关的视觉细节上。
- 许多 decoder-free 方法只做“同一时刻”的表示对齐，缺少显式的时间预测约束，因此在记忆和导航任务中容易出现表示漂移或坍塌。

## Approach
- NE-Dreamer 保留 Dreamer 的 RSSM 世界模型和 imagination-based actor-critic，只把表示学习目标从像素重建替换成“下一嵌入预测”。
- 在时间步 t，模型用**因果时序 Transformer**读取历史 latent/state/action 序列，只利用过去信息预测下一时刻编码器嵌入 \(\hat e_{t+1}\)。
- 预测结果与真实下一时刻嵌入 \(e_{t+1}\) 的 stop-gradient 目标做对齐；具体使用 **Barlow Twins** 冗余约简损失，既鼓励预测一致，也抑制表示坍塌。
- 世界模型总损失由 reward、continuation、KL 正则和 next-embedding loss 组成，不需要像素解码器、数据增强或额外辅助监督。
- 作者通过消融强调，性能关键来自两点：**因果 Transformer 的序列建模** 和 **目标向下一步偏移的预测训练**，而不是 projector 等小技巧。

## Results
- 在 **DMLab Rooms** 上，作者报告在**相同计算预算和模型规模**下（**50M environment steps、5 seeds、12M parameters**），NE-Dreamer 优于强 decoder-based 基线 **DreamerV3** 和 decoder-free 基线 **R2-Dreamer、DreamerPro**；论文未在正文摘录中给出明确分数表，但多处使用“substantial gains”“dramatic improvement”描述四个任务上的明显提升。
- 图 1/图 3 的核心主张是：在 **memory/navigation-heavy** 的 DMLab Rooms 四个任务中，NE-Dreamer 在所有任务上都学得更稳定、最终回报更高；最大收益出现在依赖长期记忆而非短时视觉线索的任务。
- 机制消融在 **DMLab Rooms** 上表明，去掉 **causal temporal transformer** 或去掉 **next-step shift** 会使性能“大幅下降/几乎失去增益”；去掉 projector 主要影响优化速度和稳定性，对最终性能影响较小。该实验同样在 **50M steps、5 seeds、12M params** 下进行。
- 在 **DMC** 上，作者称 NE-Dreamer 在统一协议下（**1M environment steps、5 seeds、12M parameters**）与 DreamerV3、R2-Dreamer、DreamerPro **持平或略优**，说明去掉重建不会伤害标准连续控制表现；但摘录未提供具体平均分数。
- 表示诊断方面，作者训练了一个**事后解码器**，声称 NE-Dreamer 的冻结 latent 能更稳定保留物体身份和空间布局，而 Dreamer/R2-Dreamer 更容易出现任务相关属性跨时间消失；这是定性证据，不是标准 benchmark 数值。

## Link
- [http://arxiv.org/abs/2603.02765v1](http://arxiv.org/abs/2603.02765v1)
