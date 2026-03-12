---
source: arxiv
url: http://arxiv.org/abs/2603.01814v1
published_at: '2026-03-02T12:50:40'
authors:
- Mingwei Liu
- Zhenxi Chen
- Zheng Pei
- Zihao Wang
- Yanlin Wang
- Zibin Zheng
topics:
- repository-level-code-generation
- architecture-aware-retrieval
- multi-design-generation
- change-impact-analysis
- llm-software-engineering
relevance_score: 0.96
run_id: materialize-outputs
---

# Architecture-Aware Multi-Design Generation for Repository-Level Feature Addition

## Summary
RAIM面向仓库级新功能添加，解决LLM在大型代码库中“看不清架构、只走单一路径改代码”的问题。它通过架构感知定位、多方案生成和影响分析选优，在NoCode-bench Verified上取得了新的SOTA。

## Problem
- 论文解决的是**仓库级 feature addition**：根据文档/规格变更，在整个代码库中自动实现新功能，而不是只修单个函数或单个bug。
- 这很重要，因为新功能添加需要跨文件理解系统架构、找到正确插入点，并避免破坏旧功能；文中还指出约**60%**的软件维护成本用于功能添加而非缺陷修复。
- 现有方法的问题是：对仓库结构“架构盲”、常把代码库当非结构化文本检索；同时采用贪心式单路径补丁生成，缺少系统性的改动影响评估，容易引入回归。

## Approach
- RAIM先构建**仓库级代码图**，把文件、类、函数及其 `imports` / `calls` / `extends` 等关系连起来，用多轮搜索先做文件定位，再做函数定位，从而找到分散的跨文件修改点。
- 在函数定位中，它结合**LLM语义判断**和**embedding检索**：先从候选文件中找相关函数，再沿代码图邻居多轮扩展与重排，逐步缩小到真正相关的编辑位置。
- 它不直接生成一个补丁，而是先让模型提出**多个实现设计（multi-design）**，每个设计描述要修改/创建什么目标以及改动意图，再分别生成对应补丁，扩大解空间、减少陷入局部最优。
- 最后用**impact-aware patch selection**选最优补丁：同时做静态结构影响分析、相关回归测试分析，以及新功能测试分析，再从相关性、代码质量、上下游安全性和回归安全性等维度综合打分。

## Results
- 在 **NoCode-bench Verified** 上，RAIM取得 **39.47% success rate**，成为新的SOTA；相对最强基线 **Agentless** 提升 **36.34%**。
- 使用开源模型 **DeepSeek-v3.2** 时，RAIM仍达到 **34.21% success rate**，论文声称这超过了某些使用领先闭源模型的基线系统。
- 论文称RAIM在 **7 个LLMs** 上表现出稳定泛化，整体性能增益范围为 **9.7%–221.4%**。
- 在复杂**跨文件修改任务**上，RAIM报告了 **191.7% relative improvement**，说明其架构感知定位和多方案机制对跨模块依赖特别有效。
- 消融研究的定性结论是：**multi-design generation** 和 **impact validation** 是关键模块，能更好处理复杂依赖并减少代码错误；摘录中未给出更细的消融数值。

## Link
- [http://arxiv.org/abs/2603.01814v1](http://arxiv.org/abs/2603.01814v1)
