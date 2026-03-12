---
source: arxiv
url: http://arxiv.org/abs/2603.01436v1
published_at: '2026-03-02T04:32:20'
authors:
- Runfa Blark Li
- David Kim
- Xinshuang Liu
- Keito Suzuki
- Dwait Bhatt
- Nikola Raicevic
- Xin Lin
- Ki Myung Brian Lee
- Nikolay Atanasov
- Truong Nguyen
topics:
- robotics
- graph-transformer
- dexterous-manipulation
- bimanual-control
- tool-use
relevance_score: 0.18
run_id: materialize-outputs
---

# PhysGraph: Physically-Grounded Graph-Transformer Policies for Bimanual Dexterous Hand-Tool-Object Manipulation

## Summary
PhysGraph提出一种面向双手灵巧手-工具-物体操作的物理先验图Transformer策略，用图结构而不是扁平向量来表示系统。核心思想是把每个连杆当作一个token，并把运动学、接触、几何和解剖学先验直接注入注意力机制。

## Problem
- 解决的是**双手高自由度灵巧操作中的工具使用控制**问题，尤其是涉及手、工具、物体三者复杂接触的任务。
- 现有方法常把整个系统压成单一状态向量，忽略手部运动学拓扑、局部接触关系和跨手协调结构，导致学习效率低、行为脆弱。
- 这很重要，因为精细工具操作（如切割、剪切等）要求稳定抓握、接触推理和双手协同，是通向更通用机器人操作能力的关键难题。

## Approach
- 将双手、工具、物体建模为一个**物理图**：节点是连杆/刚体，边是关节连接或动态接触。
- 使用**per-link tokenization**：每个连杆单独编码成token，而不是把全局状态拼成一个大向量，从而保留细粒度局部信息。
- 在Transformer注意力中加入**物理驱动复合偏置**，让模型显式关注合理的物理关系，而不是完全靠稀疏奖励自己摸索。
- 复合偏置包含四类先验：**运动学图距离**、**边类型/接触状态**、**几何空间邻近性**、以及**解剖学先验**（如同一手指串联关系、不同手指同层级协同关系）。
- 该策略仍采用参考轨迹条件的强化学习范式，但用拓扑感知的图Transformer来参数化策略与价值函数。

## Results
- 论文声称PhysGraph在**操作精度**和**任务成功率**上都显著优于SOTA基线**ManipTrans**，但给定摘录**没有提供具体数值表格、数据集名称或百分比提升幅度**。
- 参数效率方面，PhysGraph仅使用ManipTrans的**51%参数量**，同时取得更好性能。
- 泛化方面，作者声称架构因拓扑灵活性而具备对**未见工具/物体几何**的**定性zero-shot迁移**能力，但摘录中未给出定量指标。
- 兼容性方面，方法被描述为可训练于**3种机器人手**：**Shadow、Allegro、Inspire**。
- 论文还声称是首个面向**高DoF双手灵巧工具使用任务**的图Transformer策略，但这一点属于方法定位主张，而非可独立验证的量化结果。

## Link
- [http://arxiv.org/abs/2603.01436v1](http://arxiv.org/abs/2603.01436v1)
