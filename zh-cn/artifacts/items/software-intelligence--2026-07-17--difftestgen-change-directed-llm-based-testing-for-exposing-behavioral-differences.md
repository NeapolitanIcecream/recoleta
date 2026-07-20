---
source: arxiv
url: https://arxiv.org/abs/2607.16024v1
published_at: '2026-07-17T14:57:59'
authors:
- Huimin Hu
- Cristian Cadar
- Michael Pradel
topics:
- code-intelligence
- automated-testing
- llm-test-generation
- differential-testing
- software-maintenance
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# DiffTestGen: Change-Directed LLM-Based Testing for Exposing Behavioral Differences

## Summary
## 摘要
DiffTestGen 使用面向变更的 LLM 测试生成方法，揭示 Python 项目变更前后版本之间的行为差异。它结合静态调用图引导、项目文档、迭代式错误修复和联合覆盖率反馈。

## 问题
- 现有测试生成器通常无法执行拉取请求修改的代码，尤其是在变更函数为私有函数或难以通过公共 API 访问时。
- 这很重要，因为未被发现的行为差异可能导致回归、兼容性问题和可靠性问题；同时，下游回归检测器依赖能够执行变更代码的测试。

## 方法
- 分析每个拉取请求的 AST 和差异，识别变更函数，将其分类为公共方法、私有方法或特殊方法，并查找可公开访问的入口点。
- 使用静态调用图分析、API 文档、函数签名、文档字符串、导入信息和使用指导，告诉 LLM 如何到达变更代码，同时避免直接调用私有函数。
- 生成测试，通过反馈循环修复语法和运行时错误，并在隔离的旧版本和新版本程序环境中执行稳定的测试。
- 使用联合覆盖率迭代提供有针对性的覆盖率反馈。联合覆盖率结合两个程序版本中的变更行覆盖率，持续迭代，直到覆盖率达到 100% 或不再提升。

## 结果
- 在来自两个开源 Python 项目数据集的 463 个拉取请求上，DiffTestGen 在 78.2% 的拉取请求中揭示了行为差异，平均联合覆盖率达到 90.7%。
- 在两个数据集上分别进行评估时，它在 61.8% 和 79.7% 的拉取请求中揭示了行为差异，平均联合覆盖率分别为 64.5% 和 92.7%。
- 与报告中的基线方法相比，它总共多揭示了 99 个拉取请求中的行为差异，并使两个数据集上的代码覆盖率分别提高了 12.5 和 15.6 个百分点。
- 与 Testora 回归检测器集成后，结果表明 DiffTestGen 发现的行为差异能够揭示现有最佳方法遗漏的回归缺陷。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.16024v1](https://arxiv.org/abs/2607.16024v1)
