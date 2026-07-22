---
source: arxiv
url: https://arxiv.org/abs/2607.18711v1
published_at: '2026-07-21T05:07:22'
authors:
- Ruogu Yang
- Yifeng He
- Yundi Xu
- Yuqing Wei
- Hao Chen
topics:
- code-intelligence
- automated-software-testing
- llm-test-generation
- functional-bug-detection
- program-invariants
- software-foundation-model
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# LLM-Based Invariant Testing for Software Functional Bugs

## Summary
## 摘要
LISA 是一种基于 LLM 的不变量测试框架，用于检测 C/C++ 软件库中不一定会导致崩溃的功能性缺陷。它将 API 序列探索与基于文档的不变量生成分开，生成可执行测试以及供开发者确认的高置信度缺陷候选。

## 问题
- 手动编写单元测试要求开发者指定 API 输入、预期输出和调用序列，成本高，而且需要详细了解 API 语义。
- 传统模糊测试主要检测崩溃和挂起，因此经常会漏掉那些在异常终止前返回错误结果的功能性缺陷。
- 现有的 LLM 测试生成器可能生成不可靠的输入—输出断言，从而产生预言机问题：测试失败可能反映的是生成的预言机错误，而不是库中的缺陷。

## 方法
- LISA 使用 Clang 提取 API 和类型信息，然后利用 LLM 根据库规则、示例和生命周期约束生成可执行的 API 调用序列。
- 它会迭代修复无效序列，并结合 API 3-gram 反馈与自适应能量凝聚，在探索新的 API 组合和复用成功模式之间取得平衡。
- 它将经过验证的序列划分为语义一致的片段，并要求能力更强的 LLM 在片段边界插入不变量，同时使用 API 文档、挖掘出的契约和观测到的参考行为。
- 这些不变量检查状态有效性、取值范围、守恒关系和文档规定的语义契约等属性；违反不变量的情况会被报告为高置信度候选，而不是已证实的缺陷。

## 结果
- 根据论文，在 7 个真实世界的 C/C++ 库上，LISA 生成的测试取得了高于 OSS-Fuzz 的平均库级分支覆盖率；但所给摘录未提供汇总覆盖率数值。
- 在重新引入的历史功能性缺陷上，LISA 比作为对比对象的当前最先进 LLM 单元测试框架 CITYWALK 多检测出 9 个缺陷。
- 在 3 小时的预算下对 zlib 进行测试时，采用阶数 N=3 的 API 3-gram 反馈生成了 818 个有效程序，行覆盖率为 73.01%，分支覆盖率为 60.01%；N=2 生成了 512 个有效程序，分支覆盖率为 59.22%；N=4 生成了 705 个有效程序，分支覆盖率为 57.02%。
- 现有证据支持其在功能性缺陷检测方面有所改进，并具备有竞争力的覆盖率，但不变量的可靠性尚未得到形式化证明，所有报告的候选都需要开发者确认。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.18711v1](https://arxiv.org/abs/2607.18711v1)
