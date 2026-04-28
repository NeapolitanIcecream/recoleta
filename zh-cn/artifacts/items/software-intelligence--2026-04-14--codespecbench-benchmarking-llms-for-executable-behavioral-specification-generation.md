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
CodeSpecBench 是一个基准，用来测试 LLM 是否能根据自然语言软件任务写出可执行的前置条件和后置条件。结果显示这项任务很难，尤其是在真实代码仓库场景中，最好的模型通过率也只有 20.2%。

## 问题
- 论文研究的是 LLM 是否理解程序的预期行为，而不只是能否生成通过测试的代码。
- 以往的规格生成基准有明显限制：很多使用静态验证器、断言形式更简单、数据集较小，或者只包含函数级任务。
- 这很重要，因为可执行行为规格可以检查语义意图、支持验证，并为人类与智能体围绕代码协作提供更清晰的接口。

## 方法
- 该基准要求模型生成两个可执行的 Python 函数：一个 **precondition**，用于检查执行前输入和状态是否合法；一个 **postcondition**，用于检查执行后输出和状态是否正确。
- 它包含两种设置：**CodeSpecBench-Func** 用于自包含的函数任务，**CodeSpecBench-Repo** 用于带代码上下文的真实多文件仓库问题。
- 评估基于执行。生成的规格必须对所有有效行为都接受，以满足 **correctness**；并对所有无效行为都拒绝，以满足 **completeness**；**pass rate** 要求两者同时满足。
- CodeSpecBench-Func 包含 **2,494** 个基于 LeetCodeDataset 构建的任务。作者生成并验证了大规模测试集，平均每个任务有 **217.8** 个测试，平均语句覆盖率 **96.3%**，平均分支覆盖率 **93.6%**。
- CodeSpecBench-Repo 使用 **12** 个 Python 项目中的 **500** 个 SWE-bench Verified 问题，配有经 UTBoost 增强的测试；提示平均长度约 **19.7k** token，而函数级任务为 **520.7**。

## 结果
- 该基准覆盖 **2,494 个函数级任务** 和 **500 个仓库级任务**。平均每个任务的测试数分别为 Func 的 **217.8** 和 Repo 的 **123.3**。
- 在 **CodeSpecBench-Func** 上，最高 **pass rate** 由 **GPT-5-mini** 取得，为 **47.0%**。其他较强结果包括 **Gemini-2.5-Pro** 的 **46.2%**，以及 **GPT-OSS-120B** 的 **42.5%**。
- 在 **CodeSpecBench-Repo** 上，性能明显下降。最高 **pass rate** 是 **Claude-4.5-Sonnet** 的 **20.2%**，之后是 **Gemini-2.5-Pro** 的 **18.2%**，以及 **GPT-5-mini** 的 **9.6%**。
- 在仓库级任务上，领先模型的 correctness/completeness 分别为：**Claude-4.5-Sonnet** 的 **37.4% correctness**、**57.2% completeness**、**20.2% pass**。**Gemini-2.5-Pro** 的结果是 **30.8% / 53.0% / 18.2%**。
- 代码能力较强的开源模型在仓库任务上仍然表现吃力：**DeepSeek-V3.2** 的 repo pass 为 **6.8%**，**QWQ-32B** 为 **3.6%**，带推理的 **Qwen3-32B** 为 **2.0%**。
- 论文认为，规格生成比代码生成更难，因此代码生成分数高并不表示模型很好地捕捉了程序语义。当前摘录未包含与之对比的代码生成结果表。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.12268v1](http://arxiv.org/abs/2604.12268v1)
