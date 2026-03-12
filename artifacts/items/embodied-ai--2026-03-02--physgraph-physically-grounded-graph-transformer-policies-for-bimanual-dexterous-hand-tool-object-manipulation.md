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
- bimanual-manipulation
- dexterous-manipulation
- graph-transformer
- contact-aware-policy
- tool-use
relevance_score: 0.9
run_id: materialize-outputs
---

# PhysGraph: Physically-Grounded Graph-Transformer Policies for Bimanual Dexterous Hand-Tool-Object Manipulation

## Summary
PhysGraph提出了一种面向双手灵巧手-工具-物体操作的物理图Transformer策略，把整个系统按“连杆图”而不是扁平向量来表示。核心价值在于让策略显式利用运动学结构、接触和几何关系，从而在高维接触密集任务中更稳、更准。

## Problem
- 解决的问题是**双手灵巧工具使用**中的策略学习：状态和动作维度很高，接触动力学复杂，双手还要协同控制工具与目标物体。
- 现有方法常把整套手-工具-物体状态压成一个单向量，忽略了手部关节拓扑、连杆局部状态和动态接触结构，导致模型必须从稀疏奖励里“自己猜”物理关系。
- 这很重要，因为如果不能显式建模这些结构，策略容易脆弱、不符合物理规律，也难以扩展到更复杂的精细工具操作任务。

## Approach
- 将双手、工具、物体表示为一个**物理图**：节点是各个刚体/连杆，边是关节连接或动态接触关系。
- 使用**per-link tokenization**：每个连杆单独变成一个token，而不是先汇总成全局状态，这样模型能保留手指局部接触和运动链信息。
- 在Transformer注意力中加入**物理先验偏置**，不是只靠数据学习注意力；偏置包括4类：运动学图距离、边类型/接触状态、几何邻近性、解剖学先验（串联链与手指协同）。
- 这些偏置以**head-specific composite bias**形式直接注入多头注意力，使不同头关注不同物理关系，例如接触中的手指、相邻关节或协同手指。
- 训练范式仍是参考轨迹条件下的强化学习/跟踪控制，但创新点主要在于用图结构和物理偏置来参数化策略网络。

## Results
- 论文声称在“challenging bimanual tool-use tasks”上，PhysGraph在**任务成功率**和**操作精度/运动保真度**上都显著优于SOTA基线**ManipTrans**。
- 参数效率方面，PhysGraph仅使用了**ManipTrans的51%参数量**，同时仍取得更好表现，这是文中最明确的量化结论。
- 泛化方面，作者报告了对**未见过的工具/物体几何形状的zero-shot定性迁移**能力，但摘录中**没有给出具体数值指标**。
- 兼容性方面，方法被描述为可在**三种机器人灵巧手**上训练：**Shadow、Allegro、Inspire**，体现了一定的跨形态通用性。
- 摘录中**未提供更细的定量表格**，因此无法列出具体数据集、绝对成功率、提升幅度或统计显著性数字；最强的具体数字主张是**参数量降至51%**且整体表现优于ManipTrans。

## Link
- [http://arxiv.org/abs/2603.01436v1](http://arxiv.org/abs/2603.01436v1)
