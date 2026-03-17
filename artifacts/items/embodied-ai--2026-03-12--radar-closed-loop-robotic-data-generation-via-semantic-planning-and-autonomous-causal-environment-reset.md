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
- autonomous-data-collection
- vision-language-models
- in-context-imitation-learning
- robot-manipulation
- environment-reset
relevance_score: 0.95
run_id: materialize-outputs
---

# RADAR: Closed-Loop Robotic Data Generation via Semantic Planning and Autonomous Causal Environment Reset

## Summary
RADAR提出了一个面向机器人操作数据采集的全自动闭环系统，目标是在几乎不需要人工参与的情况下持续生成高质量真实世界交互数据。它把“想做什么、怎么做、是否成功、如何复位”拆成四个模块，从少量人类演示扩展到持续自主收集。

## Problem
- 机器人基础模型需要大规模高质量物理交互数据，但人工遥操作采集昂贵、缓慢且难以扩展。
- 现有自动化方案常在语义规划到物理执行之间断裂：VLM容易产生2D/像素级幻觉，低层策略又缺少自主任务生成与结果验证能力。
- 更关键的是，大多数系统无法自主环境复位，导致采集流程无法真正闭环，最终仍需人工介入。

## Approach
- 用仅**2-5个**3D人类演示构建一个affordance library，作为几何与动作先验，而不是让VLM直接“猜”3D坐标。
- 由VLM先做**语义目标识别+层级任务规划**：识别场景中真实存在的对象，生成原子任务或长时程任务链，并从演示库中检索最匹配的技能示例。
- 低层执行使用**GNN-based in-context imitation learning / graph diffusion policy**，把当前观测和检索到的演示作为上下文，生成连续机器人动作轨迹。
- 执行后，系统用**三阶段VQA成功评估**：把命令转成视觉问题，交给VLM判断，再用解析器转成严格布尔值，减少语言冗余和误判。
- 为实现真正闭环，系统在规划前向任务时同步生成**逆向复位计划**，并由FSM按照严格**LIFO因果顺序**执行复位；若复位失败，则采用非对称数据保存与重新规划，使流程继续运行。

## Results
- 仿真中，RADAR在**复杂长时程任务上成功率最高达到90%**。
- 论文声称在一些挑战性任务上，传统基线会**降到接近0%性能**，而RADAR仍能稳定求解；但摘录中未给出更细的数据集、基线名称或完整表格数值。
- 系统仅需**2-5个手工原子演示**即可启动自动数据生成流程，显著降低人工采集负担。
- 真实机器人部署中，系统可通过**one-shot或few-shot**适应执行多种接触丰富技能，包括**可变形物体操作**（如折毛巾）和**高精度对齐/插入**（如纸卷插入），且**无需特定领域微调**。
- 摘录未提供真实世界实验的定量成功率，因此当前最强证据主要是“跨仿真与真实环境均可工作、且支持自主复位与连续采集”的定性与部分定量主张。

## Link
- [http://arxiv.org/abs/2603.11811v1](http://arxiv.org/abs/2603.11811v1)
