---
source: hn
url: https://github.com/ibrahimhajjaj/wa-agent
published_at: '2026-03-08T23:40:23'
authors:
- ibrahimwithi
topics:
- whatsapp-agents
- agent-framework
- multi-agent-routing
- conversation-memory
- tool-using-agents
relevance_score: 0.86
run_id: materialize-outputs
---

# Show HN: Wa-agent – Framework for building AI agents on WhatsApp

## Summary
wa-agent 是一个用于在 WhatsApp 上构建自治 AI 代理的工程框架，重点解决消息接入、记忆、工具调用、路由和运营控制等基础设施问题。它把代理行为主要配置为 YAML，让开发者更快搭建多代理 WhatsApp 应用。

## Problem
- 现有很多 WhatsApp 机器人只是把消息简单转发给 LLM，缺少跨会话记忆、工具使用、多代理路由和生产级流控能力。
- 在高消息量群聊或多用户场景中，如果没有队列、限流和冷却机制，容易导致响应混乱、成本失控或系统不稳定。
- 为 WhatsApp 代理重复编写连接、上下文管理、调度和人工接管等胶水代码，降低了开发效率，也不利于可靠上线。

## Approach
- 用 **YAML 配置**定义代理的人设、LLM、工具、路由、记忆、触发器和人工接管规则，框架负责底层运行时。
- 基于 **Vercel AI SDK v6** 执行代理循环与工具调用，基于 **wu-cli** 处理 WhatsApp 连接、重连和消息存储。
- 采用一条清晰流水线：消息过滤与 handoff 检查 → 路由（`jid > group > keyword > default`）→ 调度器（冷却、限流、按聊天串行队列）→ 代理执行（上下文构建、tool loop、回复、后台摘要与用户画像更新）。
- 通过 **会话摘要 + 用户画像** 实现跨会话记忆：超过阈值后对旧消息后台总结，并持续提取用户事实，避免每次都塞入完整历史。
- 支持 **多代理**、**自定义工具**、**计划任务**、**热重载**、**人工升级** 以及多 LLM 后端（Anthropic/OpenAI/Ollama）。

## Results
- 文中**没有提供标准基准测试或学术实验结果**，未报告如准确率、成功率、延迟、成本或人工评测分数等定量指标。
- 提供了明确的可配置运行上限与机制：如 `maxSteps: 10`（每条消息最多 10 步工具调用）、`rateLimitPerWindow: 15`（每聊天 5 分钟最多 15 次 LLM 调用）、`cooldownMs: 5000`（5 秒冷却）。
- 记忆机制给出具体默认/示例参数：`conversationWindow: 20/30`、`summarizeAfter: 100`、`userProfiles: true`，主张能在不注入完整历史的情况下保留长期上下文。
- 抓取 URL 能力给出吞吐数字：Jina 无 key 时约 **20 RPM**，有 key 时约 **500 RPM**。
- 声称的最强工程性收益包括：同一聊天**严格串行**处理、不同聊天**并行**处理；支持自动重连、按聊天/代理限流、群聊预算保护，以及人工接管与定时任务。

## Link
- [https://github.com/ibrahimhajjaj/wa-agent](https://github.com/ibrahimhajjaj/wa-agent)
