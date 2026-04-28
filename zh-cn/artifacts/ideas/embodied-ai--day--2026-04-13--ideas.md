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

## Summary
最明确的近期变化是更严格的 VLA 基线、直接检验语义控制的测试，以及用于操作数据生成的 affordance 层。现有证据最有力地支持三点：简单的 VLM 加 MLP 基线、在留出指令变体上做语言打分规划，以及在物体部位选择决定成败的任务上使用 affordance 条件抓取生成。

## 使用预训练 VLM 和 MLP 动作头的受控 VLA 基线
对许多 VLA 团队来说，一个实用的基线现在就是预训练 VLM 加一个小型连续 MLP 动作头，并在跨任务时使用同一套固定配方评测。StarVLA-α 在最小化流水线、且不做任何基准专项调参的条件下，报告了 LIBERO 平均 98.8、RoboTwin 2.0 clean* 上 88.2、RoboCasa-GR1 上 53.8。在同样设置下，MLP 动作头可以追平或超过更重的动作头：在 RoboCasa-GR1 上，MLP 为 53.8，GR00T 风格动作为 52.8，扩散风格动作为 48.9；在 SimplerEnv Google VM 上，MLP 为 76.0，FAST 为 60.1。

流程上的变化很直接。在加入机器人预训练、动作 tokenizer、扩散头或额外接口特征之前，团队可以先维护一个固定基线：强预训练 VLM、原始 RGB、语言指令、基于训练集划分的动作归一化，以及连续 MLP 动作头。只有新组件在相同 backbone 和数据条件下超过这个基线后，才值得加入。消融结果支持这种做法：额外机器人预训练会在一个基准上带来提升，却会损害另一个基准；常见的数据工程改动在任务数据足够大时，收益也会缩小到很小。

一个低成本检查方法是，在保持 backbone 和数据集不变的情况下，重跑一次当前内部模型对比，只比较动作头和一项新增训练技巧。如果简单动作头仍只落后几个点，或者直接胜出，团队就可以减少模型复杂度，同时让评测更干净。

### Evidence
- [StarVLA-$α$: Reducing Complexity in Vision-Language-Action Systems](../Inbox/2026-04-13--starvla-a-reducing-complexity-in-vision-language-action-systems.md): StarVLA-α 报告了基准结果和动作头消融，这些结果支持将简单的 VLM 加 MLP 作为基线。

## 用于语义泛化测试的语言打分轨迹重排序
从事指令跟随的机器人团队，可以在再训练一个端到端策略之前，先加上一套按语言打分的规划测试框架，用来检验语义泛化。Grounded World Model 给出了一种具体做法：为候选动作块预测未来潜在状态，在共享的视觉-语言嵌入空间里，把每个未来状态与文本指令做打分，然后执行得分最高的动作块。在 WISER 上，这种方法测试成功率达到 0.87，训练成功率为 0.92，而 VLA 基线在训练集上平均为 0.90，在测试集上只有 0.22。

这对那类工作流很重要：机器人之前见过相关动作，但一旦措辞或视觉线索变化就会失败。WISER 就是围绕这种压力构建的。具名 VLA 基线在保留测试任务上的成绩下降到：InstructVLA 为 0.47，Wall-OSS 为 0.40，InternVLA-A1 和 π0.5 都是 0.26，其他方法更低。GWM-MPC 在迁移到 xArm6 之后，测试成功率也达到 0.83，这说明这层打分机制在不同 embodiment 之间也有用。

一个可落地的第一步，是给检索到的轨迹或策略提案加一个重排序器。保留当前的提案生成器，预测短时域结果，然后在冻结的多模态嵌入模型里，用与指令的余弦相似度来排序。第一轮验证不需要完整重训机器人。它需要的是一个留出的指令划分，其中包含释义改写、新的指代表达，以及在不改变所需动作的前提下替换视觉线索。

### Evidence
- [Grounded World Model for Semantically Generalizable Planning](../Inbox/2026-04-13--grounded-world-model-for-semantically-generalizable-planning.md): Grounded World Model 提供了按语言条件化的 MPC 设置，以及 WISER 上训练/测试语义泛化结果。

## 用于倒水和悬挂任务的 affordance 条件抓取生成
重依赖 affordance 的操作任务，仍然需要在任务文本和轨迹生成之间加一层支持。AffordSim 很清楚地展示了这个缺口。在 17 个代表性任务上，Pi 0.5 平均成功率为 61%，但倒水和挂杯子的表现仍明显低于简单抓取。示例任务中，`pick_banana` 达到 93%，`pour_cup_into_bowl` 为 43%，`hang_mug_on_rack` 为 47%。生成侧消融指出了缺失环节：AnyGrasp 在轨迹生成上平均只有 20%，而 VoxAfford 达到 61%；在 `pour_into_cup` 这类对 affordance 很敏感的任务上，VoxAfford 为 63%，AnyGrasp 为 0%。

一个具体可做的模块，是面向数据生成和策略评估的 affordance 条件抓取提议器。给定像 "graspable handle" 或 "pourable rim" 这样的任务短语，在物体点云上预测 3D affordance 区域，在这些区域周围采样抓取，再同时按 affordance 接触程度和可达性打分。这对在仿真中训练模仿学习策略的团队有用，因为对带把手、边缘、挂钩和开口的物体来说，物理上可行的抓取仍然会生成任务上错误的演示。

一个低成本检查方法，是选取五个依赖物体部位的现有任务，用 affordance 条件抓取重新生成演示，再和通用抓取规划器比较成功率。早期读数应重点看倒水、悬挂和工具使用任务，因为这些任务的结果大多取决于部位选择。

### Evidence
- [AffordSim: A Scalable Data Generator and Benchmark for Affordance-Aware Robotic Manipulation](../Inbox/2026-04-13--affordsim-a-scalable-data-generator-and-benchmark-for-affordance-aware-robotic-manipulation.md): AffordSim 报告了任务拆分和面向 affordance 的轨迹生成消融，这些结果支持加入一层 affordance 条件抓取。
