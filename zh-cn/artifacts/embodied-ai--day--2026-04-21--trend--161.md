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

# 机器人论文按训练信号在执行中的保真度来评判模型

## 概览
这一天最强的结论很明确：机器人论文正在把预训练、预测和真实执行之间的联系收紧。EmbodiedMidtrain 表明，当上游数据更像机器人经验时，VLA 性能会提高。Mask World Model 和 RoboWM-Bench 从两个方向对 world model 提出同样要求：保留与任务相关的结构，然后按可执行行为来判断成功。

## 研究发现

### VLA 预训练的数据整理
EmbodiedMidtrain 把数据选择放到 VLA 训练的核心位置。论文先测量通用视觉语言模型数据和机器人轨迹之间的真实不匹配，然后在更接近机器人数据的样本上进行 mid-training。对小型骨干模型，提升很大：InternVL3.5-1B 在 SimplerEnv-Bridge 上的成功率从 36.5 提高到 56.3，在 Libero-10 上从 39.0 提高到 54.2。Qwen3VL-2B 也在 Calvin、SimplerEnv-Bridge 和 Libero-10 上都有提升。这个日子的结论很直接：更好的机器人策略来自更好的动作前数据对齐，而不只是更大的 action head 或更多机器人微调。

#### 资料来源
- [EmbodiedMidtrain: Bridging the Gap between Vision-Language Models and Vision-Language-Action Models via Mid-training](../Inbox/2026-04-21--embodiedmidtrain-bridging-the-gap-between-vision-language-models-and-vision-language-action-models-via-mid-training.md): Summary and benchmark gains for EmbodiedMidtrain across Calvin, SimplerEnv-Bridge, and Libero-10.

### 以执行为准的 world model
这一时期的 world model 论文更看重可执行结构，而不是逼真的图像预测。Mask World Model 训练未来语义 mask，这样能保留物体布局和接触线索，同时去掉纹理噪声；它在 LIBERO 上报告 98.3% 的平均成功率，在 RLBench 上是 68.3%，领先几种强基线。RoboWM-Bench 从相反角度检验同一问题：生成视频看起来可能合理，但转成动作后还是会失败。它的机器人评测对强生成模型也偏低，逐步分析显示，很多系统能完成接触，却完不成任务序列。合起来看，机器人领域里有用的 world model 要按执行一致性来判断。

#### 资料来源
- [Mask World Model: Predicting What Matters for Robust Robot Policy Learning](../Inbox/2026-04-21--mask-world-model-predicting-what-matters-for-robust-robot-policy-learning.md): Summary and results for mask-based world modeling, including LIBERO and RLBench success rates.
- [RoboWM-Bench: A Benchmark for Evaluating World Models in Robotic Manipulation](../Inbox/2026-04-21--robowm-bench-a-benchmark-for-evaluating-world-models-in-robotic-manipulation.md): Summary and results showing divergence between visual realism and executable manipulation behavior.

### 跨具身和阶段的共享训练接口
两篇论文把机器人控制周边的训练范围扩展了。UniT 为人类和人形机器人行为引入一套共享的离散动作语言，策略训练和 world-model 训练都建立在同一组 token 上。论文使用了 27,419 条人类轨迹、少样本机器人数据和真人形机器人测试，但摘录没有给出主要差距。VLA Foundry 解决的是另一个瓶颈：它把语言预训练、视觉语言训练和动作训练放进同一套流程，并支持最多 128 张 GPU 的分布式运行和开源模型发布。两者的共同点是为迁移提供基础设施。一条路线尝试跨身体复用人类运动；另一条让完整 VLA 流水线实验更容易复现和比较。

#### 资料来源
- [UniT: Toward a Unified Physical Language for Human-to-Humanoid Policy Learning and World Modeling](../Inbox/2026-04-21--unit-toward-a-unified-physical-language-for-human-to-humanoid-policy-learning-and-world-modeling.md): Summary describes UniT's shared tokenization, human-to-humanoid transfer setting, and evaluation scope.
- [VLA Foundry: A Unified Framework for Training Vision-Language-Action Models](../Inbox/2026-04-21--vla-foundry-a-unified-framework-for-training-vision-language-action-models.md): Summary describes the unified LLM-VLM-VLA training stack and reported open training pipeline.
