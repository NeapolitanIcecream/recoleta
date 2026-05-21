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
## 摘要
SWE Atlas 是一个面向编码代理的 284 项任务基准，覆盖 18 个活跃开源仓库中的代码库问答、测试编写和重构。它衡量代理能否处理问题解决类基准经常遗漏的工程工作。

## 问题
- 现有编码代理基准侧重于漏洞修复和功能实现，因此会漏掉常见的软件工作，例如理解代码库、编写有用测试，以及安全重构。
- 这一点很重要，因为代理可能通过功能检查，同时留下薄弱测试、不完整重构、遗漏的边界情况或较差的代码卫生。
- 论文针对的是定义不充分的任务，这些任务需要仓库探索、运行时证据和专业评审标准。

## 方法
- SWE Atlas 包含 124 项代码库问答任务、90 项测试编写任务和 70 项重构任务。
- 代码库问答任务要求代理检查仓库、运行代码、跟踪行为，并用证据回答面向开发者的问题。
- 测试编写任务要求代理添加测试并提交清单；评估使用清单检查、变异检查，以及针对覆盖率、位置和约定的评分标准检查。
- 重构任务要求在保持行为不变的前提下修改代码；评估使用回归测试、隐藏测试，以及针对可维护性、清理、文档和反模式的评分标准。
- 专家软件工程师编写了任务、参考解法和评分标准；三名可信专家审查了每项任务，并移除了无效或含糊的评分项。

## 结果
- 该基准包含 18 个仓库中的 284 项任务，问答、测试编写和重构的平均评分项数量分别为 10.5、17.1 和 17.4；重构任务平均每项有 18 个测试。
- 在原生脚手架上，GPT-5.4 Codex 以 43.49 ± 3.32 Pass@1 和 29.2 Pass³ 领先；Opus 4.7 Claude Code 以 41.89 ± 3.31 Pass@1 和 29.2 Pass³ 紧随其后。
- GPT-5.4 在问答、测试编写和重构上的得分分别为 40.80、44.36 和 44.29；Opus 4.7 在相同工作流上的得分分别为 40.30、38.51 和 48.57。
- 在通用 mini-SWE-agent 脚手架下，Opus 4.7 得到 38.94 ± 3.25 Pass@1，GPT-5.4 得到 38.00 ± 3.26；GLM 5 是列出的最佳开放权重模型，得分为 24.03 ± 2.87。
- 即使是顶级系统也表现不稳定：最佳 Pass³ 值为 29.2，按不同配置计算，比 Pass@1 低约 30-50%。
- 评分标准检查揭示了功能测试掩盖的缺口：重构的回归测试通过率与评分标准通过率之间约有 15-40 分差距，测试编写的变异通过率与评分标准通过率之间约有 10-15 分差距。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08366v1](https://arxiv.org/abs/2605.08366v1)
