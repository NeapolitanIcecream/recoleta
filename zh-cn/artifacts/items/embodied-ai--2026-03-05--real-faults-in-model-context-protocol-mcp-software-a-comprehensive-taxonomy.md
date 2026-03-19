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
- github-mining
relevance_score: 0.07
run_id: materialize-outputs
language_code: zh-CN
---

# Real Faults in Model Context Protocol (MCP) Software: a Comprehensive Taxonomy

## Summary
本文系统研究了 MCP 服务器中的真实故障，提出了首个基于实证数据的故障分类体系。它通过大规模 GitHub issue 分析与从业者调研，帮助理解 MCP 软件中最常见、最关键的问题来源。

## Problem
- 论文要解决的问题是：**MCP（Model Context Protocol）软件里究竟会出现哪些真实故障，以及这些故障与普通软件故障有何不同**。
- 这很重要，因为 MCP 正在成为 LLM 与外部工具/资源交互的标准接口，而这类系统直接关系到**可靠性、安全性、鲁棒性与可测试性**。
- 现有研究讨论过一般 LLM 软件缺陷，但**此前没有专门针对 MCP 系统、尤其是 MCP server 的系统化故障分类研究**。

## Approach
- 作者从 GitHub 大规模收集 MCP Python SDK 相关仓库：最初找到 **13,555** 个仓库，经筛选后保留 **385** 个 MCP server 仓库。
- 从这些仓库中提取 **30,795** 个 closed issues，过滤非英文后剩 **26,821** 个，再用 LLM 识别 bug 类 issue，得到 **3,591** 个 bug；去除 stale/duplicate/non-reproducible 后保留 **3,282** 个有效 bug。
- 为聚焦 MCP 相关故障，作者先用 LLM 对 issue（标题、正文、评论）做摘要，再用 **BERTopic + embedding + UMAP + KMeans** 对 **3,282** 个 bug 聚类，形成 **101** 个簇。
- 作者随后人工检查聚类结果，识别出 **407 个 MCP-related issues**，并据此归纳出**5 个高层故障类别**，形成论文的 MCP 故障 taxonomy。
- 为验证分类体系的完整性与泛化性，作者还对 MCP 从业者进行了问卷调查，确认这些类别在实践中都真实存在，并分析了 MCP 故障与非 MCP 故障的差异特征。

## Results
- 论文的核心成果是提出了**首个大规模 MCP server 真实故障分类体系**，包含 **5 个高层 fault categories**；摘要未给出每类名称与占比。
- 数据规模上，研究基于 **385** 个仓库、**26,821** 个英文 closed issues、**3,282** 个精炼后的 bug issues，并最终识别出 **407** 个 MCP-related issues。
- 在 issue 分类模型选择上，作者比较了多个 LLM；**GPT-4o-mini** 在 40 个标注样本上表现最好，达到 **Accuracy 0.77 / Macro-F1 0.77**，略高于 **GPT-4.1 的 Accuracy 0.74 / Macro-F1 0.75**，也显著高于如 **Gemma3:4.3b 的 Macro-F1 0.50**。
- 在 issue 摘要模型选择上，**GPT-4.1-mini** 在 **15** 个样本中有 **10/15** 次被评为最佳，优于 **GPT-4.1 的 3/15**，因此被用于全量摘要生成。
- 从业者调查结果表明：**所有识别出的故障大类都在实际开发中出现**，且 MCP 故障与非 MCP 故障具有不同特征；但摘录文本**没有提供更细的定量调查数字**。
- 相比以往仅研究一般 LLM 软件缺陷的工作，本文声称的突破在于：**首次专门面向 MCP server 做大规模实证 taxonomy，并给出对测试、鲁棒性和安全工程有直接指导价值的故障画像**。

## Link
- [http://arxiv.org/abs/2603.05637v1](http://arxiv.org/abs/2603.05637v1)
