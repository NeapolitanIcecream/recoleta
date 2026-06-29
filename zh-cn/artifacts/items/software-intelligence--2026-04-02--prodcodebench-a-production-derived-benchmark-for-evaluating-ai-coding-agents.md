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
## 总结
ProdCodeBench 是一个面向 AI 编码代理的基准，基于工业 monorepo 中真实的开发者与助手会话构建。它的主要贡献是一套整理方法：保留原始用户提示，回溯已合入的代码变更，并用稳定的执行测试作为评分信号。

## 问题
- 公开的编码代理基准常常偏离生产环境：它们过度依赖开源仓库、结构化的 issue 文本，以及更窄的语言组合。
- 公司需要快速的离线评估来做模型选择和 harness 变更，但 monorepo 让可复现评估变得困难，因为旧工具、索引和服务很难重放。
- 许多真实的开发者请求不能直接用测试验证，而大型仓库里的天真实验测试选择会挑到不稳定或无关的测试，污染通过/失败信号。

## 方法
- 从单轮、真实的开发者-代理对话中构建任务，这些对话最终形成了已提交的 diff，保留逐字提示，并通过 AI provenance 日志把它和已合入的代码变更关联起来。
- 通过从当前仓库状态回退已合入的 diff 来隐藏真实解，然后在回退后的版本上评估代理。
- 过滤提示，去掉泄露解决方案 diff 的内容、模板/系统提示，以及被 LLM 分类器判定为不可测试的提示。
- 为每个 diff 检索候选测试，再运行测试相关性代理，并重复执行变更前/变更后版本，只保留稳定且相关的测试，并将它们分为 fail-to-pass (F2P) 或 pass-to-pass (P2P)。
- 让基准持续滚动，而不是固定不变，这样样本能保持可执行、保持最新，也更不容易在变化中的 monorepo 里受到污染。

## 结果
- 在四个 foundation model 的 F2P 子集上，solve rate 范围是 **53.2% 到 72.2%**；**Claude Opus 4.5** 表现最好。
- 大约 **75%** 的基准任务至少包含一个 F2P 测试；另外 **25%** 依赖仅 P2P 的评估。
- 这个基准覆盖 **7 种编程语言**，反映的是多语言生产代码库，而不是单语言设置。
- 每个模型评估运行 **3 次**，论文报告了 solve rate 的 **95% 置信区间**。
- 在人工验证中，任务可测试性分类器与人工一致意见在抽样案例中的匹配率为 **96.67% (29/30)**。
- 测试相关性验证使用两名标注者，初始一致率超过 **80%**；论文在 **15 对**样本中报告了 **2 个假阴性**和 **1 个假阳性**，并且还指出一个 no-op agent 的 solve rate 为 **0.0%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01527v2](http://arxiv.org/abs/2604.01527v2)
