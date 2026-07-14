---
source: arxiv
url: https://arxiv.org/abs/2607.11046v1
published_at: '2026-07-13T03:18:22'
authors:
- Genevieve Caumartin
- Tse-Hsun
- Chen
- Diego Elias Costa
topics:
- code-retrieval
- bug-localization
- software-agents
- code-representation
- llm-ranking
- context-engineering
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Retrieval-Oriented Code Representations in Agentic Bug Localization

## Summary
## 摘要
论文研究仓库文件的文本表示如何影响软件代理进行文件级缺陷定位。角色感知摘要通常在准确率与成本之间取得最佳平衡，组合不同表示并使用 LLM 重排还能提高覆盖率。

## 问题
- 仓库级缺陷定位需要在数百或数千个候选文件中找出相关文件，代理才能生成或验证补丁。
- 原始源代码可能超出上下文限制，并增加令牌和检索成本；文件路径则缺少有用的语义信息。
- 研究在 Long Code Arena 和 SWE-bench Verified 上衡量表示选择对检索准确率、排序质量和表示占用的影响。

## 方法
- 比较五种文件表示：文件路径、原始源代码、角色感知摘要、详细技术摘要和合成缺陷报告摘要。
- 使用 BM25、稠密嵌入或 LLM 检索候选文件，然后通过倒数排名融合或 LLM 对候选文件重新排序。
- 使用 MAP 和 Hit@k 衡量定位效果，并通过基于令牌的表示占用和摘要生成 API 成本估算开销。
- 在 Agentless 文件定位流程中测试效果最好的方法。

## 结果
- 角色感知摘要相较文件路径表示最多将 Hit@5 提高 40%，同时表示占用比原始源代码小 10.4 至 20.9 倍。
- 对互补的 LLM 检索结果进行倒数排名融合后，Long Code Arena 上的 Hit@5 达到 89.3%，SWE-bench Verified 上达到 83.4%。
- 组合不同表示最多可将定位效果提高 31.9%，LLM 检索后排序最多可将结果提高 42.0%。
- 在 Agentless 案例研究中，角色感知摘要结合 LLM 排序达到 94% 的 Hit@6，比基线提高 4.7 个百分点。
- 论文没有发现一种表示能在所有模型、数据集和流程阶段都取得最佳效果；角色感知摘要整体上提供了最好的成本效益平衡，而原始源代码在成本大幅更高的情况下也可能取得良好效果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.11046v1](https://arxiv.org/abs/2607.11046v1)
