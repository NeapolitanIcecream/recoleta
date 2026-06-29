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
ARISE 为一个 LLM 修复代理加入了带有语句级 def-use 边的仓库图。在 SWE-bench Lite 上，它提升了细粒度定位能力，并且让 Pass@1 高于 SWE-agent。

## 问题
- 仓库级修复代理必须先找到正确的文件、函数和代码行，才能修补缺陷。
- 现有图工具主要跟踪文件、类、函数、导入、调用和引用；它们看不到变量值在函数内部如何流动。
- 这很关键，因为行级和函数级定位是 SWE-bench 风格修复中的主要失败点。

## 方法
- ARISE 为 Python 仓库构建了一个带类型的图，包含 Directory、Module、Class、Function、Method 和 Statement 节点。
- 它加入了 Contains、Imports、Calls、Inherits，以及过程内的 DataflowDefUse/DataflowUseDef 边。
- 数据流过程会扫描每个函数体，记录顶层语句，找出变量定义和使用，并把每次使用连接到同一函数中最近的前一个定义。
- 代理获得了三层 API：结构导航、数据流切片和上下文打包。主工具会针对选定变量和语句返回后向、前向或双向切片。
- 评估在 SWE-bench Lite 上使用 Qwen2.5-Coder-32B-Instruct 作为 SWE-agent 的骨干模型。

## 结果
- SWE-bench Lite 包含来自 11 个 Python 仓库的 300 个真实 GitHub issue。
- 与未修改的 SWE-agent 相比，ARISE 将 Function Recall@1 提高了 17.0 个百分点。
- 与同一基线相比，ARISE 将 Line Recall@1 提高了 15.0 个百分点。
- ARISE 的 Pass@1 达到 22.0%，修复了 66/300 个问题，比 SWE-agent 高 4.7 个百分点。这意味着基线大约修复了 52/300 个问题，即 17.3% 的 Pass@1。
- 消融实验把提升归因于数据流图；仅有工具模式的条件无法达到同样效果。
- 论文报告称，Qwen2.5-Coder-32B-Instruct 可以直接使用结构化切片输出，不需要自然语言摘要层。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.03117v1](https://arxiv.org/abs/2605.03117v1)
