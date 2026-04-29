---
kind: trend
trend_doc_id: 161
granularity: day
period_start: '2026-04-21T00:00:00'
period_end: '2026-04-22T00:00:00'
topics:
- robotics
- vision-language-action
- world-models
- humanoids
- training-data
run_id: materialize-outputs
aliases:
- recoleta-trend-161
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/humanoids
- topic/training-data
language_code: zh-CN
---

# 机器人论文用训练信号在执行中保留得有多好来评判模型

## Overview
这一天最强的主题只有一个：机器人论文正在收紧预训练、预测和真实执行之间的联系。EmbodiedMidtrain 表明，当上游数据更像机器人经验时，VLA 性能会提高。Mask World Model 和 RoboWM-Bench 从相反两端提出同一个要求：保留与任务相关的结构，然后用可执行行为来判断成败。

## Clusters

### 用于VLA预训练的数据整理
EmbodiedMidtrain把数据选择变成VLA训练中的核心环节。论文测量了通用视觉语言模型数据与机器人轨迹之间的真实错配，然后用与机器人数据更接近的样本进行中期训练。对小型骨干模型，提升幅度很大：InternVL3.5-1B在 SimplerEnv-Bridge 上的成功率从36.5升到56.3，在 Libero-10 上从39.0升到54.2。Qwen3VL-2B 在 Calvin、SimplerEnv-Bridge 和 Libero-10 上也都有提升。这给当天研究一个明确结论：更好的机器人策略来自动作前数据与机器人经验的更好对齐，不只是更大的动作头或更多机器人微调。

#### Evidence
- [EmbodiedMidtrain: Bridging the Gap between Vision-Language Models and Vision-Language-Action Models via Mid-training](../Inbox/2026-04-21--embodiedmidtrain-bridging-the-gap-between-vision-language-models-and-vision-language-action-models-via-mid-training.md): EmbodiedMidtrain 在 Calvin、SimplerEnv-Bridge 和 Libero-10 上的摘要与基准增益。

### 以执行为依据的世界模型
这一时期的世界模型论文更关注可执行的结构，而不是照片级真实的预测。Mask World Model 在未来语义掩码上训练，这样能保留物体布局和接触线索，同时去掉纹理噪声；它在 LIBERO 上报告了 98.3% 的平均成功率，在 RLBench 上报告了 68.3%，领先多个强基线。RoboWM-Bench 从另一面检验同一问题：生成视频看起来可能合理，但转换成动作后仍会失败。即使对强生成器，它的机器人评测结果仍然偏低；分步分析还显示，许多系统可以到达接触阶段，却无法完成整段任务序列。合在一起看，信号很明确：对机器人来说，有用的世界模型要按执行保真度来评判。

#### Evidence
- [Mask World Model: Predicting What Matters for Robust Robot Policy Learning](../Inbox/2026-04-21--mask-world-model-predicting-what-matters-for-robust-robot-policy-learning.md): 基于掩码的世界模型摘要与结果，包括 LIBERO 和 RLBench 的成功率。
- [RoboWM-Bench: A Benchmark for Evaluating World Models in Robotic Manipulation](../Inbox/2026-04-21--robowm-bench-a-benchmark-for-evaluating-world-models-in-robotic-manipulation.md): 摘要与结果显示视觉真实感和可执行操控行为之间存在分歧。

### 跨具身形态与训练阶段的共享训练接口
两篇论文扩大了机器人控制训练的范围。UniT 为人类和人形机器人行为引入了一种共享的离散动作语言，并让策略训练和世界模型训练建立在同一套 token 上。论文使用了 27,419 条人类轨迹、少样本机器人数据和真实人形机器人测试，不过节选没有给出主要优势幅度。VLA Foundry 处理的是另一个瓶颈：它把语言预训练、视觉语言训练和动作训练放进同一个技术栈，支持最多 128 张 GPU 的分布式运行，并发布开放模型。共同主题是迁移基础设施。一条路线尝试在不同身体之间复用人类运动；另一条路线让完整流程的 VLA 实验更容易复现和比较。

#### Evidence
- [UniT: Toward a Unified Physical Language for Human-to-Humanoid Policy Learning and World Modeling](../Inbox/2026-04-21--unit-toward-a-unified-physical-language-for-human-to-humanoid-policy-learning-and-world-modeling.md): 摘要描述了 UniT 的共享 token 化、人类到人形机器人的迁移设定和评测范围。
- [VLA Foundry: A Unified Framework for Training Vision-Language-Action Models](../Inbox/2026-04-21--vla-foundry-a-unified-framework-for-training-vision-language-action-models.md): 摘要描述了统一的 LLM-VLM-VLA 训练栈和公开报告的训练流程。
