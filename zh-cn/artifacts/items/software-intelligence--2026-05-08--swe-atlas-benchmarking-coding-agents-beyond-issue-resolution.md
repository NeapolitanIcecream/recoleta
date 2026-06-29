---
source: arxiv
url: https://arxiv.org/abs/2605.08366v1
published_at: '2026-05-08T18:21:44'
authors:
- Mohit Raghavendra
- Soham Dan
- Miguel Romero Calvo
- Yannis Yiming He
- Johannes Baptist Mols
- Gautam Anand
- Cole McCollum
- Edgar Arakelyan
- Vijay Bharadwaj
- Andrew Park
- Jeff Da
- MohammadHossein Rezaei
- Bing Liu
- Brad Kenstler
- Yunzhong He
topics:
- coding-agents
- software-engineering-benchmark
- codebase-qa
- test-generation
- refactoring
- llm-evaluation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# SWE Atlas: Benchmarking Coding Agents Beyond Issue Resolution

## Summary
## 总结
SWE Atlas 是一个面向编码代理的 284 题基准，覆盖代码库问答、测试编写和重构，数据来自 18 个活跃的开源仓库。它衡量的是问题修复类基准常常遗漏的工程工作。

## 问题
- 现有编码代理基准主要关注修复 bug 和实现功能，因此会漏掉常见的软件工作，例如理解代码库、编写有用测试和安全地重构。
- 这很重要，因为代理可以通过功能检查，却留下薄弱测试、不完整重构、遗漏边界情况或较差的代码卫生。
- 这篇论文针对的是边界不清的任务，这类任务需要仓库探索、运行时证据和专业评审标准。

## 方法
- SWE Atlas 包含 124 个代码库问答任务、90 个测试编写任务和 70 个重构任务。
- 代码库问答任务要求代理检查仓库、运行代码、追踪行为，并带着证据回答开发者提出的问题。
- 测试编写任务要求代理添加测试并提交清单；评估使用清单检查、变异检查和评分量表检查覆盖率、位置和约定。
- 重构任务要求在保持行为不变的前提下修改代码；评估使用回归测试、隐藏测试，以及关于可维护性、清理、文档和反模式的评分量表。
- 任务、参考解和评分量表都由资深软件工程师编写；三位可信专家审查了每个任务，并删除了无效或含糊的评分量表条目。

## 结果
- 该基准包含 18 个仓库中的 284 个任务，问答、测试编写和重构的平均评分量表数量分别是 10.5、17.1 和 17.4；重构任务平均每题有 18 个测试。
- 在原生脚手架上，GPT-5.4 Codex 领先，Pass@1 为 43.49 ± 3.32，Pass³ 为 29.2；Opus 4.7 Claude Code 紧随其后，Pass@1 为 41.89 ± 3.31，Pass³ 也是 29.2。
- GPT-5.4 在问答、测试编写和重构上的分数分别是 40.80、44.36 和 44.29；Opus 4.7 在同样三个工作流上的分数分别是 40.30、38.51 和 48.57。
- 在常见的 mini-SWE-agent 脚手架下，Opus 4.7 的 Pass@1 为 38.94 ± 3.25，GPT-5.4 为 38.00 ± 3.26；列出的开权重模型中，GLM 5 最好，为 24.03 ± 2.87。
- 即使是顶级系统也表现不稳定：最佳 Pass³ 只有 29.2，按不同配置计算，比 Pass@1 低大约 30-50%。
- 评分量表检查暴露出功能测试看不到的缺口：重构任务中，回归测试通过率和评分量表通过率之间大约差 15-40 分；测试编写中，变异通过率和评分量表通过率之间大约差 10-15 分。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08366v1](https://arxiv.org/abs/2605.08366v1)
