---
source: arxiv
url: http://arxiv.org/abs/2603.29067v1
published_at: '2026-03-30T23:10:19'
authors:
- Pengtao Zhao
- Boyang Yang
- Bach Le
- Feng Liu
- Haoye Tian
topics:
- automated-program-repair
- repository-level-rag
- swe-bench
- code-generation
- fault-localization
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond Localization: Recoverable Headroom and Residual Frontier in Repository-Level RAG-APR

## Summary
## 摘要
这篇论文研究了当故障定位变得更强之后，仓库级自动程序修复还能从哪里继续提升。基于 SWE-bench Lite，论文发现 oracle 定位能帮助 Agentless、KGCompass 和 ExpeRepair，但修复缺口仍然很大；提示级上下文融合只能收回未解决前沿中的一小部分。

## 问题
- 仓库级 APR 论文常把更好的定位当作提升修复效果的主要路径，但端到端分数把定位、提示构造、补丁生成和验证混在一起了。
- 这让人很难判断，在已经知道正确文件和行号之后，真正限制性能的是什么。
- 这个问题很重要，因为下一步研究要先找准瓶颈：检索、证据打包、接口设计，还是补丁合成。

## 方法
- 论文在 **SWE-bench Lite（300 个实例）** 上做了一个受控研究，使用三个仓库级 RAG-APR 系统：**Agentless、KGCompass 和 ExpeRepair**。
- 它注入 **Oracle Localization**，把由 gold-patch 推导出的补丁前文件和行范围提供给每个系统，同时保留各系统自己的下游提示构造和修复流程。
- 它用 **Best-of-K** 测量剩余搜索空间，其中 **K = 10**，并在这个固定池内做理想选择。
- 它在两个固定接口下测试新增上下文，并配套控制条件：同 token 填充提示和同仓库 hard negative，用来区分有用证据和提示长度效应。
- 它还做了一个 **common-wrapper oracle check**，看 oracle 带来的提升有多依赖各系统自己的修复包装器和提示构造器。

## 结果
- **Oracle 定位提升了三个系统，但在原生流程里没有一个达到 50% 成功率。** Agentless 从 **84/300（28.0%）** 提升到 **121/300（40.3%）**；KGCompass 从 **88/300（29.3%）** 提升到 **129/300（43.0%）**；ExpeRepair 从 **98/300（32.7%）** 提升到 **117/300（39.0%）**。
- **完成率在 oracle 定位下也上升了**：Agentless **84.7% -> 99.0%**，KGCompass **90.0% -> 98.7%**，ExpeRepair **92.0% -> 98.0%**。论文指出，总成功增益中有 **61.6% 到 79.3%** 来自已完成运行中的通过率提高，而不只是更多运行完成。
- **成对增益为正，但不是单调的。** 只看 oracle、对比只看 baseline 的胜利数分别是：Agentless **46/9**，KGCompass **54/13**，ExpeRepair **43/24**。报告的成对风险差分别是 **+12.3 个百分点**、**+13.7 个百分点** 和 **+6.3 个百分点**。
- **用 GPT-4.1 做的 backbone 检查显示出同样的模式。** Agentless 在 oracle 定位下从 **74/300** 提升到 **109/300**，KGCompass 从 **55/300** 提升到 **126/300**；成对胜负分别是 **40/5** 和 **78/7**。
- **包装器选择对 Agentless 的结果影响很大。** 在共享包装器检查中，Agentless 在共享 oracle 下从 **35.7%** 变到 **37.0%**，但在共享 builder oracle 下达到 **51.0%**。KGCompass 为 **17.0% -> 50.3% -> 51.0%**，ExpeRepair 为 **40.3% -> 51.3% -> 51.0%**。
- 摘要写明，**Best-of-K 头部空间存在，但很快就饱和了**，而且**最好的固定新增上下文探针只比原生三个系统的 Solved@10 并集多解出 6 个实例**。摘录里没有完整的 RQ2-RQ4 表格，所以这里看不到更细的搜索饱和和上下文探针定量结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.29067v1](http://arxiv.org/abs/2603.29067v1)
