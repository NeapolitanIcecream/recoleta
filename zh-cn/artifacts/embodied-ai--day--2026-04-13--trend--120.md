---
kind: trend
trend_doc_id: 120
granularity: day
period_start: '2026-04-13T00:00:00'
period_end: '2026-04-14T00:00:00'
topics:
- robotics
- vision-language-action
- world-models
- benchmarks
- simulation
- quantization
run_id: materialize-outputs
aliases:
- recoleta-trend-120
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/benchmarks
- topic/simulation
- topic/quantization
language_code: zh-CN
---

# 机器人论文更奖励干净的基线和更锋利的语义控制测试

## Overview
4 月 13 日这组机器人论文最有说服力的地方，是把评测收缩到具体的控制问题上。证据最充分的论文主要在回答三个问题：一个简单的 VLA 配方是否已经让许多基准接近饱和，视觉特征是否真的携带动作信息，以及世界模型能否以有语义意义的方式给候选未来打分。StarVLA-α、LARYBench 和 GWM-MPC 提供了最清晰的证据。

## Clusters

### 简单 VLA 基线在受控评测下依然站得住
StarVLA-α给出了这一时期最明确的结论：在控制变量后的配方下，一个普通的视觉语言模型（VLM）加上一个小型 MLP 动作头，就能追平或超过更重的视觉语言动作系统。它的专用模型在 LIBERO 上平均达到 98.8，在 RoboTwin 2.0 clean* 上达到 88.2，在 RoboCasa-GR1 上达到 53.8，而且这个简单的 MLP 头在相同设置下追平或超过了更复杂的动作头。消融实验和这些主要数字同样重要。额外的机器人预训练对一些基准有帮助，对另一些则有损害；而常见流水线增强在任务数据足够大后只带来很小的收益。这一天最强的具体结果不是一套新架构，而是对究竟哪些因素会改变结果做了更清楚的核算。

#### Evidence
- [StarVLA-$α$: Reducing Complexity in Vision-Language-Action Systems](../Inbox/2026-04-13--starvla-a-reducing-complexity-in-vision-language-action-systems.md): 简单 VLM-to-action 基线及其消融实验的摘要和基准结果。

### 评测开始聚焦动作语义和 affordance
各类基准正在更严格地界定：一种表征要做到什么程度，才算对控制有用。LARYBench同时测试语义动作解码和底层轨迹回归，结果很直接：通用视觉编码器已经强于许多专门的潜在动作模型。V-JEPA 2 的平均动作分类达到 76.62%，而 DINOv3 在控制回归上取得了最好的 0.19 平均 MSE。AffordSim则针对另一种失败模式。它表明，模仿学习策略在那些要求机器人作用于物体正确部位的任务上仍然会失效。在 17 个代表性任务中，Pi 0.5 的平均成功率是 61%，但倒水和杯子悬挂的表现仍远低于简单抓取，而在这些任务上，具备 affordance 感知的轨迹生成相比通用抓取有明显优势。

#### Evidence
- [LARY: A Latent Action Representation Yielding Benchmark for Generalizable Vision-to-Action Alignment](../Inbox/2026-04-13--lary-a-latent-action-representation-yielding-benchmark-for-generalizable-vision-to-action-alignment.md): 基准结果表明，通用视觉编码器在语义和控制回归上优于潜在动作模型。
- [AffordSim: A Scalable Data Generator and Benchmark for Affordance-Aware Robotic Manipulation](../Inbox/2026-04-13--affordsim-a-scalable-data-generator-and-benchmark-for-affordance-aware-robotic-manipulation.md): 基准结果表明，affordance 要求高的操作仍然困难，并且会受益于 affordance 感知的数据生成。

### 世界模型的评判标准转向语义打分和部署成本
这一时期的世界模型在尝试让规划和动作解码建立在更扎实的语义基础上。AIM 在未来预测和动作生成之间插入了空间价值图，并报告在 RoboTwin 2.0 Easy 上平均成功率为 94.0%，在 Hard 上为 92.1%。Grounded World Model 则把共享的语言-图像潜在空间用于模型预测控制，因此候选未来不是对照目标图像打分，而是对照文本指令打分。在 WISER 上，它把测试成功率做到 0.87，而 VLA 基线平均只有 0.22，同时训练成功率保持在 0.92。DexWorldModel 在部署阶段也指向同一个问题：预测语义特征，让内存开销不随时域增长，并把一部分推理隐藏在机器人执行期间。它关于延迟的说法很具体，大约是 50%，但在现有摘录里，任务性能证据仍然偏少。

#### Evidence
- [AIM: Intent-Aware Unified world action Modeling with Spatial Value Maps](../Inbox/2026-04-13--aim-intent-aware-unified-world-action-modeling-with-spatial-value-maps.md): AIM 在空间意图建模和 RoboTwin 成功率上的结果。
- [Grounded World Model for Semantically Generalizable Planning](../Inbox/2026-04-13--grounded-world-model-for-semantically-generalizable-planning.md): Grounded World Model 在语言条件规划和 WISER 泛化上的结果。
- [DexWorldModel: Causal Latent World Modeling towards Automated Learning of Embodied Tasks](../Inbox/2026-04-13--dexworldmodel-causal-latent-world-modeling-towards-automated-learning-of-embodied-tasks.md): DexWorldModel 关于语义潜变量、O(1) 内存和延迟降低的说法；摘录中的定量任务证据有限。

### 端侧效率被表述为漂移控制
效率方向的工作正在更接近机器人特有的失效分析。DA-PTQ把量化误差当作控制问题处理，核心风险被定义为轨迹随时间漂移，而不是静态层重建误差。该方法加入接口补偿和漂移感知的混合精度，目标是在校准后不增加额外运行时成本的前提下，让低比特 VLA 的行为尽量接近全精度。这个思路符合当天更广泛的重点，即执行保真度，但现有摘录没有给出基准表，因此它目前仍是一个看起来合理的系统贡献，在本地语料中可见的验证有限。

#### Evidence
- [DA-PTQ: Drift-Aware Post-Training Quantization for Efficient Vision-Language-Action Models](../Inbox/2026-04-13--da-ptq-drift-aware-post-training-quantization-for-efficient-vision-language-action-models.md): 漂移感知量化的摘要，以及摘录中缺少定量基准表。
