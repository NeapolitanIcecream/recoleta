---
source: arxiv
url: https://arxiv.org/abs/2605.26521v1
published_at: '2026-05-26T04:07:55'
authors:
- Nafiseh Kahani
- Mojtaba Bagherzadeh
topics:
- multi-agent-testing
- agent-workflows
- structural-coverage
- code-intelligence
- software-agents
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Testing Agentic Workflows with Structural Coverage Criteria

## Summary
## 摘要
本文提出一种面向多智能体工作流的结构覆盖测试方法，让测试集能够表明已声明的智能体、工具、限制和交接是否被实际执行。

## 问题
- 端到端任务成功可能通过，但某些智能体、工具权限、受限调用或委派路径从未运行。
- 工作流修改可能改变工具访问或交接结构，却不会导致基准失败，这使结构回归难以发现。
- 这对带有策略、安全或合规约束的智能体系统很重要，因为团队需要可追踪的证据来证明限制和路由规则已经测试过。

## 方法
- 该方法把智能体工作流转换为一个带类型的协调图，图中包含智能体节点、工具节点、允许的工具边、受限工具边和委派边。
- 它导出四类覆盖准则：可达智能体、允许的工具调用、受限工具尝试和委派边。
- 对于每个图中的义务，它构造一个见证目标，例如到达某个智能体、使用某个工具、探测受限工具或触发一次交接。
- DSPy 将每个目标转成自然语言测试场景；运行时轨迹再判断预期的结构事件是否发生。
- 原型面向 OpenAI Agents SDK 风格的工作流，并从 Python 智能体入口点提取清单。

## 结果
- 评估覆盖 10 个来自 SDK 的工作流，共有 49 个可达智能体、47 个工具和 403 个结构义务。
- 在给定的细化预算内，生成的场景见证了 75 个允许工具义务中的 54 个，即 72%。
- 在同一受限流程内，生成的场景见证了 48 个委派义务中的 36 个，即 75%。
- 对受限工具的探测产生了 248 个受限工具义务中的 23 个受限调用违规，找出了具体的路由错误。
- 运行中的 oai_customer_service 示例包含 3 个可达智能体、2 个工具、2 条允许的工具边、4 条受限工具边和 4 条委派边，总计 13 个结构义务。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.26521v1](https://arxiv.org/abs/2605.26521v1)
