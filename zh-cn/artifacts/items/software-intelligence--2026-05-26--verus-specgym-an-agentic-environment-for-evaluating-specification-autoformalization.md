---
source: arxiv
url: https://arxiv.org/abs/2605.26457v1
published_at: '2026-05-26T02:12:48'
authors:
- Anmol Agarwal
- Natalie Neamtu
- Pranjal Aggarwal
- Seungone Kim
- Jannis Limperg
- Cedric Flamant
- Kanna Shimizu
- Bryan Parno
- Sean Welleck
topics:
- specification-autoformalization
- formal-verification
- code-intelligence
- ai-coding-agents
- verus
- software-benchmarks
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization

## Summary
## 摘要
Verus-SpecGym 评估编码代理能否把自然语言编程任务转成忠实的 Verus 规格说明。这很重要，因为只有当形式化规格与用户意图一致时，验证过的代码才有价值。

## 问题
- AI 代理可以生成代码和证明，但验证器只检查代码是否符合形式化规格，所以错误的规格也可能为错误行为“背书”。
- 规格自动形式化很难，因为自然语言编程任务里有输入约束、输出规则和边界情况，这些都要变成精确的逻辑谓词。
- 现有评估方式成本高或效果弱：专家参考规格无法扩展，LLM 评审也可能漏掉细微的规格错误。

## 方法
- 论文提出了 Verus-SpecBench，这是一个基于 Codeforces 题目、面向 Verus（一个 Rust 验证器）的 581 个规格编写任务集合。
- Verus-SpecGym 给代理提供非形式化题目、带有 `pre_spec` 和 `post_spec` 的 Verus 骨架、样例测试、示例、文档，以及通过 Verus、bash 和文件系统的工具访问。
- 评估器扩展了 Verus 的 `exec_spec`，让生成的逻辑规格可以在具体输入和输出上作为可执行的 Rust 检查运行。
- 每个提交的规格都会在四类用例上测试：接受有效输入、拒绝无效输入、接受正确输出、拒绝错误输出。
- 隐藏评估使用官方 Codeforces 测试，以及由参赛者编写、用来破坏错误解法的对抗性 Codeforces hacks。

## 结果
- 在 581 个任务上，表现最好的模型 `gemini-3.1pro` 完成了 77.8%。
- 其他前沿模型在论文固定的计算和时间预算下完成了 51.1% 到 57.8%。
- 开源模型只能达到 21.5% 到 25.5%，比最低的前沿模型得分至少低 25.6 个百分点。
- 论文评估了 6 个前沿和开源代理。
- LLM-as-a-judge 评估漏掉了可执行评估器捕捉到的 26% 失败。
- 报告的失败模式包括遗漏输入假设、接受错误输出和拒绝有效输出。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.26457v1](https://arxiv.org/abs/2605.26457v1)
