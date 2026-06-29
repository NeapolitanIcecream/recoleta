---
source: hn
url: https://agingbench.github.io
published_at: '2026-05-27T23:10:09'
authors:
- zfancy
topics:
- ai-agents
- agent-reliability
- memory-systems
- benchmarking
- longitudinal-evaluation
relevance_score: 0.68
run_id: materialize-outputs
language_code: zh-CN
---

# AgingBench: AI Agents Age Too

## Summary
## 摘要
AgingBench 用来测试长寿命 AI 代理在部署后，随着记忆和状态变化，是否还能保持可靠。即使基础模型参数冻结，代理外壳在压缩、检索、修订和维护状态时，仍然可能出错。

## 问题
- 第一天的基准测试评估的是刚初始化的代理，会漏掉在多轮会话后才出现的故障。
- 持久化代理会不断积累摘要、记忆、修订后的事实和维护事件，因此可靠性取决于完整的记忆管线。
- 运营方需要知道故障出在写入、检索还是利用环节，这样才能把修复措施指向正确组件。

## 方法
- AgingBench 定义了四种老化机制：压缩老化、干扰老化、修订老化和维护老化。
- 它在重复会话中运行纵向代理场景，然后检查可靠性如何随时间变化。
- 它使用时间依赖图来追踪哪些已存事实和派生状态应该影响后续答案。
- 它使用成对反事实探针，在记忆管线的写入、检索和利用阶段诊断故障。
- 它在多个模型和记忆策略下测试由运行器控制的代理和自主代理。

## 结果
- 论文报告了 7 个场景、14 个模型、多种记忆策略，以及跨 8 到 200 个会话的约 400 次运行。
- 该基准同时覆盖由运行器控制的代理和自主代理。
- 行为测试可以保持正常，但事实精度会下降；摘要没有给出精确的精度分数。
- 派生状态跟踪在单个模型内也可能急剧崩塌；摘要没有给出按模型划分的具体崩塌率。
- 同一个错误答案可能需要不同的修复方式，取决于诊断画像指向的是写入、检索还是利用故障。

## Problem

## Approach

## Results

## Link
- [https://agingbench.github.io](https://agingbench.github.io)
