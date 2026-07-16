---
kind: ideas
granularity: day
period_start: '2026-04-13T00:00:00'
period_end: '2026-04-14T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- world-models
- benchmarks
- simulation
- quantization
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/benchmarks
- topic/simulation
- topic/quantization
language_code: zh-CN
---

# 语言引导的操作控制

## 摘要
近期最清晰的变化是更紧的 VLA 基线、直接测试语义控制，以及用于操作数据生成的可供性层。支撑这些判断的证据最强的是：一个简单的 VLM 加 MLP 基线、在留出指令变体上的语言评分规划，以及在物体部位选择决定成败的任务上使用可供性条件抓取生成。

## 使用预训练 VLM 和 MLP 动作头的受控 VLA 基线
许多 VLA 团队现在可以用一个更实用的基线：预训练 VLM 加一个小的连续 MLP 动作头，并在不同任务上用同一套固定流程评估。StarVLA-α 报告了在 LIBERO 上平均 98.8、RoboTwin 2.0 clean* 上 88.2、RoboCasa-GR1 上 53.8 的结果，流程简化，没有针对具体基准做调参。用同一套设置时，MLP 头的表现和更重的动作头相当或更好：RoboCasa-GR1 上 53.8，对比 GR00T 风格头的 52.8 和扩散风格头的 48.9；SimplerEnv Google VM 上 76.0，对比 FAST 的 60.1。

工作流上的改动很直接。在加入机器人预训练、动作分词器、扩散头或额外接口特征之前，团队可以先保留一个固定基线，这个基线由强预训练 VLM、原始 RGB、语言指令、训练集内的动作归一化和连续 MLP 头组成。新组件只有在同一骨干和同一数据上超过这个基线时才值得加入。消融结果支持这种做法：额外的机器人预训练会提升一个基准、拖累另一个，而常见的数据工程改动在任务数据量变大后只带来很小的收益。

一个低成本检查是，把当前的一项内部模型对比在骨干和数据集固定的情况下重跑，然后只比较动作头和一个额外训练技巧。如果简单头能保持在几分之内，或者直接胜出，团队就可以降低模型复杂度，让评测更干净。

### 资料来源
- [StarVLA-$α$: Reducing Complexity in Vision-Language-Action Systems](../Inbox/2026-04-13--starvla-a-reducing-complexity-in-vision-language-action-systems.md): StarVLA-α reports the benchmark results and action-head ablations that support a simple VLM plus MLP baseline.

## 用于语义泛化测试的语言评分轨迹重排序
做指令跟随的机器人团队，可以先加一个带语言评分的规划模块，测试语义泛化，再去训练另一个端到端策略。Grounded World Model 给出了一个具体做法：先为候选动作片段预测未来潜在状态，在共享的视觉语言嵌入空间里按文本指令给每个未来状态打分，然后执行分数最高的片段。在 WISER 上，这个方法的测试成功率是 0.87，训练成功率是 0.92，而 VLA 基线的训练平均是 0.90、测试平均只有 0.22。

这对那些机器人已经见过动作、但在措辞或视觉线索变化后会失败的工作流很有用。WISER 就是按这个压力设计的。具体的 VLA 基线在测试集上的表现分别降到：InstructVLA 0.47，Wall-OSS 0.40，InternVLA-A1 和 π0.5 都是 0.26，其他方法更低。GWM-MPC 迁移到 xArm6 后测试成功率也达到 0.83，这说明这个评分层可以跨不同本体使用。

一个可落地的第一步，是在检索到的轨迹或策略提案上加一个重排序器。保留现有的提案生成器，预测短时域结果，再用冻结的多模态嵌入模型按它们和指令的余弦相似度排序。第一次验证不需要完整的机器人重训，只需要一个留出的指令切分，并加入改写、新指代和保留动作需求的视觉替换。

### 资料来源
- [Grounded World Model for Semantically Generalizable Planning](../Inbox/2026-04-13--grounded-world-model-for-semantically-generalizable-planning.md): Grounded World Model provides the language-conditioned MPC setup and the train/test semantic generalization results on WISER.

## 用于倒水和悬挂任务的可供性条件抓取生成
高依赖物体部位的操作任务，任务文本和轨迹生成之间仍然需要一层支持。AffordSim 把这个缺口显示得很清楚。在 17 个代表性任务上，Pi 0.5 的平均成功率是 61%，但倒水和挂杯子的结果仍然明显低于简单抓取。示例任务中，`pick_banana` 达到 93%，`pour_cup_into_bowl` 是 43%，`hang_mug_on_rack` 是 47%。生成端的消融也指出了缺失的一环：AnyGrasp 的轨迹生成平均只有 20%，而 VoxAfford 达到 61%；在 `pour_into_cup` 这类对可供性敏感的任务上，VoxAfford 是 63%，AnyGrasp 是 0%。

具体做法可以是一个用于数据生成和策略评估的可供性条件抓取提议器。给定像“可抓握把手”或“可倾倒杯沿”这样的任务短语，在物体点云上预测 3D 可供性区域，在这些区域周围采样抓取，再按可供性接触和可达性一起打分。对在仿真中训练模仿策略的团队来说，这很有用，因为在带把手、杯沿、挂钩和开口的物体上，物理上可行的抓取仍可能生成任务错误的演示。

一个低成本检查是，挑选五个依赖物体部位的现有任务，用可供性条件抓取重新生成演示，再和通用抓取规划器对比成功率。早期读数应该重点看倒水、悬挂和工具使用任务，因为这些任务里，选对部位决定了大部分结果。

### 资料来源
- [AffordSim: A Scalable Data Generator and Benchmark for Affordance-Aware Robotic Manipulation](../Inbox/2026-04-13--affordsim-a-scalable-data-generator-and-benchmark-for-affordance-aware-robotic-manipulation.md): AffordSim reports the task breakdown and the affordance-aware trajectory generation ablation that motivate an affordance-conditioned grasp layer.
