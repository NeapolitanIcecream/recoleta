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
## 摘要
BayesInsights 是 Bloomberg 的一个内部工具，它用贝叶斯网络把软件交付指标和开发者体验因素连接起来，并让用户对这些关系做假设分析。论文说明了 Bloomberg 如何结合调查数据、文献、专家输入和结构学习算法构建这些网络，然后用资深从业者测试该工具。

## 问题
- 工程仪表板会显示 DORA 和开发者调查分数等指标，但它们不能解释某个指标为什么变化，也不能说明一次变化会影响哪些其他指标。
- 软件交付和开发者体验数据里有很多混杂因素，而且基于调查的软件工程数据噪声很大，所以只看相关性或只靠数据做因果发现，可能会得出误导性的结论。
- 这很重要，因为团队需要一种方法来找出可能的根因，分析取舍，并用更好的证据选择工程改进方案。

## 方法
- Bloomberg 构建了两个贝叶斯网络：一个用于软件交付绩效，一个用于开发者体验，节点对应内部调查问题和交付因素。
- 网络结构来自一个混合流程：先用 DORA 和既有文献画出初始因果图，再请 8 名 DevX 专家做问卷，对候选链接打分，同时用 HC 和 PC 结构学习算法并结合自助法检查做额外验证。
- 在专家问卷中，24 种可能关系按加权分数评估；得分低于 0.70 的链接被删除。这样删掉了 2 个关系，新增了 3 个关系。
- 最终模型采用专家修订后的结构，因为它们的 BIC 优于 HC 和 PC。随后用一份内部调查估计条件概率表，这份调查有 20 个问题，收到了 2,000 多份回答；在稀疏情况中使用了 BDeu 平滑。
- 该工具通过一个基于 Django 的客户端-服务器应用提供这些网络，用户可以点击节点上的证据，并实时看到更新后的概率分布。

## 结果
- 性能测试报告显示，单次推理请求的平均延迟为 **24 毫秒**。
- 在 **50 个并发用户** 下，中位响应时间保持在 **40 毫秒以下**，作者认为这足以支持实时交互使用。
- 在用户评估中，**28** 名资深从业者参加了焦点小组，**24** 人完成了问卷。
- **95.8%** 的受访者认为该工具有助于识别团队或组织层面的交付问题。
- **75%** 认为输出容易解读，**83.3%** 表示能清楚理解指标变化如何在模型中传播，**70.9%** 对输出有信心。
- **79.2%** 表示会使用或推荐 BayesInsights；**62.5%** 认为它对领导层决策有价值，**62.5%** 认为它适合做假设分析，**50%** 认为它有助于识别根因，**37.5%** 认为它适合复核团队实践。该工具目前处于早期访问阶段，已向 **7 个工程团队** 开放。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.29929v1](http://arxiv.org/abs/2603.29929v1)
