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
- software-engineering
- architecture-aware-retrieval
- multi-design-generation
- impact-analysis
- llm-code-agents
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# Architecture-Aware Multi-Design Generation for Repository-Level Feature Addition

## Summary
RAIM 是一个面向仓库级新功能添加的代码生成框架，目标是在跨文件、跨模块修改时保持架构一致性并减少回归。它通过“架构感知定位 + 多设计生成 + 影响分析筛选”提升了 LLM 在复杂代码库演化任务上的成功率。

## Problem
- 解决的是**仓库级新功能添加**：根据文档或需求变更，在现有大型代码库中自动生成跨文件补丁，而不是只修单个函数或单个 bug。
- 这很重要，因为真实软件维护里功能新增占很大比例；任务需要理解全局架构、依赖关系和正确插入点，否则容易破坏旧功能。
- 现有方法主要问题是**架构盲**和**单路径贪心生成**：把仓库当无结构文本检索，且往往接受第一个看似可行的补丁，缺少系统性的回归与影响评估。

## Approach
- 先构建**仓库级代码图**，表示文件、类、函数及其 `imports`、`calls`、`extends` 等关系，用多轮搜索做文件级和函数级定位，找出真正相关的修改点。
- 在函数定位中，结合 **LLM 语义判断** 与 **embedding 检索**：先从特征描述和文件骨架找候选，再沿代码图邻居继续迭代检索，最后由 LLM 重排筛出最相关函数。
- 不直接生成单个补丁，而是先让模型提出多个**实现设计方案**，每个方案明确修改/创建哪些目标，以及高层修改逻辑，从而扩大解空间。
- 针对每个设计独立定位行级编辑位置并生成候选补丁，再做**影响感知选择**：结合静态代码子图分析、回归测试分析和新功能测试分析，对补丁在相关性、代码质量、上下游安全和回归安全等维度打分并选最优。

## Results
- 在 **NoCode-bench Verified** 上，RAIM 取得 **39.47% success rate**，论文称为该任务新的 **SOTA**。
- 相比最强基线 **Agentless**，RAIM 达到 **36.34% 相对提升**。
- 使用开源模型 **DeepSeek-v3.2** 时，RAIM 仍达到 **34.21% success rate**，并且论文声称其超过了一些由领先闭源模型驱动的基线系统。
- 方法在 **7 个 LLM** 上表现出泛化性，报告的性能增益范围为 **9.7%–221.4%**。
- 在复杂**跨文件修改任务**上，论文报告 **191.7% 相对提升**，说明架构感知定位和多设计筛选对依赖复杂场景尤其有效。
- 消融研究的定性结论是：**multi-design generation** 和 **impact validation** 是关键模块；摘录中未给出更细的消融数值。

## Link
- [http://arxiv.org/abs/2603.01814v1](http://arxiv.org/abs/2603.01814v1)
