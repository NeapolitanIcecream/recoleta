---
source: arxiv
url: http://arxiv.org/abs/2604.04009v1
published_at: '2026-04-05T07:54:18'
authors:
- Shuyin Ouyang
- Jie M. Zhang
- Jingzhi Gong
- Gunel Jahangirova
- Mohammad Reza Mousavi
- Jack Johns
- Beum Seuk Lee
- Adam Ziolkowski
- Botond Virginas
- Joost Noppen
topics:
- vision-language-models
- software-architecture
- diagram-understanding
- benchmarking
- multimodal-reasoning
relevance_score: 0.85
run_id: materialize-outputs
language_code: zh-CN
---

# Benchmarking and Evaluating VLMs for Software Architecture Diagram Understanding

## Summary
## 摘要
本文提出 SADU，一个用于测试视觉语言模型能否读取并推理软件架构图的基准。当前模型在这项任务上还不可靠：最佳报告准确率为 70.18%，而几款常用模型的表现差得多。

## 问题
- 软件工程基准大多关注代码，而架构图这类早期设计产物研究较少。
- 架构图包含系统结构、行为和数据关系，因此图理解能力弱会破坏架构层面的辅助，并造成设计与实现之间的不一致。
- 通用多模态基准没有针对软件特定的图语义做集中测试。

## 方法
- 作者构建了 **SADU**，一个包含 **154** 张精心筛选的软件架构图的基准：**51** 张行为图、**53** 张结构图和 **50** 张 ER 图。
- 每张图都配有人工作出的 JSON 结构化标注，包括实体、关系、聚类，以及可选的属性或方法；标注耗时约 **160** 个人工小时。
- 该基准包含 **2,431** 个问答任务，覆盖 **24** 个子类型，涉及对图中元素的计数、检索和关系推理。
- 作者在温度设为 **0** 的条件下评估了来自 **Gemini、Claude、GPT 和 Qwen** 系列的 **11** 个 VLM，并同时使用精确匹配的规则评分和基于 LLM 的裁判流程。
- 他们还按图类型、问题子类型、复杂度和 token 成本分析了难度。

## 结果
- SADU 由最初 **1,044** 张图构成，经过筛选后缩减到 **154** 张；被移除的项目包括 **318** 个重复项、**157** 张低分辨率图像、**64** 张不可读图，以及 **311** 个因相关性或标注质量被排除的项目。
- 总体最佳准确率是 **70.18%**，来自 **gemini-3-flash-preview**。其后依次是 **gemini-2.5-flash: 69.68%**、**gemini-3.1-flash-lite-preview: 66.31%**、**claude-sonnet-4.5: 56.36%**、**gpt-5-nano: 55.45%** 和 **gpt-4o-mini: 17.77%**。
- 不同图类型上的表现差异明显。**gemini-3-flash-preview** 在行为图上得分 **63.58%**，在结构图上得分 **68.87%**，在 ER 图上得分 **78.53%**。**gemini-2.5-flash** 在摘录中报告的 ER 图最高分是 **82.54%**。
- 开源权重的 Qwen 模型落后于表现最好的闭源模型，而且模型越大通常越好：**qwen-2.5-VL-32B: 45.17%**，**7B: 38.58%**，**3B: 31.30%**（总体准确率）。
- 图越复杂，所有模型都更难处理：随着实体和关系数量增加，准确率下降；文中把行为图和依赖定位的检索任务描述为最难的情况。
- 不同模型的 token 成本差别很大。**gpt-5-nano** 平均使用 **1475.19** 个 completion token，而许多更轻量的模型大约只用 **13–20** 个 token；**gemini-3.1-flash-lite-preview** 被描述为准确率和成本之间的较好折中，准确率为 **66.31%**，平均 completion token 为 **16.94**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04009v1](http://arxiv.org/abs/2604.04009v1)
