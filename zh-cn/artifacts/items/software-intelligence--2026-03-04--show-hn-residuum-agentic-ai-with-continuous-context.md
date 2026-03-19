---
source: hn
url: https://github.com/Grizzly-Endeavors/residuum
published_at: '2026-03-04T23:40:51'
authors:
- BearFlinn
topics:
- agent-framework
- continuous-memory
- multi-channel-agents
- context-management
- proactive-scheduling
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Residuum | Agentic AI with continuous context

## Summary
Residuum 是一个个人 AI 代理框架，主打“无会话边界”的连续上下文，让同一个代理跨 CLI、Discord 和 webhook 持续共享记忆。它试图解决传统 agent 每次新会话都要重新建立上下文、以及定时主动检查浪费 token 的问题。

## Problem
- 现有 AI agent 框架通常以**会话**为单位工作，新对话会丢失连续上下文，用户需要反复重述历史。
- 依赖 RAG 或固定记忆文件只能部分弥补，因为模型仍把每次对话当作孤立事件；较旧上下文还要求代理先“猜到要检索”。
- 常见 proactive/heartbeat 机制会定期触发完整 LLM 调用来检查是否有任务，带来不必要的 token 成本。

## Approach
- 用**单代理、单连续线程**替代会话式交互：把对话历史压缩成持续驻留上下文中的 observation log，而不是每次临时检索最近记忆。
- 对更早的历史细节，提供**深度检索**机制，结合 BM25 + 向量嵌入做混合搜索；近期工作记忆则直接保留在上下文中。
- 通过**多渠道汇聚**，将 CLI、Discord、webhooks 等消息统一接入同一个代理和同一份记忆，实现跨渠道连续对话。
- 用**YAML pulse scheduling**把定时/触发逻辑移出 LLM：用户定义检查内容、时间和通知去向，LLM 仅在到点时触发，并可用便宜模型执行。
- 系统采用**file-first** 与模块化设计，状态保存在可读文件中，兼容 OpenClaw skills，并支持多家模型提供商与故障切换。

## Results
- 文本**没有提供标准基准测试、公开数据集或正式实验指标**，因此没有可核验的定量 SOTA 结果。
- 相比 OpenClaw，作者声称解决了其“**两天左右上下文悬崖**”问题：旧上下文不再主要依赖代理先猜测并搜索，而是通过持续 observation log 保持可用。
- 相比 OpenClaw 每 **30 分钟**触发一次完整 LLM heartbeat，Residuum 声称通过 YAML pulse scheduling 去掉了这类由 LLM 承担的调度逻辑，从而减少 token 浪费；但未给出节省比例。
- 相比 NanoClaw（文中称约 **500 行 TypeScript**、偏极简和容器隔离），Residuum强调自己的差异化能力包括持续记忆压缩、结构化主动调度、后台任务委派与模型分层、多渠道统一线程。
- 工程层面给出的具体事实包括：Rust 实现；支持 Linux（x86_64、aarch64）与 macOS Apple Silicon；要求 Rust **1.85+**；支持 Anthropic、OpenAI、Google、Ollama，并内建 provider failover。

## Link
- [https://github.com/Grizzly-Endeavors/residuum](https://github.com/Grizzly-Endeavors/residuum)
