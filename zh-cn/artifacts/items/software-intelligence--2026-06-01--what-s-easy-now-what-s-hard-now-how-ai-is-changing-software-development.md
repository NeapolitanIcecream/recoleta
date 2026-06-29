---
source: hn
url: https://brooker.co.za/blog/2026/05/18/whats-easy-whats-hard.html
published_at: '2026-06-01T23:05:07'
authors:
- pgedge_postgres
topics:
- coding-agents
- software-engineering
- llm-agents
- developer-tools
- formal-methods
- feedback-loops
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# What's Easy Now? What's Hard Now? How AI Is Changing Software Development

## Summary
## 总结
文章认为，编程代理在有快速、准确反馈的软件任务上进步最大，比如编译器错误、测试、基准测试和形式化检查。它预测，规格明确的系统工作可能会比依赖人类判断的 UI 或产品工作更容易让代理完成。

## 问题
- 编程代理的能力常常按模型在开放环路中的质量来判断，这会忽略代理如何通过构建、测试和修复循环改进。
- 软件任务在反馈质量上差别很大。机器可检查的清晰反馈有利于代理；模糊的人类偏好会拖慢它们。
- 这很重要，因为工具设计、规格实践和工程工作流会决定代理能可靠构建什么。

## 方法
- 核心机制是反馈：LLM 编写或编辑代码，观察错误或测试结果，然后再试一次。
- 文章比较了开放环路的 AI 自动补全和把构建、测试、迭代都放进代理循环中的编程代理。
- 它用了一些反馈很强的例子，包括 Rust 编译器消息、性能基准测试、基于性质的测试、TLA+、P、Verus、Hydro、模拟器、mock 和规格分析。
- 它也对比了反馈较弱或依赖人的任务，比如架构选择、UI 质量，以及带有隐藏运行时故障的并发程序。

## 结果
- 这段摘录没有报告任何基准、数据集、基线或测得的准确率结果。
- 它认为，过去大约 2 年里，开发者工具已经从开放环路自动补全转向会运行反馈循环的代理。
- 它认为，计算机系统至少 85 年来一直具有人类水平以上的能力，而编程代理很可能会沿着同样的模式发展：某些任务很强，另一些任务很弱。
- 它预测，带有明确规格、安全性质、活性性质、测试或基准的任务会变得更容易让代理完成。
- 它预测，当成功取决于缓慢且不稳定的人类反馈时，SaaS 和 UI 工作对代理可能仍然很难；而当规格可以由机器检查时，系统软件可能会变得更容易。

## Problem

## Approach

## Results

## Link
- [https://brooker.co.za/blog/2026/05/18/whats-easy-whats-hard.html](https://brooker.co.za/blog/2026/05/18/whats-easy-whats-hard.html)
