---
source: arxiv
url: https://arxiv.org/abs/2604.27895v1
published_at: '2026-04-30T14:09:14'
authors:
- Jiawei Liu
- Senqiao Yang
- Mingjun Wang
- Yu Wang
- Bei Yu
topics:
- graph-world-models
- world-models
- embodied-ai
- robotics
- graph-representation-learning
- causal-reasoning
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Graph World Models: Concepts, Taxonomy, and Future Directions

## Summary
## 摘要
这篇综述将图世界模型定义为一类世界模型：它们用节点存储实体，用边存储关系，用于预测、规划和推理。论文按空间、物理和逻辑关系偏置梳理已有工作，并关联到机器人、具身 AI、导航、仿真和 LLM 智能体。

## 问题
- 基于扁平张量的传统世界模型可能把容量耗在像素噪声上，在长程 rollout 中产生漂移，并遗漏规划所需的对象关系或因果关系。
- 在世界模型中使用图的工作分散在强化学习、机器人、计算机视觉、具身 AI 和 LLM 智能体等领域，因此论文旨在给出共同定义和研究版图。
- 这个主题关系到需要更长时域导航、物理预测、操作和指令跟随的智能体，可减少真实世界中的试错。

## 方法
- 论文先将标准世界模型定义为作用于潜在状态的视觉模块 V 和记忆模块 M，然后用图 G_t=(V_t,E_t) 定义图世界模型。
- 图世界模型包含结构抽象 ψ 和关系转移 T_G。结构抽象 ψ 将观测或潜在状态转换为图；关系转移 T_G 在动作条件下随时间更新节点、边和属性。
- 该分类法使用 3 类关系归纳偏置：用于可达性的空间图、用于对象或系统动力学的物理图，以及用于语义或因果推理的逻辑图。
- 论文将代表性方法分为连接器、模拟器和推理器三类，并讨论动态图更新、概率动力学、多粒度关系和 GWM 专用基准等缺口。

## 结果
- 论文没有报告新的基准实验或汇总准确率表；它是一篇综述和分类法论文。
- 论文称自己是第一篇将图世界模型明确定义为统一研究领域的综述，该领域以图结构关系归纳偏置为中心。
- 该分类法有 3 个主要类别：图作为连接器、图作为模拟器、图作为推理器。
- 形式化的 GWM 定义向世界模型加入 2 个核心操作：结构抽象 ψ 和关系转移 T_G。
- 综述中列出的具体能力主张包括：HD-VPD 能实时处理超过 100,000 个隐式粒子，用于高保真动态仿真；SPTM、SoRB、POINT、L3P、Dreamwalker 和 CityNavAgent 等图导航方法将连续观测上的搜索转化为节点和边上的搜索。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.27895v1](https://arxiv.org/abs/2604.27895v1)
