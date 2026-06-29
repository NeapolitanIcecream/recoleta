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
本文是一篇关于视觉-语言-动作机器人研究的综述，重点放在数据、评测和可扩展的数据生成上，而不是模型架构。文章认为，VLA 的进展取决于更好的数据集、基准和数据引擎，并把这一领域组织为这三部分。

## 问题
- VLA 研究缺少一张清晰的数据视角地图，说明有哪些训练数据、基准如何测试泛化，以及可扩展的数据流水线如何运作。
- 真实机器人数据成本高、覆盖面窄，合成数据更容易扩展，但常常缺少真实的视觉和物理细节，这会影响仿真到真实的迁移。
- 现有基准使用不同的任务、环境和成功标准，因此很难比较方法，也难以准确衡量长时程和组合泛化。

## 方法
- 论文通过三个类别来综述 VLA 操作研究：**数据集**、**基准**和**数据引擎**。
- 它按真实世界与合成来源、具身多样性、模态组合，以及动作空间设计来分类数据集，例如末端执行器控制与关节控制、绝对动作与增量动作。
- 它从两个维度分析基准：**任务复杂度**和**环境结构**，覆盖从短时程桌面任务到长时程多场景设置。
- 它把数据引擎分为**视频转数据**、**硬件辅助采集**和**生成式引擎**，这些方法用于创建或扩充机器人训练数据。
- 它归纳出围绕不同具身之间的表征对齐、多模态监督、推理评测以及带有物理真实性的可扩展数据生成等开放问题。

## 结果
- 这是一篇综述论文，因此**没有**报告新的模型性能数值或新的最先进结果。
- 论文声称这是**首篇**从**数据视角**研究 VLA 的综述，并在统一分类体系下覆盖了**2023 到 2025 年**的相关工作。
- 它定义了三个主要综述支柱：**数据集、基准、数据引擎**，并列举了代表性资源，例如 **Open X-Embodiment（22 个机器人）**、**Meta-World（50 个任务）**和 **COLOSSEUM（14 个扰动轴）**。
- 它指出存在持续的**真实性-成本权衡**：真实世界数据集提供更好的物理约束，但成本高；合成数据集更容易扩展，但真实性和迁移能力较弱。
- 它发现当前基准在**组合泛化**和**长时程推理**评测上仍有缺口，尤其是在任务难度和环境变化相互交织时。
- 论文在文中给出的 GitHub 链接上发布了一个**持续更新**的 VLA 数据集和基准仓库。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23001v1](http://arxiv.org/abs/2604.23001v1)
