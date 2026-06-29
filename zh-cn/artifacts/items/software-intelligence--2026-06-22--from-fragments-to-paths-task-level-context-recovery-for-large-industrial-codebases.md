---
source: arxiv
url: https://arxiv.org/abs/2606.22906v1
published_at: '2026-06-22T06:44:51'
authors:
- Jiawei He
- Weisong Sun
- Mengyu Shi
- Jie Jia
- Tong Bian
- Xikai Yang
- Dong Sun
topics:
- code-intelligence
- repository-understanding
- software-agents
- context-retrieval
- automated-software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# From Fragments to Paths: Task-Level Context Recovery for Large Industrial Codebases

## Summary
## 摘要
DeepDiscovery 通过先找到可靠的任务锚点，再沿代码、配置、测试和组织关系扩展，在大型代码库中恢复任务级上下文。论文称，它在工业仓库中能更好地恢复相关文件，并在 SWE-bench Verified 上取得更高的解决率。

## 问题
- LLM 编码系统常常只检索局部代码片段，但仓库级任务需要跨接口、业务逻辑、配置、测试和依赖关系连接文件。
- 大型工业仓库变化频繁，预构建向量索引或静态图可能过时，并增加维护成本。
- 缺少桥接文件会降低自动化编码成功率，例如注册文件、依赖注入文件或测试到实现的关联文件。

## 方法
- DeepDiscovery 使用两阶段 Location-Inference 工作流：Location 找到一小组高置信度任务锚点，Inference 从这些锚点扩展，以恢复更完整的实现路径。
- Location 阶段用语义和词法匹配、压缩后的结构摘要、规则模板匹配，以及按任务条件设定的工件角色先验来为候选文件打分。
- Inference 阶段在多关系仓库图上扩展，覆盖显式依赖、配置到代码绑定等隐式链接，以及文件夹和模块邻近等组织链接。
- 感知预算的优先级分数按估计收益除以成本来选择扩展动作，默认设置为 8 个锚点、0.15 的扩展停止阈值，以及 0.62 的全文提升阈值。
- 最终上下文采用元数据优先的方式：大多数被选实体保留紧凑元数据，可能被修改或高价值文件则提供全文。

## 结果
- 在 27 个中等规模任务和 135 个手工标注的黄金相关文件上，DeepDiscovery 报告的文件恢复质量优于五个基线：DeepWiki、CodeWiki、RAG、GraphRAG 和 AST+GraphRAG。
- 工业仓库设置覆盖 267 万行代码和超过 25,000 个文件。
- 在组织内部工业评估中，DeepDiscovery 在 27 个中等规模任务上，使多个 AI 编码系统的 Full Recall Rate 提高 2.5 到 7.4 个百分点。
- 在 40 个大型子项目工业任务上，它使多个 AI 编码系统的 Full Recall Rate 提高 1.6 到 9.2 个百分点。
- 在 SWE-bench Verified 上，配备 DeepDiscovery 的系统达到 78.6% Solve Rate，比对应基线高 8.2 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.22906v1](https://arxiv.org/abs/2606.22906v1)
