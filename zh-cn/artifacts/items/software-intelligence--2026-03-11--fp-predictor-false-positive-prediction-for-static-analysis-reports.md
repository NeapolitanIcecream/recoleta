---
source: arxiv
url: http://arxiv.org/abs/2603.10558v1
published_at: '2026-03-11T09:05:39'
authors:
- Tom Ohlmer
- Michael Schlichtig
- Eric Bodden
topics:
- static-analysis
- false-positive-prediction
- graph-neural-network
- code-property-graph
- software-security
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# FP-Predictor - False Positive Prediction for Static Analysis Reports

## Summary
该论文提出 **FP-Predictor**，用图卷积网络在静态应用安全测试（SAST）报告层面预测“真阳性/假阳性”，以减少开发者处理误报的成本。核心思想是把被报告代码片段转成代码属性图，再让模型学习代码结构与语义来判断该告警是否可信。

## Problem
- SAST 工具虽能自动发现潜在漏洞，但**假阳性很多**，会浪费开发者排查时间、拖慢修复真实漏洞，并削弱对自动化安全分析的信任。
- 传统基于规则/模式匹配的方法，难以捕捉决定“报告是否真的危险”的复杂代码结构、控制流与数据依赖。
- 论文聚焦于**Java 加密 API 误用**场景，尤其是如何对已有静态分析告警做后处理筛选，而不是直接从代码做漏洞检测。

## Approach
- 将每条 SAST 告警对应的方法代码构造成 **Code Property Graph (CPG)**，融合 **AST、CFG、PDG** 三种程序视图，表示语法、控制流和数据依赖关系。
- 使用 **GCN** 对 CPG 做图学习，输出一个 \[0,1\] 分数；文中用 **0.8 阈值**，高于阈值判为假阳性，否则判为真阳性。
- 每个图节点包含三类特征：**Jimple 语句的 Word2Vec 向量**、**节点类型 one-hot**、以及是否为**违规节点标记**。
- 在 **CamBenchCAP** 上训练与测试（80/20 划分），再迁移到 **CryptoAPI-Bench** 上评估泛化；输入告警来自 **CogniCrypt 5.0.2**。
- 机制上可以简单理解为：把“告警附近的代码上下文”变成一张图，让模型学习“这类结构通常是真漏洞还是误报”。

## Results
- 在 **CamBenchCAP** 上，使用 **80/20 train-test split**，模型在测试集上报告 **100% accuracy**；作者同时承认该数据集仅有 **431** 个标注样本，且较为结构化/合成，可能高估泛化能力。
- 在 **CryptoAPI-Bench** 上，自动评估时：对 **91** 个真实漏洞告警，正确识别 **89/91** 为真阳性，真阳性侧准确率约 **97.8%**；对 **27** 个安全样例触发的误报，仅识别 **1/27** 为假阳性，假阳性侧准确率约 **3.7%**。
- 经过人工复核，作者认为最初 **26** 个“误分类”中有 **22/26** 实际包含真实安全问题或不良加密实践，因此假阳性侧“有效准确率”可从 **1/27 (3.7%)** 提升到 **23/27 (85.2%)**。
- 基于上述人工重评，论文声称整体准确率可达 **96.6%**；若对 **3** 个“有争议但未改标签”的 bad practice 案例不调整真值，则整体准确率为 **94.1%**。
- 论文还给出训练成本：在 **Intel i7-11700K + RTX 4090 + 64GB RAM** 的 PC 上，模型训练约 **5 分钟**。
- 主要局限是当前 CPG **缺少跨过程/跨类连接**，对含 `if` 等复杂控制流或跨方法依赖的场景更难；作者计划加入 **call graph** 和图可解释性方法。

## Link
- [http://arxiv.org/abs/2603.10558v1](http://arxiv.org/abs/2603.10558v1)
