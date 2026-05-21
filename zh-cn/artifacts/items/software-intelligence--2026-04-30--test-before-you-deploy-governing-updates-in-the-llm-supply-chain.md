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
## 摘要
本文将托管式 LLM 更新视为软件供应链风险，并提出在采用更新前由部署方执行检查。主要观点是，面向具体应用的合约和按风险类别组织的测试可以发现由提供商侧模型变更引起的回归。

## 问题
- 托管式 LLM API 可能在端点或版本不变的情况下改变行为，这可能破坏代码生成、结构化输出、安全行为和工作流自动化。
- 提供商的基准测试和发布说明不会测试每个应用的需求，例如有效 JSON、安全的认证代码或仅输出代码。
- 论文引用了既有漂移证据：据报告，GPT-4 的直接代码执行率在三个月内从 52% 降至 10%；一次 Anthropic 事件影响了最多 16% 的请求。

## 方法
- 定义生产合约：模型在使用前必须满足的明确规则，例如通过单元测试、生成有效 JSON，或造成 0% 安全违规。
- 按部署风险对测试分组，例如认证、数据验证和结构化输出，而不是依赖一个总分。
- 对每个提示运行多次，并记录可见的模型名称和时间戳，以便在非确定性输出下跟踪漂移。
- 使用兼容性关卡，将各类别指标与阈值比较，并在某个阈值未通过时阻止采用。
- 在失败后采取缓解措施，例如修改提示、修订工作流、启用回退方案和重新验证。

## 结果
- 探索性验证使用了 7 个 Anthropic Claude 模型：Haiku 3.5、Opus 3、Sonnet 4、Opus 4.5、Sonnet 4.5、Haiku 4.5 和 Opus 4.6。
- 测试套件在 3 个风险领域使用了 25 个提示：认证函数、数据验证和结构化输出生成。
- 每个提示运行 3–5 次，用于测量输出变异性和类别级合规性。
- 结构化 JSON 任务比 SQL 和认证任务表现出更多漂移；例子包括空 JSON、过早报错、异常类型变化、输出 JavaScript 而不是 Python，以及由元数据包裹的输出。
- 一个后端 SQL 函数在 Sonnet 4 上通过了所有测试，但第二天未通过安全编码测试，而 Sonnet 4.5 在两天内都保持稳定。
- 论文没有报告完整的定量通过率表；其最有力的结果是定性证据，即按风险类别组织的测试可以发现单一汇总正确性指标可能掩盖的回归。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.27789v1](https://arxiv.org/abs/2604.27789v1)
