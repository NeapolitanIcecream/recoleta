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
这篇综述将图世界模型定义为把实体存为节点、把关系存为边，用于预测、规划和推理的世界模型。它按空间、物理和逻辑三类关系归纳偏置，并把相关工作连接到机器人、具身 AI、导航、仿真和 LLM 代理。

## Problem
- 基于扁平张量的传统世界模型会把容量花在像素噪声上，在长时滚动预测中发生漂移，还会漏掉规划所需的对象关系或因果关系。
- 世界模型里的图方法分散在强化学习、机器人、计算机视觉、具身 AI 和 LLM 代理中，所以这篇论文想给出统一定义和分类图谱。
- 对需要更长时程导航、物理预测、操作和按指令执行、同时减少真实世界试错的代理来说，这个主题很重要。

## Approach
- 论文先把标准世界模型定义为基于潜在状态的视觉模块 V 和记忆模块 M，再把图世界模型定义为图 G_t=(V_t,E_t)。
- 图世界模型包含结构抽象 ψ，用来把观测或潜在状态转换成图；还包含关系转移 T_G，在动作作用下随时间更新节点、边和属性。
- 这个分类法使用 3 类关系归纳偏置：用于可达性抽象的空间图、用于对象或系统动力学的物理图、用于语义或因果推理的逻辑图。
- 论文把代表性方法分成连接器、模拟器和推理器三类，然后讨论动态图更新、概率动力学、多粒度关系和 GWM 专用基准等缺口。

## Results
- 论文没有新的基准实验或汇总准确率表；它是一篇综述和分类论文。
- 论文声称自己是第一篇把图世界模型明确界定为一个以图结构关系归纳偏置为中心的统一研究领域的综述。
- 这个分类法有 3 个主要类别：图作为连接器、图作为模拟器、图作为推理器。
- 形式化的 GWM 定义给世界模型增加了 2 个核心操作：结构抽象 ψ 和关系转移 T_G。
- 综述中给出的具体能力例子包括：HD-VPD 可实时处理超过 100,000 个隐式粒子，用于高保真动态仿真；SPTM、SoRB、POINT、L3P、Dreamwalker 和 CityNavAgent 等图导航方法把在连续观测上的搜索，转成在节点和边上的搜索。

## Link
- [https://arxiv.org/abs/2604.27895v1](https://arxiv.org/abs/2604.27895v1)
