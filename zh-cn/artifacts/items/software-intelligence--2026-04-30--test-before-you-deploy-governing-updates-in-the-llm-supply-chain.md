---
source: arxiv
url: https://arxiv.org/abs/2604.27789v1
published_at: '2026-04-30T12:32:13'
authors:
- Mohd Sameen Chishti
- Damilare Peter Oyinloye
- Jingyue Li
topics:
- llm-supply-chain
- behavioral-drift
- regression-testing
- llm-governance
- code-generation
- ci-cd
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Test Before You Deploy: Governing Updates in the LLM Supply Chain

## Summary
## 总结
本文将托管的 LLM 更新视为软件供应链风险，并提出在采用前由部署方进行检查。其核心主张是，应用特定契约和按风险类别划分的测试，可以发现由提供方模型变更引起的回归。

## 问题
- 托管的 LLM API 可能在不更改端点或版本号的情况下改变行为，这会破坏代码生成、结构化输出、安全行为和工作流自动化。
- 提供方的基准测试和发布说明不会针对每个应用的要求进行测试，例如有效 JSON、安全的认证代码或仅输出代码。
- 论文引用了先前的漂移证据：据称 GPT-4 直接代码执行率在三个月内从 52% 降到 10%，Anthropic 的一次事件影响了多达 16% 的请求。

## 方法
- 定义生产契约：模型在使用前必须满足的明确规则，例如通过单元测试、生成有效 JSON，或将安全违规率降到 0%。
- 按部署风险对测试分组，例如认证、数据验证和结构化输出，而不是只看一个总分。
- 每个提示运行多次，并记录可见的模型名称和时间戳，以便在非确定性输出下追踪漂移。
- 使用兼容性门槛将各类别指标与阈值比较，在任一阈值未通过时阻止采用。
- 失败后采取缓解措施，例如修改提示、调整工作流、启用回退方案和重新验证。

## 结果
- 探索性验证使用了 7 个 Anthropic Claude 模型：Haiku 3.5、Opus 3、Sonnet 4、Opus 4.5、Sonnet 4.5、Haiku 4.5 和 Opus 4.6。
- 测试集包含 25 个提示，覆盖 3 个风险领域：认证函数、数据验证和结构化输出生成。
- 每个提示运行 3 到 5 次，以衡量输出波动和类别级合规性。
- 结构化 JSON 任务比 SQL 和认证任务更容易出现漂移；例子包括空 JSON、过早报错、异常类型变化、输出 JavaScript 而不是 Python，以及被元数据包裹的输出。
- 一个后端 SQL 函数在第一天用 Sonnet 4 通过了全部测试，第二天却没通过安全编码测试，而 Sonnet 4.5 在两天内都保持稳定。
- 论文没有报告完整的定量通过率表；它最强的结果是定性证据，说明按风险类别的测试可以发现单一汇总正确性指标可能掩盖的回归。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.27789v1](https://arxiv.org/abs/2604.27789v1)
