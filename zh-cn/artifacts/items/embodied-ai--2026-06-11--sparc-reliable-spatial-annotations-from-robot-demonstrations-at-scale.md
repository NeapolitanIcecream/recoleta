---
source: arxiv
url: https://arxiv.org/abs/2606.13497v1
published_at: '2026-06-11T15:46:28'
authors:
- Nils Blank
- Paul Mattes
- Maximilian Xiling Li
- Jakub Suliga
- Thomas Roth
- Moritz Reuss
- Pankhuri Vanjani
- Rudolf Lioutikov
topics:
- robot-learning
- spatial-annotation
- reliability-scoring
- embodied-vlm
- data-filtering
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# SPARC: Reliable Spatial Annotations from Robot Demonstrations at Scale

## Summary
## 摘要
SPARC 解决了机器人演示的空间标注自动生成中的可靠性问题，让机器人学习可以使用更多数据，而不会被噪声标签拖累。它之所以重要，是因为具身策略和具身基础模型需要物体位置、轨迹和阶段标签，但仅靠检测器置信度在杂乱场景里经常会选错对象。

## 问题
- 机器人演示需要物体框、轨迹和操作阶段这类结构化标签，但人工标注成本很高。
- 现有自动标注流水线把检测器置信度当作主要质量信号，而这个信号不能反映被检测到的对象是不是机器人实际操作的对象。
- 在杂乱、遮挡和双手操作场景中，这些流水线会在质量和覆盖率之间取舍：保留噪声标签，或者丢掉有用数据。

## 方法
- SPARC 先用夹爪阶段检测和语言解析，把一次演示切成以对象为中心的交互片段。
- 对每个候选对象，它先用 LLMDet 提议区域，再用 SAM2 生成掩码，用 AllTracker 跟踪，并用 MoGe-2 把轨迹提升到 3D。
- 它用交互证据给每个候选对象打分：抓取阶段的运动、与夹爪的 3D 距离，以及与机器人身体重叠的惩罚项。
- 得分最高的候选对象成为标注结果，一个可靠性阈值控制筛选严格程度。
- 论文还引入了 IA-Bench，这是一个基准，包含 12 种具身形态、1,748 次演示中的人工标注交互对象起始框和目标框。

## 结果
- 在 IA-Bench 上，SPARC 的交互对象定位准确率达到 80.2%，检测置信度基线为 58.1%。
- 在 90% 精度运行点，它保留了 77.6% 的覆盖率；最强的轨迹过滤基线只有 33.1% 覆盖率，检测器置信度只有 0.2% 覆盖率。
- 它的选择性预测分数是已报告结果中最好的：AURC 为 0.056，E-AURC 为 0.035。
- 在 95% 精度目标下，SPARC 保留了 58% 的样本，而最强的轨迹过滤方法是 20%。
- 用大约 511K 个 SPARC 生成的 VQA 对训练 Qwen3.5-4B，在 IA Bench 上得到 79.1，在 Where2Place 上得到 71.0，在 VA Bench-P 上得到 65.7，指向类基准的平均分为 69.6；这超过了人工标注的 EO-1.5M 混合数据在已报告空间定位平均分上的结果（69.6 对 62.6）。
- 在真实世界的杂乱操作场景中，用 SPARC 标注训练的策略优于用检测器标注数据训练的基线，但摘要没有给出具体策略分数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.13497v1](https://arxiv.org/abs/2606.13497v1)
