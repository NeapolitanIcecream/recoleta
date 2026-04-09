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
这篇论文提出了 **SADU**，一个用于测试视觉语言模型能否读取并推理软件架构图的基准。当前模型在这项任务上离可靠还很远：报告中的最高准确率只有 **70.18%**，而一些常用模型的表现要差得多。

## 问题
- 软件工程基准主要集中在代码上，而架构图这类早期设计产物研究较少。
- 架构图承载系统结构、行为和数据关系，因此图表理解能力弱，会影响架构层面的辅助能力，并造成设计与实现之间的不一致。
- 通用多模态基准没有针对软件专用图表语义进行集中测试。

## 方法
- 作者构建了 **SADU**，这是一个包含 **154** 张精选软件架构图的基准：**51** 张行为图、**53** 张结构图和 **50** 张 ER 图。
- 每张图都配有人工编写的 JSON 结构化标注，包括实体、关系、簇，以及可选的属性或方法；标注总计耗费约 **160** 人工小时。
- 该基准包含 **2,431** 个问答任务，分布在 **24** 个子类型中，覆盖对图表元素的计数、检索和关系推理。
- 作者评测了来自 **Gemini、Claude、GPT 和 Qwen** 系列的 **11** 个 VLM，temperature 设为 **0**，同时使用基于规则的精确匹配评分和 LLM-as-a-judge 协议。
- 他们还按图表类型、问题子类型、复杂度和 token 成本进行了分析。

## 结果
- SADU 从最初的 **1,044** 张图中构建而成，删除 **318** 个重复项、**157** 张低分辨率图、**64** 张无法辨认的图，以及 **311** 个因相关性或标注质量被排除的项目后，最终保留 **154** 张。
- 总体最高准确率是 **gemini-3-flash-preview** 的 **70.18%**。其后依次是 **gemini-2.5-flash: 69.68%**、**gemini-3.1-flash-lite-preview: 66.31%**、**claude-sonnet-4.5: 56.36%**、**gpt-5-nano: 55.45%** 和 **gpt-4o-mini: 17.77%**。
- 不同图表类型上的表现有差异。**gemini-3-flash-preview** 在行为图上得分 **63.58%**，在结构图上得分 **68.87%**，在 ER 图上得分 **78.53%**。**gemini-2.5-flash** 在摘要所列结果中取得最高的 ER 分数，为 **82.54%**。
- 开放权重的 Qwen 模型落后于排名靠前的闭源模型，并呈现明显的参数规模趋势：**qwen-2.5-VL-32B: 45.17%**、**7B: 38.58%**、**3B: 31.30%**。
- 图表复杂度会拉低所有模型的表现：随着实体和关系数量增加，准确率下降，其中行为图和依赖定位能力较强的检索任务被描述为最难的情况。
- 不同模型的 token 成本差异很大。**gpt-5-nano** 平均使用 **1475.19** 个 completion tokens，而许多较轻量的模型平均在 **13–20** 个 token 左右；**gemini-3.1-flash-lite-preview** 以 **66.31%** 的准确率和 **16.94** 的平均 completion tokens，被认为是在准确率与成本之间表现较好的折中方案。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04009v1](http://arxiv.org/abs/2604.04009v1)
