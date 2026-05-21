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
Conclave 为 OpenCode 增加了一个结构化的多 LLM 辩论引擎，让多个模型先讨论一个软件任务，再选择一个回复或实现方案。它面向代码工作，尤其是单个模型可能漏掉架构缺陷、边界情况或安全问题的任务。

## 问题
- 单模型编码智能体可能在写代码前漏掉设计缺陷、边界情况和安全风险。
- 已经为 Claude Code、Gemini CLI、Codex 或本地模型付费的团队，可能没有用于多模型工作流的直接 API 访问权限。
- 多模型辩论会增加延迟和成本，因此该工具更适合复杂任务，而非简单提示。

## 方法
- Conclave 用团队辩论引擎修改了 OpenCode；页面称大约改动了 12 个文件，同时 OpenCode 保留了 providers、agents、git 支持、tools 和 TUI。
- 模型使用 LEAD、SUPPORT、ALIGN、BUILD 和 CHALLENGE 信号进行结构化轮次辩论。
- 辩论结束后，系统按认可分数选择胜出者。
- 用户可以混用通过 CLI 认证的模型和 API 模型，包括 Claude Code、Gemini CLI、Codex、OpenAI、Anthropic、DeepSeek、Google、NVIDIA、Groq 和 Ollama。
- 每个模型会获得按自身上下文限制裁剪的辩论线程；大上下文模型可以看到更多上下文，小上下文模型会收到信号摘要。

## 结果
- 摘录没有提供 benchmark、dataset 或人工评估结果来证明输出质量优于单个 LLM。
- 实现范围：大约修改了 12 个 OpenCode 文件来加入辩论引擎。
- 成本和延迟会随团队规模和轮次数增加：3 个模型辩论 3 轮，每条用户消息会产生 9 次 API 调用。
- 成本示例：每个团队成员都会独立调用一次，因此 3 模型团队的成本约为单模型调用的 3 倍，除非使用免费的 CLI 或本地模型。
- 上下文主张：该工具可以把 1M-token 的 DeepSeek 模型和 128K-token 的 Gemini Flash 模型配对，方法是按模型截断或摘要化辩论线程。
- 成熟度主张：项目只有数周历史；辩论、团队持久化和 provider 连接已经可用，context optimization、live streaming 和 Breaking Teams 是路线图项目。

## Problem

## Approach

## Results

## Link
- [https://adndvlp.github.io/conclave/](https://adndvlp.github.io/conclave/)
