---
source: arxiv
url: http://arxiv.org/abs/2604.23001v1
published_at: '2026-04-24T20:41:59'
authors:
- Ziyao Wang
- Bingying Wang
- Hanrong Zhang
- Tingting Du
- Tianyang Chen
- Guoheng Sun
- Yexiao He
- Zheyu Shen
- Wanghao Ye
- Ang Li
topics:
- vision-language-action
- robotics-survey
- robot-datasets
- robot-benchmarks
- sim2real
- embodied-ai
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Vision-Language-Action in Robotics: A Survey of Datasets, Benchmarks, and Data Engines

## Summary
## 摘要
这篇论文是一篇关于视觉-语言-动作机器人研究的综述，重点放在数据、评测和可扩展的数据生成上，而不是模型架构。论文认为，VLA 的进展将更多依赖更好的数据集、基准和数据引擎，并围绕这三部分组织整个领域。

## 问题
- VLA 研究缺少一张清晰的数据中心图谱：现有训练数据有哪些、基准如何测试泛化能力、可扩展的数据流水线如何工作。
- 真实机器人数据成本高、覆盖面窄，而合成数据更容易扩展，但常常缺少真实的视觉和物理细节，因此会削弱 sim-to-real transfer。
- 现有基准使用不同的任务、环境和成功标准，因此很难公平比较方法，也难以很好地衡量长时程和组合泛化能力。

## 方法
- 论文通过三类内容综述 VLA 操作研究：**datasets**、**benchmarks** 和 **data engines**。
- 它按照真实世界与合成来源、具身形态多样性、模态组合，以及动作空间设计进行数据集分类，例如末端执行器控制与关节控制、绝对动作与增量动作。
- 它用两个维度分析基准：**task complexity** 和 **environment structure**，覆盖从短时程桌面任务到长时程多场景设置。
- 它将数据引擎分为 **video-to-data**、**hardware-assisted collection** 和 **generative engines**，这些方法用于创建或增强机器人的训练数据。
- 它归纳出几个开放挑战：跨具身形态的表示对齐、多模态监督、推理评测，以及具备物理真实感的可扩展数据生成。

## 结果
- 这是一篇综述论文，因此**不**报告新的模型性能数字，也没有新的 state-of-the-art 结果。
- 它称自己是**第一篇综述**，从**数据中心**视角研究 VLA，并用统一的分类体系覆盖 **2023 到 2025** 年的工作。
- 它定义了综述的三个核心支柱：**datasets、benchmarks、data engines**，并列出了一些代表性资源，例如 **Open X-Embodiment (22 robots)**、**Meta-World (50 tasks)** 和 **COLOSSEUM (14 perturbation axes)**。
- 它指出一个持续存在的**保真度-成本权衡**：真实世界数据集提供更好的物理落地性，但成本高；合成数据集更容易扩展，但真实性和迁移能力较弱。
- 它认为，当前基准在**组合泛化**和**长时程推理**评测上仍有缺口，尤其是在任务难度和环境变化混在一起时。
- 它发布了一个**持续更新的仓库**，汇总 VLA 数据集和基准，链接是论文中给出的 GitHub 地址。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23001v1](http://arxiv.org/abs/2604.23001v1)
