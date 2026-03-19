---
source: hn
url: https://github.com/ibrahimhajjaj/wa-agent
published_at: '2026-03-08T23:40:23'
authors:
- ibrahimwithi
topics:
- whatsapp-agent
- agent-framework
- llm-orchestration
- tool-use
- conversation-memory
relevance_score: 0.04
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Wa-agent – Framework for building AI agents on WhatsApp

## Summary
这是一个面向 WhatsApp 的 AI agent 框架，目标是把连接、队列、记忆、工具调用和路由等基础设施封装起来，让开发者主要通过 YAML 配置构建代理。它更像工程化中间层而非新模型，强调多代理、持久记忆和成本控制。

## Problem
- 解决的问题：现有 WhatsApp 机器人通常只是把消息转发给 LLM，缺少**跨会话记忆、工具使用、多代理路由、限流与排队**等能力，难以支撑真实生产场景。
- 为什么重要：在群聊、高频消息和多类任务环境下，如果没有串行化、限流和记忆机制，系统会**响应混乱、成本失控、上下文丢失**。
- 对开发者而言，重复编写 WhatsApp 连接、重连、消息存储、工具执行等“胶水代码”降低了构建 agent 的效率与可维护性。

## Approach
- 核心方法：用一个**YAML 驱动的 agent 框架**来声明代理的人设、LLM、工具、路由、记忆、限流和人工接管规则，框架负责运行时编排。
- 系统机制上，消息流经过 **wu-cli WhatsApp 连接层 → 中间件 → 路由器 → 调度器 → Agent(tool loop)**；其中路由优先级为 **jid > group > keyword > default**。
- 为保证稳定性，框架对**同一聊天串行处理**、不同聊天并行处理，并提供**每 chat / 每 agent 的 cooldown 与 rate limit**，避免噪声群聊耗尽 API 预算。
- 为实现长期上下文，框架读取 wu-cli 的 SQLite 历史，并额外维护**会话摘要**与**用户画像**；当消息数超过阈值后，后台总结旧对话并在未来提示中复用，而不是每次塞入完整历史。
- 支持**工具调用、多步推理、定时任务、人工 handoff、自定义 TypeScript 工具、热重载**，并兼容 Anthropic、OpenAI 和 Ollama。

## Results
- 文本**没有提供标准基准测试或学术实验结果**，因此没有可核验的准确率、成功率、延迟或成本曲线数字。
- 给出的具体配置/能力数字包括：`conversationWindow` 示例为 **20/30**，`summarizeAfter` 为 **100** 条消息后摘要，`maxSteps` 最多 **10** 步工具调用。
- 限流示例为每 chat 在 **5 分钟 15 次** LLM 调用，`cooldownMs` 示例为 **5000 ms**。
- `fetchUrl` 使用 Jina 时，无 key 约 **20 RPM**，带 key 约 **500 RPM**。
- 运行环境要求包括 **Node.js >= 20**；首次启动通过扫描 **QR code** 绑定 WhatsApp，之后支持自动重连。
- 最强的具体主张是：该框架相较常见 WhatsApp bot glue code，提供了**多代理路由、跨会话记忆、串行聊天队列、限流/冷却、计划任务与人工接管**等完整 agent 基础设施。

## Link
- [https://github.com/ibrahimhajjaj/wa-agent](https://github.com/ibrahimhajjaj/wa-agent)
