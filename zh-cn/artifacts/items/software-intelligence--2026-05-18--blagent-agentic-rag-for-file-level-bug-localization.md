---
source: arxiv
url: https://arxiv.org/abs/2605.17965v1
published_at: '2026-05-18T07:20:13'
authors:
- Md Afif Al Mamun
- Gias Uddin
topics:
- bug-localization
- agentic-rag
- code-intelligence
- automated-program-repair
- software-agents
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# BLAgent: Agentic RAG for File-Level Bug Localization

## Summary
## 摘要
BLAgent 是一个用于代码仓库中文件级漏洞定位的 agentic RAG 流水线。它先从 bug 报告中对可能出错的文件进行排序，再通过向修复系统提供更好的文件上下文来提升后续自动修复效果。

## 问题
- 文件级漏洞定位是调试、分诊、根因分析和自动程序修复中的瓶颈，因为一旦选错文件，后续步骤就会失效。
- SWE-bench 仓库平均有超过 11,000 个函数和 168,000 条语句，所以直接做语句级搜索对基于 LLM 的修复系统来说成本太高。
- 以往的 RAG 方法通常在较弱的代码切块上做静态检索，而基于图的 agent 方法往往成本较高，或者需要额外的模型训练。

## 方法
- BLAgent 用 AST 感知的切块来索引源文件，因此切块会对齐到函数、类或其他语法单元，而不是任意文本片段。
- 它在每个切块前加上相对文件路径，这有助于匹配提到模块、回溯信息或带包名前缀名称的 bug 报告。
- 它把每条 bug 报告改写成两个检索查询：一个结构查询，用于识别符和模块；一个行为查询，用于观察到的行为与预期行为。
- 它从这两个查询中检索候选文件，最多保留 15 个候选项，并按每个文件中最匹配的切块给文件排序。
- 它分两阶段重排候选项：先由 ReAct agent 给文件骨架打分，再用一次性 LLM 针对前 5 个文件，结合最相关的检索切块比较裁剪后的文件上下文。

## 结果
- 在 SWE-bench Lite 上，BLAgent 使用闭源模型时达到 86.7% 的 Top-1 准确率和 0.900 的 MRR。
- 使用开源模型时，它在 SWE-bench Lite 上达到 78.6% 的 Top-1 准确率和 0.851 的 MRR。
- 论文称，BLAgent 与 LocAgent 使用相同模型时，API 成本低 18 倍以上。
- 集成到开源 APR 系统 Agentless 后，BLAgent 将问题解决率提高了 20% 以上。
- 论文报告说，在多粒度定位流水线中去掉文件级定位后，Top-5 准确率下降了 94%，语句级 MAP 下降了 96%，这说明文件级定位很重要。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17965v1](https://arxiv.org/abs/2605.17965v1)
