---
source: arxiv
url: http://arxiv.org/abs/2603.29929v1
published_at: '2026-03-31T16:02:49'
authors:
- Serkan Kirbas
- Federica Sarro
- David Williams
topics:
- bayesian-networks
- developer-experience
- software-delivery
- causal-modeling
- engineering-analytics
relevance_score: 0.68
run_id: materialize-outputs
language_code: zh-CN
---

# BayesInsights: Modelling Software Delivery and Developer Experience with Bayesian Networks at Bloomberg

## Summary
## 概要
BayesInsights 是 Bloomberg 的内部工具，用贝叶斯网络把软件交付指标和开发者体验因素连接起来，并允许用户基于这些关系做 what-if 分析。论文说明了 Bloomberg 如何基于问卷数据、文献、专家输入和结构学习算法构建这些网络，并用高级从业者对工具进行测试。

## 问题
- 工程仪表盘会显示 DORA 指标和开发者问卷分数等指标，但它们无法解释某个指标为什么变化，也无法说明这种变化可能影响哪些其他指标。
- 软件交付和开发者体验数据里有很多混杂因素，基于问卷的软件工程数据也有噪声，因此简单的相关性视图或只靠数据的因果发现很容易得出误导性结论。
- 这很重要，因为团队需要一种方法来找出可能的根本原因，分析取舍，并基于更可靠的证据选择工程改进项。

## 方法
- Bloomberg 构建了两个贝叶斯网络：一个用于软件交付表现，另一个用于开发者体验；网络节点映射到内部问卷问题和交付因素。
- 网络结构来自一个混合流程：先用 DORA 和既有文献建立初始因果图，再由 8 名 DevX 专家组成的专家问卷对候选连接打分，并用 HC 和 PC 结构学习算法加上 bootstrap 检查做额外验证。
- 在专家问卷中，24 个可能的关系按加权分数进行评估；得分低于 0.70 的连接被删除。这个过程移除了 2 个关系，并新增了 3 个。
- 最终模型采用了经专家修正的结构，因为与 HC 和 PC 相比，它们的 BIC 最好。之后，条件概率表基于一份包含 20 个问题、超过 2,000 份回复的内部问卷进行估计，并在稀疏情形下使用 BDeu 平滑。
- 该工具通过一个基于 Django 的客户端-服务器应用提供这些网络，用户可以在节点上点击证据，并实时看到更新后的概率分布。

## 结果
- 性能测试报告单次推理请求的**平均延迟为 24 ms**。
- 在**50 个并发用户**下，响应时间中位数仍保持在**40 ms 以下**，作者认为这足以支持实时交互使用。
- 在用户评估中，**28** 名高级从业者参加了焦点小组，**24** 人完成了问卷。
- **95.8%** 的受访者表示，该工具有助于识别团队或组织层面的交付挑战。
- **75%** 认为输出结果易于理解，**83.3%** 表示他们清楚理解了指标变化如何通过模型传播，**70.9%** 对输出结果表示有信心。
- **79.2%** 表示他们会使用或推荐 BayesInsights；**62.5%** 认为它对管理层决策有价值，**62.5%** 认为它适合 what-if 分析，**50%** 认为它适合根因识别，**37.5%** 认为它适合审查团队实践。该工具目前处于早期访问阶段，已向**7 个工程团队**开放。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.29929v1](http://arxiv.org/abs/2603.29929v1)
