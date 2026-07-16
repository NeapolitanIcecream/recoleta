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

# 机器人论文更看重更干净的基线和更尖锐的语义控制测试

## 概览
4 月 13 日的机器人论文集在把评估收紧到具体控制问题时最有力。证据最充分的论文都在问：一个简单的 VLA 方案是否已经让很多基准接近饱和，视觉特征是否真的包含动作信息，以及世界模型能否用有语义意义的方式给未来打分。StarVLA-α、LARYBench 和 GWM-MPC 提供了最清楚的证据。

## 研究发现

### 在受控评估下，简单的 VLA 基线依然站得住
StarVLA-α 提出了这一时间段里最清楚的判断：只要训练方案受控，一个普通的视觉-语言模型（VLM）加一个小型 MLP 动作头，就能追平或超过更重的视觉-语言-动作系统。它的专用模型在 LIBERO 上报告平均 98.8，在 RoboTwin 2.0 clean* 上是 88.2，在 RoboCasa-GR1 上是 53.8；同一设置下，简单的 MLP 头与更复杂的头持平，甚至更好。消融结果和主指标一样重要。额外的机器人预训练对一些基准有帮助，对另一些有害；当任务数据足够多时，常见管线增补只带来很小的收益。当天最扎实的结果不是新架构，而是更清楚地说明了什么会真正改变结果。

#### 资料来源
- [StarVLA-$α$: Reducing Complexity in Vision-Language-Action Systems](../Inbox/2026-04-13--starvla-a-reducing-complexity-in-vision-language-action-systems.md): Summary and benchmark results for the simple VLM-to-action baseline and its ablations.

### 评估开始聚焦动作语义和可供性
基准越来越清楚地要求表示在被称为对控制有用之前，先完成什么任务。LARYBench 同时测试语义动作解码和低层轨迹回归，结论很直接：通用视觉编码器已经强于很多专门的潜在动作模型。V-JEPA 2 的平均动作分类达到 76.62%，而 DINOv3 在控制回归上给出最好的 0.19 平均 MSE。AffordSim 针对的是另一类失败。它表明，模仿策略在需要作用到物体正确部位的任务上仍然会失效。在 17 个代表性任务里，Pi 0.5 的平均成功率是 61%，但倒液和杯子悬挂仍然远低于简单抓取；在这些任务上，考虑可供性的轨迹生成明显优于通用抓取。

#### 资料来源
- [LARY: A Latent Action Representation Yielding Benchmark for Generalizable Vision-to-Action Alignment](../Inbox/2026-04-13--lary-a-latent-action-representation-yielding-benchmark-for-generalizable-vision-to-action-alignment.md): Benchmark evidence that general visual encoders outperform latent action models on semantics and control regression.
- [AffordSim: A Scalable Data Generator and Benchmark for Affordance-Aware Robotic Manipulation](../Inbox/2026-04-13--affordsim-a-scalable-data-generator-and-benchmark-for-affordance-aware-robotic-manipulation.md): Benchmark evidence that affordance-heavy manipulation remains difficult and benefits from affordance-aware data generation.

### 世界模型的评价开始看语义评分和部署成本
这一时期的世界模型尝试让规划和动作解码更有语义依据。AIM 在未来预测和动作生成之间插入空间价值图，然后报告在 RoboTwin 2.0 Easy 上平均成功率 94.0%，在 Hard 上是 92.1%。Grounded World Model 用共享的语言-图像潜空间做模型预测控制，因此候选未来是按文本指令评分，而不是按目标图像评分。在 WISER 上，这带来 0.87 的测试成功率，而 VLA 基线平均只有 0.22，同时训练成功率保持在 0.92。DexWorldModel 在部署阶段指向同一个问题：预测语义特征，把记忆规模固定住，并把一部分推理放到机器人执行期间。它给出的延迟数字很具体，约 50%，但可见摘录里的任务性能证据仍然有限。

#### 资料来源
- [AIM: Intent-Aware Unified world action Modeling with Spatial Value Maps](../Inbox/2026-04-13--aim-intent-aware-unified-world-action-modeling-with-spatial-value-maps.md): AIM results on spatial intent modeling and RoboTwin success rates.
- [Grounded World Model for Semantically Generalizable Planning](../Inbox/2026-04-13--grounded-world-model-for-semantically-generalizable-planning.md): Grounded World Model results on language-conditioned planning and WISER generalization.
- [DexWorldModel: Causal Latent World Modeling towards Automated Learning of Embodied Tasks](../Inbox/2026-04-13--dexworldmodel-causal-latent-world-modeling-towards-automated-learning-of-embodied-tasks.md): DexWorldModel claims on semantic latents, O(1) memory, and latency reduction, with limited quantitative task evidence in the excerpt.

### 设备端效率被表述为漂移控制
效率方向的工作正在更接近机器人特有的失效分析。DA-PTQ 把量化误差当作控制问题来处理，关键风险被定义为轨迹随时间漂移，而不是静态层重建误差。这个方法加入接口补偿和感知漂移的混合精度，目标是在校准后不增加运行时成本的前提下，让低比特 VLA 的行为尽量接近全精度。这个思路符合当天对执行一致性的关注，但可见摘录没有给出基准表，所以它仍然是一个合理的系统贡献，只是本地语料里的可见验证有限。

#### 资料来源
- [DA-PTQ: Drift-Aware Post-Training Quantization for Efficient Vision-Language-Action Models](../Inbox/2026-04-13--da-ptq-drift-aware-post-training-quantization-for-efficient-vision-language-action-models.md): Summary of drift-aware quantization and the lack of quantitative benchmark tables in the excerpt.
