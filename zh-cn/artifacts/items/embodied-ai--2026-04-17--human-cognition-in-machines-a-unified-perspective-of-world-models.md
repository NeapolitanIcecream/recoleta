---
source: arxiv
url: http://arxiv.org/abs/2604.16592v1
published_at: '2026-04-17T17:51:46'
authors:
- Timothy Rupprecht
- Pu Zhao
- Amir Taherin
- Arash Akbari
- Arman Akbari
- Yumei He
- Sean Duffy
- Juyi Lin
- Yixiao Chen
- Rahul Chowdhury
- Enfu Nan
- Yixin Shen
- Yifan Cao
- Haochen Zeng
- Weiwei Chen
- Geng Yuan
- Jennifer Dy
- Sarah Ostadabbas
- Silvia Zhang
- David Kaeli
- Edmund Yeh
- Yanzhi Wang
topics:
- world-models
- cognitive-architecture
- survey-paper
- embodied-ai
- sim2real
- scientific-discovery-agents
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Human Cognition in Machines: A Unified Perspective of World Models

## Summary
## 摘要
这篇论文是一篇综述和立场论文，不是一个新训练的世界模型。论文主张应当按照认知架构理论中的认知功能来分类世界模型，并提出了一个统一视角，覆盖视频、具身和“认知型”世界模型。

## 问题
- 现有世界模型综述大多按架构分类，或按表征与生成的宽泛划分来组织方法。作者认为，这种做法掩盖了一个系统实际改进了哪些认知功能。
- 许多论文把世界模型描述为具有类人的认知能力，但作者认为，这些说法缺少与认知架构理论的一阶原理对照，尤其是在动机和元认知方面。
- 这很重要，因为研究投入可能会偏向被夸大的能力，而与智能体行为、规划和自我监控相关的关键缺失功能仍然薄弱，甚至根本不存在。

## 方法
- 论文围绕七种认知功能建立了一个世界模型分类体系：记忆、感知、语言、推理、想象、动机和元认知。
- 它将这一分类体系应用到三个领域：视频世界模型、具身世界模型，以及一个新提出的类别——认知型世界模型，用于在结构化知识上进行科学发现。
- 它提出了一个概念上的统一世界模型，将多模态感知、潜在状态记忆、语言接口、通过 rollout 或 sim2real transfer 实现的想象、推理模块、基于奖励的动机，以及通过 global workspace 风格机制实现的元认知控制结合起来。
- 它使用 JEPA、Dreamer 风格智能体、多模态具身系统和智能体框架等例子，说明以往工作如何对应到具体认知功能，而不是被放进单一的架构类别。
- 它将动机和元认知识别为主要研究缺口，并指出 active inference 和 global workspace theory 是可行的研究方向。

## 结果
- 论文声称自己是**第一篇**按认知架构理论中的认知功能对世界模型进行分类的综述；表 1 将其范围与 **2025-2026** 年的 **8** 篇既有综述进行了比较，并标注该综述覆盖视频、具身、仿真、物理对齐、认知型模型和基于 CAT 的分析。
- 它引入了**1 个新类别**，即**认知型世界模型**，定义为在结构化知识空间上运行、用于科学发现等任务的智能体系统。
- 它定义了一个包含 **7 种认知功能**的统一分类体系：记忆、感知、语言、推理、想象、动机和元认知。
- 它提出了一个明确的缺口判断：当前最先进的世界模型基本缺少手工设计奖励之外的内在动机，论文还称**没有任何**系统展示出真正的元认知能力，例如自我监控、自我评估或自我控制。
- 摘录中**没有实验基准结果**，也没有给所提模型提供新的任务指标。它的主要贡献是概念性的：一个分类体系、一次综述比较、一个统一设计提案，以及对研究缺口的识别。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16592v1](http://arxiv.org/abs/2604.16592v1)
