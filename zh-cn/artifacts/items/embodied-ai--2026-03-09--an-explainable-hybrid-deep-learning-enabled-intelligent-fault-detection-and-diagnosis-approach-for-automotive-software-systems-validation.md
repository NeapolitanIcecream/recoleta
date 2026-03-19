---
source: arxiv
url: http://arxiv.org/abs/2603.08165v1
published_at: '2026-03-09T09:46:28'
authors:
- Mohammad Abboush
- Ehab Ghannoum
- Andreas Rausch
topics:
- fault-diagnosis
- automotive-software
- explainable-ai
- cnn-gru
- hil-simulation
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# An explainable hybrid deep learning-enabled intelligent fault detection and diagnosis approach for automotive software systems validation

## Summary
本文提出一种面向汽车软件系统实时验证的可解释混合深度学习故障检测与诊断方法，将1dCNN-GRU与多种XAI技术结合，用于从HIL测试记录中检测、识别并定位故障。其核心卖点是把原本“黑盒”的诊断模型变成可解释、可优化的白盒版本，尤其面向单故障与并发故障场景。

## Problem
- 车载软件系统在HIL/实时验证阶段会产生大量复杂时序测试记录，人工或传统规则方法难以高效分析，且难以定位根因。
- 现有DL故障检测与诊断模型通常是黑盒，工程师难以理解“为什么这样判定”，这会降低在安全关键场景中的信任度，并增加模型优化成本。
- 并发故障、类别不平衡和高噪声数据进一步增加了故障识别与定位难度，而现有可解释FDD工作大多只关注单一故障。

## Approach
- 使用HIL实时仿真平台采集汽车软件系统测试数据，结合用户驾驶行为、虚拟试驾以及基于CAN总线的故障注入，构建健康、故障类型和故障位置数据集。
- 对时序数据做预处理，包括去噪、异常/冗余信息清理、归一化、分窗，以及针对类别不平衡采用RUS、Class Weights、SMOTE等重采样策略。
- 构建混合1dCNN-GRU模型：1dCNN负责从原始时间序列中提取局部模式，GRU负责建模时间依赖，最后用全连接层输出故障类别/位置预测；文中给出的故障类型分类模型参数量为199,335。
- 引入4种XAI方法——Integrated Gradients、DeepLIFT、Gradient SHAP、DeepLIFT SHAP——解释模型预测，识别关键变量，用于根因分析与特征筛选。
- 基于解释结果构建“白盒”精简模型，目标是在保持或提升诊断性能的同时降低计算成本与模型复杂度。

## Results
- 论文明确声称：在HIL实时仿真数据集上，所提方法在故障类型诊断与故障位置定位方面优于state-of-the-art模型，但当前摘录**未给出具体准确率、F1、AUC或相对提升百分比**。
- 论文给出的最具体可量化信息之一是：对4种XAI技术进行了比较，关注其计算开销与性能差异，但摘录中**没有提供具体数值结果**。
- 文中宣称该方法能够处理**单故障与并发故障**，并且适用于**类别不平衡数据**，这是相对现有很多只处理单故障方案的扩展。
- 论文声称通过XAI驱动的重要变量识别，可得到**低计算成本、低复杂度**的白盒DL模型，同时支持工程师进行根因分析；但摘录中**未提供压缩比例、推理时延或资源节省数字**。
- 可见的结构性数字包括：故障类型分类模型（FTCM）总参数量为**199,335**，最终输出为**7类**；这说明其模型规模相对适中，但这不是性能指标。

## Link
- [http://arxiv.org/abs/2603.08165v1](http://arxiv.org/abs/2603.08165v1)
