---
source: arxiv
url: http://arxiv.org/abs/2603.11811v1
published_at: '2026-03-12T11:18:52'
authors:
- Yongzhong Wang
- Keyu Zhu
- Yong Zhong
- Liqiong Wang
- Jinyu Yang
- Feng Zheng
topics:
- robot-data-generation
- vision-language-models
- imitation-learning
- environment-reset
- long-horizon-planning
relevance_score: 0.28
run_id: materialize-outputs
---

# RADAR: Closed-Loop Robotic Data Generation via Semantic Planning and Autonomous Causal Environment Reset

## Summary
RADAR 是一个面向机器人数据采集的全自动闭环系统，目标是在几乎不需要人工参与的情况下持续生成高质量物理交互数据。它把“想做什么、怎么执行、是否成功、如何复原环境”拆成四个模块联动运行。

## Problem
- 机器人学习需要大量真实世界交互数据，但人工遥操作采集成本高、速度慢且难以扩展。
- 现有自动化方案通常无法可靠地把高层语义任务转成可执行的物理动作，还常依赖脆弱的2D猜测或会产生几何幻觉的图像生成。
- 更关键的是，很多系统不能自动判断任务是否成功，也不能自动把环境复位，因此仍离不开人工介入，无法形成持续闭环采集。

## Approach
- 用仅 **2-5** 个3D人工演示构建一个“affordance library”，把它作为几何先验，而不是让VLM直接凭空生成3D动作。
- 先由 **VLM** 做语义层工作：场景中目标物体识别、任务生成、长时程任务分解，以及从演示库中检索语义和几何上最匹配的技能示例。
- 再由基于 **GNN 的 in-context imitation learning / graph diffusion policy** 把“当前观察 + 检索到的示例”转成连续机器人动作轨迹，相当于用少样本示范驱动执行。
- 执行后通过一个 **三阶段 VQA 成功评估**（任务转问题、VLM视觉判断、LLM布尔解析）自动筛掉失败轨迹，避免单步VLM判断的不稳定性。
- 为了去掉人工复位，系统在规划正向任务时同步生成逆向复位计划，并由 **FSM** 按严格 **LIFO** 因果顺序执行环境重置；若复位失败，则采用非对称数据保存与重新规划机制继续采集。

## Results
- 仿真中，RADAR 在复杂长时程任务上达到 **最高 90% success rate**。
- 论文声称在一些困难任务上，传统基线方法的表现会**跌到接近 0**，而 RADAR 仍能保持高成功率，但摘录中未提供更细的基线名称、数据集名或逐项数值表。
- 系统只需 **2-5 个**人工原子演示，就能扩展为持续的数据生成流程，显著减少人工参与。
- 真实机器人部署中，RADAR 可通过 **one-shot 或 few-shot** 适配执行多种接触丰富技能，包括**可变形物体操作**（如折毛巾）和**高精度对齐**（如纸卷插入），且**无需 domain-specific fine-tuning**。
- 摘录没有给出真实世界实验的定量指标，因此最强的具体结论是：系统在仿真与现实中都展示了无需人工闭环干预的持续数据采集能力。

## Link
- [http://arxiv.org/abs/2603.11811v1](http://arxiv.org/abs/2603.11811v1)
