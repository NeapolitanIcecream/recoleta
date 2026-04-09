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
## 概要
本文研究了在故障定位显著增强之后，仓库级自动程序修复的表现。在 SWE-bench Lite 上，论文发现 oracle localization 能提升 Agentless、KGCompass 和 ExpeRepair，但修复能力仍有较大缺口，而基于提示词的上下文融合只补回了未解决部分中的一小部分。

## 问题
- 仓库级 APR 论文常把更好的定位当作提升修复效果的主要途径，但端到端分数同时混合了定位、提示构造、补丁生成和验证。
- 这使得人在已经知道正确文件和代码行之后，仍然很难判断性能到底受什么限制。
- 这很重要，因为下一步研究取决于瓶颈在哪里：检索、证据组织、接口设计，还是补丁合成。

## 方法
- 论文在 **SWE-bench Lite（300 个实例）** 上做了一个受控研究，测试三个仓库级 RAG-APR 系统：**Agentless、KGCompass 和 ExpeRepair**。
- 它通过向每个系统提供从 gold patch 导出的修复前文件和代码行区间，注入 **Oracle Localization**，同时保留各系统原有的下游提示构造和修复流程。
- 它用 **Best-of-K** 测量剩余的搜索空间，设置 **K = 10** 个采样补丁候选，并在这个固定候选池内做理想选择。
- 它在两个固定接口下测试附加上下文，并设置控制条件：相同 token 数的 filler prompts，以及同一仓库内的 hard negatives，以区分真正有用的证据和提示长度带来的影响。
- 它还运行了一个 **common-wrapper oracle check**，用来判断 oracle 带来的提升有多少取决于各系统的修复 wrapper 和 prompt builder。

## 结果
- **Oracle Localization 提升了全部三个系统，但在原生流程中没有一个达到 50% 的成功率。** Agentless 从 **84/300 (28.0%)** 提高到 **121/300 (40.3%)**；KGCompass 从 **88/300 (29.3%)** 提高到 **129/300 (43.0%)**；ExpeRepair 从 **98/300 (32.7%)** 提高到 **117/300 (39.0%)**。
- **完成率也在 oracle localization 下上升。** Agentless **84.7% -> 99.0%**，KGCompass **90.0% -> 98.7%**，ExpeRepair **92.0% -> 98.0%**。论文指出，总成功增益中有 **61.6% 到 79.3%** 来自已完成运行中更高的通过率，而不只是因为完成的运行更多。
- **配对增益为正，但不是单调上升。** Oracle-only wins 相对 baseline-only wins 分别是 Agentless **46/9**、KGCompass **54/13**、ExpeRepair **43/24**。论文报告的配对风险差分别为 **+12.3 points**、**+13.7 points** 和 **+6.3 points**。
- **使用 GPT-4.1 的 backbone check 显示出同样的模式。** Agentless 在 oracle localization 下从 **74/300** 提高到 **109/300**，KGCompass 从 **55/300** 提高到 **126/300**；配对 wins/losses 分别是 **40/5** 和 **78/7**。
- **对 Agentless 来说，wrapper 的选择会明显改变结果。** 在共享 wrapper 检查中，Agentless 在 shared oracle 下从 **35.7%** 变为 **37.0%**，但在 shared-builder oracle 下达到 **51.0%**。KGCompass 为 **17.0% -> 50.3% -> 51.0%**，ExpeRepair 为 **40.3% -> 51.3% -> 51.0%**。
- 摘要指出，**Best-of-K 仍有提升空间，但很快饱和**，并且 **最佳固定附加上下文 probe** 相比原生三系统 **Solved@10 union** 也只多解决了 **6 个实例**。给出的摘录不包含完整的 RQ2-RQ4 表格，因此这里没有关于搜索饱和和上下文 probe 的更细量化结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.29067v1](http://arxiv.org/abs/2603.29067v1)
