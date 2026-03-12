---
source: arxiv
url: http://arxiv.org/abs/2603.05637v1
published_at: '2026-03-05T19:47:26'
authors:
- Mina Taraghi
- Mohammad Mehdi Morovati
- Foutse Khomh
topics:
- model-context-protocol
- software-testing
- bug-taxonomy
- llm-software
- empirical-software-engineering
relevance_score: 0.9
run_id: materialize-outputs
---

# Real Faults in Model Context Protocol (MCP) Software: a Comprehensive Taxonomy

## Summary
本文针对 MCP（Model Context Protocol）服务器中的真实缺陷，提出了首个大规模、基于实证数据的故障分类体系。其意义在于帮助构建更可靠、更安全的 LLM 工具调用与外部资源集成软件。

## Problem
- 现有研究讨论过一般性的 LLM 软件缺陷，但**缺少对 MCP 软件真实故障的系统性认识**。
- MCP 正在成为 LLM 与工具、资源、宿主应用之间的标准接口，因此其故障会直接影响**可靠性、安全性、鲁棒性和互操作性**。
- 若不了解 MCP 特有故障类型，就难以设计有针对性的测试、调试与工程实践，尤其在安全关键场景中影响更大。

## Approach
- 作者从 GitHub 上系统收集 MCP Python SDK 相关仓库：先找到 **13,555** 个候选仓库，经筛选后保留 **385** 个真实 MCP server 仓库。
- 从这些仓库提取 **30,795** 个 closed issues，过滤非英文后剩 **26,821** 个；再用 LLM 分类出 **3,591** 个 bug 相关问题，并去除 stale/duplicate/不可复现后得到 **3,282** 个有效 bug issues。
- 为聚焦 MCP 相关缺陷，作者先用 LLM 对 issue 标题、正文和评论做摘要，再用 **BERTopic + embedding + UMAP + KMeans** 聚类，将 **3,282** 个 bug issues 划分为 **101** 个簇。
- 在此基础上，人工检查并识别出 **407** 个 MCP 相关 issues，据此归纳出 **5 个高层故障类别**，并通过 MCP 从业者问卷验证这些类别是否完整、是否真实存在。
- 简单说，核心机制就是：**先大规模抓取真实 issue，再用 LLM 和聚类缩小范围，最后人工归纳并用从业者调查验证 taxonomy**。

## Results
- 论文声称提出了**首个**针对 MCP servers 的大规模真实故障 taxonomy，最终得到 **5 个高层故障类别**。
- 数据规模方面：从 **13,555** 个候选仓库筛到 **385** 个 MCP server 仓库；从 **30,795** 个 closed issues 缩减到 **26,821** 个英文 issues，再到 **3,282** 个精炼后的 bug issues；其中识别出 **407** 个 MCP 相关 issues。
- 在 issue 分类模型对比中，作者用 **40** 条人工标注样本评估多个 LLM：**GPT-4o-mini** 表现最好，达到 **Accuracy 0.77 / Precision-macro 0.78 / Recall-macro 0.82 / F1-macro 0.77**；对比 **GPT-4.1** 的 **0.74 / 0.76 / 0.81 / 0.75**，以及 **Llama3.1:8b** 的 **0.77 / 0.81 / 0.82 / 0.76**。
- 在摘要模型选择中，作者随机抽取 **15** 个 bug issues 比较摘要质量，**GPT-4.1-mini** 在 **10/15** 个样本上被评为最佳，优于 **GPT-4.1** 的 **3/15**，因此被选为全量摘要模型。
- 聚类阶段，作者将 issue 摘要嵌入为 **3,072 维**向量，经 UMAP 降至 **5 维**，并划分为 **101** 个聚类，以支持后续人工识别 MCP 相关故障。
- 关于最终效果，给定摘录**没有提供更细的定量结果**（例如 5 类故障各自占比、问卷样本量、严重度差异统计、与非 MCP 故障的显著性比较）。最强的具体结论是：**所有识别出的故障类别都在实践中出现，并且 MCP 特有故障与非 MCP 故障存在可区分特征**。

## Link
- [http://arxiv.org/abs/2603.05637v1](http://arxiv.org/abs/2603.05637v1)
