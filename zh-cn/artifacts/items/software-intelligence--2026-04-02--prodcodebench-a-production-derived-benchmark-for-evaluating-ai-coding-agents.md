---
source: arxiv
url: http://arxiv.org/abs/2604.01527v2
published_at: '2026-04-02T01:52:55'
authors:
- Smriti Jha
- Matteo Paltenghi
- Chandra Maddila
- Vijayaraghavan Murali
- Shubham Ugare
- Satish Chandra
topics:
- ai-coding-agents
- benchmarking
- software-engineering
- monorepo-evaluation
- code-intelligence
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents

## Summary
## 摘要
ProdCodeBench 是一个用于评估 AI 编码代理的基准，数据来自工业 monorepo 中真实的开发者—助手会话。它的主要贡献是一套筛选方法：保留用户原始提示词，回退已落地的代码变更，并用可稳定执行的测试作为评分信号。

## 问题
- 公开的编码代理基准通常不符合生产环境条件：它们更偏向开源仓库、结构化 issue 文本，以及更窄的语言分布。
- 公司需要快速的离线评估来选择模型和调整 harness，但 monorepo 很难做可复现评估，因为旧工具、索引和服务很难重放。
- 许多真实的开发者请求无法直接测试，而在大型代码库里直接选择测试时，容易选到不稳定或不相关的测试，这会破坏通过/失败信号。

## 方法
- 从单轮、真实的开发者—代理对话中构建任务，这些对话最终产生了已提交的 diff；保留逐字提示词，并通过 AI 来源日志将其关联到已落地的代码变更。
- 通过从当前仓库状态中回退已落地的 diff 来隐藏真实解答，然后在这个回退后的版本上评估代理。
- 过滤提示词，移除会泄露解答 diff 的样本、模板/系统提示词，以及被 LLM 分类器判定为不可测试的提示词。
- 为每个 diff 检索候选测试，然后运行测试相关性代理，并重复执行变更前/变更后的测试，只保留稳定且相关的测试，并将其分类为 fail-to-pass (F2P) 或 pass-to-pass (P2P)。
- 让基准保持滚动更新，而不是固定不变，这样样本能持续可执行、保持最新，并且在不断变化的 monorepo 中更不容易受到污染。

## 结果
- 在 F2P 子集上测试四个基础模型时，解题率范围为 **53.2% 到 72.2%**；**Claude Opus 4.5** 表现最好。
- 大约 **75%** 的基准任务至少包含一个 F2P 测试；另外 **25%** 只能依赖 P2P 评估。
- 该基准覆盖 **7 种编程语言**，反映的是多语言生产代码库，而不是单语言环境。
- 每个模型评估都会运行 **3 次**，论文为解题率报告了 **95% 置信区间**。
- 在人工验证中，任务可测试性分类器与人工共识在抽样案例中的一致率为 **96.67% (29/30)**。
- 测试相关性验证由两名标注者完成，初始一致率高于 **80%**；论文在一个 **15 对** 的样本中报告了 **2 个假阴性** 和 **1 个假阳性**，还说明一个 no-op 代理的解题率为 **0.0%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01527v2](http://arxiv.org/abs/2604.01527v2)
