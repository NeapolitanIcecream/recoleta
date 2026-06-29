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
## 概述
本文是一篇综述和立场论文，不是一个新训练的世界模型。它主张应按认知架构理论中的认知功能来分类世界模型，并提出一个统一视角，涵盖视频、具身和“认识性”世界模型。

## 问题
- 现有世界模型综述多按架构，或按“表征”和“生成”的宽泛划分来归类方法。作者认为，这会掩盖系统实际上提升了哪些认知功能。
- 许多论文把世界模型描述成人类式认知，但作者认为这些说法缺少与认知架构理论的扎实对照，尤其是在动机和元认知上。
- 这很重要，因为研究投入可能会流向被夸大的能力，而代理行为、规划和自我监控所需的关键功能仍然薄弱或缺失。

## 方法
- 论文围绕七种认知功能建立世界模型分类：记忆、感知、语言、推理、想象、动机和元认知。
- 这套分类被应用到三个领域：视频世界模型、具身世界模型，以及一个新提出的类别“认识性世界模型”，用于在结构化知识上进行科学发现。
- 论文提出一个概念性的统一世界模型，把多模态感知、潜在状态记忆、语言接口、通过 rollout 或 sim2real 迁移实现的想象、推理模块、基于奖励的动机，以及通过类似全局工作空间机制的元认知控制结合起来。
- 文中用 JEPA、Dreamer 风格代理、多模态具身系统和代理框架等例子，说明已有工作应按具体认知功能来归类，而不是只放进单一架构桶里。
- 作者把动机和元认知列为主要研究缺口，并把主动推断和全局工作空间理论作为可行方向。

## 结果
- 论文称自己是**第一篇**按认知架构理论中的认知功能对世界模型分类的综述；表 1 将其范围与 **8** 篇来自 **2025-2026** 年的既有综述进行比较，并将其综述标记为覆盖视频、具身、模拟、物理对齐、认识性模型和基于 CAT 的分析。
- 论文提出 **1 个新类别**，即**认识性世界模型**，定义为在结构化知识空间上运行、用于科学发现等任务的代理系统。
- 论文给出一个包含 **7** 种认知功能的统一分类法：记忆、感知、语言、推理、想象、动机和元认知。
- 论文明确指出一个缺口：当前最先进的世界模型大多缺少超出手工设计奖励之外的内在动机，而且论文认为**没有**模型展示出真正的元认知能力，例如自我监控、自我评估或自我控制。
- 摘要没有给出任何实验基准结果，也没有给出所提模型的新任务指标。主要贡献是概念性的：一个分类法、一项综述比较、一个统一设计提案，以及已识别的研究缺口。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16592v1](http://arxiv.org/abs/2604.16592v1)
