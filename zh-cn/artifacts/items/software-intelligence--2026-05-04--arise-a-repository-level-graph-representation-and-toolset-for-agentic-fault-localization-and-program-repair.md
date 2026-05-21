---
source: arxiv
url: https://arxiv.org/abs/2605.03117v1
published_at: '2026-05-04T19:59:23'
authors:
- Shahd Seddik
- Fatemeh Fard
topics:
- software-engineering-agents
- automated-program-repair
- fault-localization
- program-analysis
- code-graphs
- data-flow-slicing
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# ARISE: A Repository-level Graph Representation and Toolset for Agentic Fault Localization and Program Repair

## Summary
## 摘要
ARISE 为 LLM 修复代理加入了带有语句级 def-use 边的仓库图。在 SWE-bench Lite 上，它提升了细粒度定位能力，并让 Pass@1 高于 SWE-agent。

## 问题
- 仓库级修复代理必须先找到正确的文件、函数和行，才能修补 bug。
- 现有图工具大多跟踪文件、类、函数、导入、调用和引用；它们缺少函数内部变量值流动的信息。
- 这一点很关键，因为行级和函数级定位是 SWE-bench 类修复任务的主要失败点。

## 方法
- ARISE 为 Python 仓库构建一个类型化图，包含 Directory、Module、Class、Function、Method 和 Statement 节点。
- 它加入 Contains、Imports、Calls、Inherits，以及过程内 DataflowDefUse/DataflowUseDef 边。
- 数据流遍历会扫描每个函数体，记录顶层语句，找到变量定义和使用，并把每个使用连接到同一函数中此前最近的定义。
- 代理获得一个三层 API：结构导航、数据流切片和上下文打包。主工具会针对选定变量和语句返回后向、前向或双向切片。
- 评测在 SWE-bench Lite 上使用带有 Qwen2.5-Coder-32B-Instruct 的 SWE-agent。

## 结果
- SWE-bench Lite 包含来自 11 个 Python 仓库的 300 个真实 GitHub issue。
- 相比未修改的 SWE-agent，ARISE 将 Function Recall@1 提高了 17.0 个点。
- 相比同一基线，ARISE 将 Line Recall@1 提高了 15.0 个点。
- ARISE 达到 22.0% Pass@1，修复 66/300 个 issue，比 SWE-agent 高 4.7 个百分点。这意味着基线大约修复了 52/300 个 issue，即 17.3% Pass@1。
- 消融实验将增益归因于数据流图；仅改变工具 schema 的条件没有达到同等效果。
- 论文报告称，Qwen2.5-Coder-32B-Instruct 可以直接使用结构化切片输出，不需要自然语言摘要层。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.03117v1](https://arxiv.org/abs/2605.03117v1)
