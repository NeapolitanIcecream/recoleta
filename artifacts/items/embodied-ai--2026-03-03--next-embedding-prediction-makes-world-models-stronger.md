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
- world-model
- representation-learning
- temporal-transformer
- partial-observability
relevance_score: 0.82
run_id: materialize-outputs
---

# Next Embedding Prediction Makes World Models Stronger

## Summary
本文提出 NE-Dreamer，一种用于模型式强化学习的无解码器世界模型，通过预测“下一时刻的编码嵌入”而不是重建像素来学习状态表示。核心结论是：这种时间预测式表示学习在部分可观测、需要记忆与导航的任务上明显更强，同时在标准控制基准上不退化。

## Problem
- 现有世界模型在像素输入下常依赖重建图像来学习表示，但重建目标计算重、优化复杂，还会浪费容量去拟合与控制无关的视觉细节。
- 许多无解码器方法只做**同一时刻**的表示对齐，缺少跨时间的显式约束；在部分可观测环境中，这会导致表示不具备预测性，难以支持长时记忆和规划。
- 这很重要，因为在 DMLab 这类记忆/导航任务里，智能体必须从历史中整合信息，而不能只看当前帧做反应。

## Approach
- NE-Dreamer 保留 Dreamer 式 RSSM 世界模型和 imagination-based actor-critic 控制骨架，但移除了像素解码器。
- 它让一个**因果时序 Transformer**根据截至时间 \(t\) 的历史 latent/state/action，去预测下一步编码器嵌入 \(\hat e_{t+1}\)。
- 预测目标是真实下一帧经过编码器得到的嵌入 \(e_{t+1}\)，但对目标使用 stop-gradient；也就是说，模型学的是“从历史预测未来表示”。
- 训练时用 **Barlow Twins** 风格的冗余抑制对齐损失，让预测嵌入与目标嵌入在对应维度上对齐、在非对应维度上去冗余，从而避免塌缩。
- 简单说，方法的核心机制是：**不再要求模型把当前图像重建出来，而是要求它从过去的信息猜对下一步会看到的高层表示**。

## Results
- 在 **DMLab Rooms** 上，作者声称在**相同算力与模型容量**下（**50M environment steps, 5 seeds, 12M parameters**），NE-Dreamer 优于强基线，包括 **DreamerV3、R2-Dreamer、DreamerPro**；但摘录中**未提供具体分数表或逐任务数值**。
- 在机制消融中，移除**因果 Transformer**（w/o transformer）或移除**next-step target shift**（w/o shift）都会使性能“substantially reduces / collapses / nearly complete loss of gains”；这支持性能提升来自“预测式序列建模”，但摘录中**没有给出量化降幅**。
- 在 **DeepMind Control Suite (DMC)** 上，NE-Dreamer 在**1M environment steps、5 seeds、12M parameters**设置下，作者称其**匹配或略优于** DreamerV3 及其他无解码器基线；摘录中同样**没有具体任务均值或 aggregate score 数字**。
- 表征诊断中，作者通过冻结 latent 后训练事后解码器，声称 NE-Dreamer 的 latent 能更稳定保留物体身份、空间布局和任务相关信息，而 Dreamer/R2-Dreamer 更容易出现时序不一致；这是**定性证据**，无定量指标。
- 总体最强的具体主张是：在**50M steps 的 DMLab Rooms** 记忆/导航任务上，NE-Dreamer 在**同参数规模 12M**、**5 个随机种子**下优于现有 decoder-based 与 decoder-free 世界模型；在**1M steps 的 DMC** 上则无性能回退。

## Link
- [http://arxiv.org/abs/2603.02765v1](http://arxiv.org/abs/2603.02765v1)
