---
source: arxiv
url: http://arxiv.org/abs/2604.03035v1
published_at: '2026-04-03T13:44:40'
authors:
- KN Ajay Shastry
- Ganesh Senrayan
- Shrey Satapara
- Pranoy Panda
- Chaitanya Devaguptapu
topics:
- coding-agents
- benchmarking
- software-evolution
- repository-level-evaluation
- multi-step-reasoning
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution

## Summary
## 总结
本文介绍了 SWE-STEPS，一个面向编码代理的数据集和评估框架，用来评估依赖式 pull request 序列，而不是孤立任务。核心结论是，标准的单 PR 基准会高估代理能力，也会忽略对长期代码质量的损害。

## 问题
- 现有的编码代理基准一次只评估一个 pull request，而且是在干净的仓库状态下进行，这不符合真实软件开发中变更会不断累积的情况。
- 这种设置会漏掉前序代理代码带来的溢出影响，包括回归、不断增加的测试负担、技术债务，以及更高的代码复杂度。
- 这很重要，因为一个代理即使能通过孤立任务，也可能在多步开发序列中失败，并让仓库更难维护。

## 方法
- 作者构建了一个自动化框架，利用 git 历史提取相关 PR 链、它们的元数据、被修改的符号以及关联测试。
- 他们创建了 **SWE-STEPS**，一个包含 **168 个任务** 和 **963 个 PR** 的数据集，覆盖 **6 个 Python 仓库**，任务链长度为 **3 到 11 个 PR**。
- 每个任务包含初始仓库状态、按顺序排列的 PR 请求，以及分成 **FAIL_TO_PASS** 测试和 **PASS_TO_PASS** 测试的验证套件，前者检查新功能，后者检查回归。
- 他们在三种设置下评估代理：**Individual PR**（孤立，类似 SWE-bench 的重置方式）、**Global Memory / conversational coding**（跨 PR 保持状态）、以及 **PRD-based coding**（一开始给出全部需求，最后检查累计测试套件）。
- 评估同时覆盖功能成功率和仓库健康状况，并使用诸如 **cognitive complexity** 和 **technical debt** 这类静态分析指标，与人工编写的真实结果进行比较。

## 结果
- **数据集规模：** **168 个任务**、**963 个 PR**、**6 个仓库**；链长度为 **3 到 11 个 PR**。
- **任务复杂度：** 平均 issue 文本长度为 **3,656 词**，而 SWE-Bench 为 **195.1**，SWE-Gym 为 **239.8**；平均被修改文件数为 **17.1**，而后两者分别为 **1.7** 和 **2.5**。
- **性能膨胀：** 孤立 PR 评估会把成功率高估最多 **20 个百分点**。以 Mini 切分为例，**Claude Sonnet 4.5** 在 Individual 设置下从 **66.25%** 降到连续设置中的 **43.75%**。
- 在 Lite 切分上，**Gemini 3 Flash** 在 Individual 设置下从 **56.52%** 降到 Global 设置中的 **36.59%**。
- 在测试过的各个 LLM 中，引入有状态的多步评估后，性能相对孤立评估下降约 **15% 到 25%**。
- 论文还指出，代理生成的代码比人工开发者的代码具有更高的 **cognitive complexity** 和更多 **technical debt**，这些指标由 **SonarQube** 衡量，但摘要里没有给出这些指标的具体数值差异。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03035v1](http://arxiv.org/abs/2604.03035v1)
