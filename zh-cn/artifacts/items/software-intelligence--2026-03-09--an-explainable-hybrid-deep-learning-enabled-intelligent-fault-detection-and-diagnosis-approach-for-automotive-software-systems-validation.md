---
source: arxiv
url: http://arxiv.org/abs/2603.08165v1
published_at: '2026-03-09T09:46:28'
authors:
- Mohammad Abboush
- Ehab Ghannoum
- Andreas Rausch
topics:
- automotive-software
- fault-diagnosis
- explainable-ai
- cnn-gru
- hardware-in-the-loop
relevance_score: 0.54
run_id: materialize-outputs
language_code: zh-CN
---

# An explainable hybrid deep learning-enabled intelligent fault detection and diagnosis approach for automotive software systems validation

## Summary
本文提出一种面向汽车软件系统实时验证的可解释故障检测与诊断方法，把混合深度学习与XAI结合起来，用于从HIL测试记录中发现、识别并定位故障。其核心价值在于把原本难以信任和优化的黑盒诊断模型，转化为更可解释、可裁剪的白盒式工作流。

## Problem
- 解决的问题是：如何在汽车软件系统（ASSs）实时验证阶段，自动分析海量HIL测试记录，完成故障检测、故障类型识别和故障位置定位，且要支持**单一故障与并发故障**。
- 这很重要，因为汽车系统验证受ISO 26262等安全要求约束，传统规则/工具难以高效处理复杂时序数据，也难以做根因分析、区分安全与关键故障。
- 现有DL式FDD虽有效，但通常是黑盒；缺乏可解释性会降低工程师信任，增加模型优化与部署成本，尤其不利于安全关键实时应用。

## Approach
- 核心方法是一个**1dCNN-GRU混合模型**：1dCNN先从时间序列里抓局部模式，GRU再建模时间依赖，最后用全连接层输出故障类别或故障位置；可把它理解为“先找信号片段特征，再理解它们随时间如何演变”。
- 数据来自**HIL实时仿真**与虚拟试驾，包含用户驾驶行为、高保真汽车系统模型，以及通过CAN总线注入的传感器/执行器故障；覆盖健康、单故障和并发故障场景。
- 预处理流程包括去噪、去异常/冗余、归一化、重采样与窗口切分，并针对类别不平衡使用**RUS、Class Weights、SMOTE**等方法。
- 为了让模型可解释，作者比较了四种XAI技术：**Integrated Gradients、DeepLIFT、Gradient SHAP、DeepLIFT SHAP**，用它们识别重要变量、支持根因分析，并进一步做特征筛选与模型简化。
- 文中还给出一个白盒化版本：根据解释结果保留关键变量，目标是在尽量保持诊断能力的同时，降低复杂度和计算成本。

## Results
- 文摘与节选明确声称：该方法在**故障类型诊断与故障位置定位**上优于现有state-of-the-art模型，但当前提供的文本**未给出具体精度、F1、召回率或对比基线数值**。
- 已给出的可量化实现细节包括：故障类型分类模型（FTCM）输出为**7类**，总参数量约**199,335**；模型由多层Conv1d/BatchNorm/ReLU/MaxPool、**2层GRU**和全连接层组成。
- 论文宣称XAI集成后可得到**高性能、低计算成本**的白盒DL模型，并通过识别显著变量来提升性能、效率并降低复杂度，但节选中**没有提供这些提升的百分比或绝对值**。
- 实验数据基于**HIL实时仿真数据集**，考虑用户行为与高保真ASS模型，且包含**单故障与并发故障**；作者还比较了四种XAI方法的计算成本与效果，但当前文本未提供具体排序数字。
- 作者宣称据其所知，这是**首个**在ASSs实时验证阶段，将XAI与混合DL式FDD结合并显式考虑并发故障的研究。

## Link
- [http://arxiv.org/abs/2603.08165v1](http://arxiv.org/abs/2603.08165v1)
