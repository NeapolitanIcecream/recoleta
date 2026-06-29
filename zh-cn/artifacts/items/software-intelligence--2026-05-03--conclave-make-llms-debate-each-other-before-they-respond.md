---
source: hn
url: https://adndvlp.github.io/conclave/
published_at: '2026-05-03T23:45:45'
authors:
- andngd
topics:
- multi-agent-software-engineering
- llm-debate
- code-agents
- automated-software-production
- developer-tools
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Conclave – make LLMs debate each other before they respond

## Summary
## 摘要
Conclave 为 OpenCode 增加了一个结构化的多 LLM 辩论引擎，让多个模型先讨论软件任务，再决定由哪个响应或实现方案胜出。它面向代码工作场景，因为单个模型可能漏掉架构缺陷、边缘情况或安全问题。

## 问题
- 单模型编码代理在写代码前可能漏掉设计缺陷、边缘情况和安全风险。
- 已经为 Claude Code、Gemini CLI、Codex 或本地模型付费的团队，可能没有直接的 API 访问，难以做多模型工作流。
- 多模型辩论会增加延迟和成本，所以这个工具更适合复杂任务，而不是简单提示。

## 方法
- Conclave 在 OpenCode 上改动出一个团队辩论引擎；页面说明大约改了 12 个文件，而 OpenCode 继续提供 providers、agents、git 支持、tools 和 TUI。
- 模型按结构化轮次辩论，使用 LEAD、SUPPORT、ALIGN、BUILD 和 CHALLENGE 信号。
- 辩论结束后，按 endorsement score 选出胜者。
- 用户可以混合使用带 CLI 认证的模型和 API 模型，包括 Claude Code、Gemini CLI、Codex、OpenAI、Anthropic、DeepSeek、Google、NVIDIA、Groq 和 Ollama。
- 每个模型都有与其上下文上限匹配的辩论线程；大上下文模型能看到更多上下文，小模型收到信号摘要。

## 结果
- 摘要没有给出任何基准、数据集或人工评测结果，无法证明它比单个 LLM 输出更好。
- 实现范围：大约改动了 12 个 OpenCode 文件来加入辩论引擎。
- 成本和延迟会随团队规模和轮次增加：3 个模型辩论 3 轮，每个用户消息会产生 9 次 API 调用。
- 成本示例：每个团队成员都会独立调用一次，所以一个 3 模型团队的成本大约是单模型调用的 3 倍，除非使用免费的 CLI 或本地模型。
- 上下文说明：该工具可以把 1M token 的 DeepSeek 模型和 128K token 的 Gemini Flash 模型配在一起，并按模型截断或摘要辩论线程。
- 成熟度说明：项目只有几周历史；辩论、团队持久化和 provider 连接可用，而上下文优化、实时流式传输和 Breaking Teams 还在路线图上。

## Problem

## Approach

## Results

## Link
- [https://adndvlp.github.io/conclave/](https://adndvlp.github.io/conclave/)
