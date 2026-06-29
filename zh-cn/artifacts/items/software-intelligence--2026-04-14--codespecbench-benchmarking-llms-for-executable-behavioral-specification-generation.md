---
source: arxiv
url: http://arxiv.org/abs/2604.12268v1
published_at: '2026-04-14T04:31:45'
authors:
- Zaoyu Chen
- Jianbo Dai
- Boyu Zhu
- Jingdong Wang
- Huiming Wang
- Xin Xu
- Haoyang Yuan
- Zhijiang Guo
- Xiao-Ming Wu
topics:
- code-benchmark
- specification-generation
- program-semantics
- repository-level-reasoning
- llm-evaluation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# CodeSpecBench: Benchmarking LLMs for Executable Behavioral Specification Generation

## Summary
## 摘要
CodeSpecBench 是一个基准，用来测试 LLM 是否能根据自然语言软件任务写出可执行的前置条件和后置条件。结果表明，这件事很难，尤其是在真实代码仓库里，最佳模型的通过率只有 20.2%。

## 问题
- 这篇论文研究的是 LLM 是否理解程序的预期行为，而不只是能否生成能通过测试的代码。
- 以往用于规格生成的基准有不少限制：很多依赖静态验证器、只用更简单的断言形式、数据集较小，或者只做函数级任务。
- 这很重要，因为可执行的行为规格可以检查语义意图，支持验证，也能为人和代理围绕代码协作提供更清晰的接口。

## 方法
- 这个基准要求模型生成两个可执行的 Python 函数：**前置条件**，用于在执行前检查有效输入和状态；**后置条件**，用于在执行后检查输出和状态。
- 它有两个设置：**CodeSpecBench-Func** 面向自包含的函数任务，**CodeSpecBench-Repo** 面向带代码上下文的真实多文件仓库问题。
- 评估基于执行。生成的规格必须接受所有有效行为，才算满足**正确性**；还必须拒绝所有无效行为，才算满足**完整性**；**通过率**要求两者都满足。
- CodeSpecBench-Func 包含 **2,494** 个任务，来自 LeetCodeDataset。作者生成并验证了大规模测试集，平均每个任务有 **217.8** 个测试，平均语句覆盖率 **96.3%**，平均分支覆盖率 **93.6%**。
- CodeSpecBench-Repo 使用 **12** 个 Python 项目中的 **500** 个 SWE-bench Verified 问题，配合 UTBoost 增强测试，平均提示词长度约 **19.7k** tokens，而函数级任务约为 **520.7**。

## 结果
- 这个基准覆盖 **2,494** 个函数级任务和 **500** 个仓库级任务。平均每个任务的测试数分别是 Func 的 **217.8** 和 Repo 的 **123.3**。
- 在 **CodeSpecBench-Func** 上，最佳**通过率**是 **GPT-5-mini** 的 **47.0%**。其他较好的结果是 **Gemini-2.5-Pro** 的 **46.2%** 和 **GPT-OSS-120B** 的 **42.5%**。
- 在 **CodeSpecBench-Repo** 上，性能明显下降。最佳**通过率**是 **Claude-4.5-Sonnet** 的 **20.2%**，其次是 **Gemini-2.5-Pro** 的 **18.2%** 和 **GPT-5-mini** 的 **9.6%**。
- 仓库级任务上，最佳模型的正确性/完整性分别是 **37.4% / 57.2% / 20.2%**，对应 **Claude-4.5-Sonnet**。**Gemini-2.5-Pro** 的结果是 **30.8% / 53.0% / 18.2%**。
- 即使是代码能力很强的开源模型，在仓库任务上也表现吃力：**DeepSeek-V3.2** 的仓库通过率是 **6.8%**，**QWQ-32B** 是 **3.6%**，带推理的 **Qwen3-32B** 是 **2.0%**。
- 论文的结论是，规格生成比代码生成更难，所以高代码生成分数并不意味着模型真正掌握了程序语义。摘录里没有包含对应代码生成分数的对比表。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.12268v1](http://arxiv.org/abs/2604.12268v1)
