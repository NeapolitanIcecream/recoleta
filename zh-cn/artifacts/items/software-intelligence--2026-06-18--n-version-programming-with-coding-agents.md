---
source: arxiv
url: https://arxiv.org/abs/2606.20158v1
published_at: '2026-06-18T12:23:02'
authors:
- Javier Ron
- Benoit Baudry
- Martin Monperrus
topics:
- coding-agents
- n-version-programming
- software-reliability
- code-intelligence
- automated-testing
- multi-agent-software-engineering
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# N-Version Programming with Coding Agents

## Summary
## 摘要
本文测试 AI 编码代理能否让 N 版本编程成为提升软件可靠性的实用方法。研究发现，不同代理版本有许多共同故障，但多数投票仍能减少观测到的故障。

## 问题
- N 版本编程依赖各版本独立失效，但 Knight-Leveson 研究显示，人类编写的版本经常在相同输入上失效。
- AI 编码代理现在可以低成本生成许多实现，因此本文考察代理、模型和语言多样性是否能减少共同失效模式。
- 这关系到自动化软件生产，因为只有在投票能屏蔽足够多缺陷时，代理编写的冗余代码才可能提升可靠性。

## 方法
- 作者使用 AI 编码代理复现了 Knight-Leveson 的 Launch Interceptor Program 实验。
- 他们在 5 个代理运行框架、23 个模型配置和 3 种语言中生成了 69 个实现：Python、Rust 和 Pascal。
- 每个版本都必须通过 200 个用例的验收筛查，参照对象是一个由 82 个单元测试验证过的 Python oracle。
- 通过验收的 48 个版本在同一组 1,000,000 个随机输入上运行；当 241 个输出位中的任意一位与 oracle 不同时，记录为一次故障。
- 研究测量了共同故障、成对故障相关性、语言和代理影响、LIC 层面的故障来源，以及所有 3 版本多数投票单元。

## 结果
- 69 个生成版本中有 48 个通过验收，录取率为 70%。Cursor 通过 6/6，Claude Code 通过 13/15，Codex 通过 11/15，Gemini 通过 8/15，OpenCode 通过 10/18。
- 录取率因语言而异：Python 为 18/23，Rust 为 17/23，Pascal 为 13/23。
- 独立性模型失效：测试活动发现 429 个共同故障用例，而随机独立性预测为 115.36，z=29.20。
- 在 48 个通过验收的版本中，27 个在 1,000,000 个用例的测试活动中没有故障；最差版本在 10,469 个输入上失效。
- 在全部 17,296 个三版本单元中，平均故障数从单版本的 387.44 降至多数投票三元组的 130.99。
- 17,296 个三版本单元中有 11,844 个在 1,000,000 个随机输入上没有观测到故障。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.20158v1](https://arxiv.org/abs/2606.20158v1)
