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
## 摘要
这篇论文提出了 **SWE-STEPS**，这是一个用于评估编程代理的数据集和评测框架。它不再把任务当作彼此独立的单个 pull request，而是让代理处理相互依赖的 PR 序列。论文的核心结论是，标准的单 PR 基准高估了代理能力，也看不到它们对长期代码质量造成的损害。

## 问题
- 现有编程代理基准一次只评估一个 pull request，并假设仓库处于干净的初始状态。这与真实软件开发不符，因为代码改动会不断累积。
- 这种设定看不到代理早期代码带来的连带影响，包括回归问题、测试负担增加、技术债积累，以及代码复杂度上升。
- 这很重要，因为一个代理即使能通过孤立任务，也可能在多步开发序列中失败，并让仓库更难维护。

## 方法
- 作者构建了一个自动化框架，从 git 历史中提取相关 PR 链、元数据、被修改的符号以及关联测试。
- 他们创建了 **SWE-STEPS** 数据集，包含 **168 个任务** 和 **963 个 PR**，覆盖 **6 个 Python 仓库**，每条任务链由 **3 到 11 个 PR** 组成。
- 每个任务都包含一个初始仓库状态、一组按顺序排列的 PR 请求，以及拆分后的验证测试套件：用于检验新功能的 **FAIL_TO_PASS** 测试和用于回归检查的 **PASS_TO_PASS** 测试。
- 他们在三种设定下评估代理：**Individual PR**（孤立评估，采用 SWE-bench 风格重置）、**Global Memory / conversational coding**（状态在多个 PR 之间持续保留），以及 **PRD-based coding**（一开始给出全部需求，最后检查累积后的完整测试套件）。
- 评估既看功能是否完成，也看仓库健康状况，并使用 **cognitive complexity** 和 **technical debt** 等静态分析指标，与人类编写的真实变更进行比较。

## 结果
- **数据集规模：** **168 个任务**、**963 个 PR**、**6 个仓库**；任务链长度为 **3 到 11 个 PR**。
- **任务复杂度：** 问题文本平均长度为 **3,656 词**，而 SWE-Bench 为 **195.1**，SWE-Gym 为 **239.8**；平均编辑文件数为 **17.1**，而后两者分别为 **1.7** 和 **2.5**。
- **性能高估：** 孤立 PR 评估会把成功率高估最多 **20 个百分点**。例如在 Mini split 上，**Claude Sonnet 4.5** 在 Individual 设定中的成绩为 **66.25%**，在连续设定中降到 **43.75%**。
- 在 Lite split 上，**Gemini 3 Flash** 从 Individual 设定的 **56.52%** 降到 Global 设定的 **36.59%**。
- 在测试的各个 LLM 中，引入有状态的多步评估后，性能相比孤立评估下降约 **15% 到 25%**。
- 论文还称，与人类开发者相比，代理生成的代码具有更高的 **cognitive complexity** 和更多 **technical debt**，因此会恶化仓库健康状况。这些指标用 **SonarQube** 测量，但摘录中没有给出具体数值差异。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03035v1](http://arxiv.org/abs/2604.03035v1)
