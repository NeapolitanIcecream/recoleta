---
source: hn
url: https://zserge.com/posts/socreates/
published_at: '2026-05-27T23:41:26'
authors:
- croottree
topics:
- coding-agents
- code-review
- llm-tool-use
- agent-loop
- context-management
- human-ai-interaction
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# A non-coding coding agent

## Summary
## 摘要
Socreates 是一个小型 coding-agent 原型，它通过工具调用检查工作区，但不让模型改代码。文章说明了 agent 循环、工具接口、提示词、上下文裁剪和会话记忆，没有基准测试结果。

## 问题
- Coding agents 可能会写出大量代码，带来不安全的改动，并制造后续维护工作，开发者还得自己调试。
- 开发者可能希望 LLM 帮忙做审查、查错和设计施压，但不想给模型写入权限。
- Agent 实现还需要控制上下文、安全执行工具，并保存会话状态，才能跨轮次工作。

## 方法
- 这个 agent 运行一个简单循环：加入用户消息，把 system prompt 和历史记录发给 LLM，执行请求的工具调用，把工具结果回传，然后在模型返回最终答案时停止。
- 它使用一个与模型无关的 LLM 接口，支持聊天消息、工具 schema、工具调用和 token 用量，并为 Ollama 和 OpenAI 兼容 API 提供适配器。
- System prompt 禁止代码、代码片段和伪代码；它要求模型引用文件行号，提出批判性问题，并在较少的工具轮次内完成回答。
- 工具集有 4 个动作：list_files、read_file、search 和 run_command；run_command 默认需要用户确认，除非开启自动批准。
- 上下文控制会把过长的工具输出裁剪到 400 个字符，在历史记录超过估算的 16,000 个 token 时丢弃较早轮次，并把完整会话记录存到 .socreates/session.json。

## 结果
- 文章没有报告定量基准、准确率、用户研究或对照比较。
- 这个原型使用 1 个控制循环、4 个工具，没有依赖。
- 循环在 10 次迭代后停止；提示词要求模型在 2 到 3 轮工具调用内回复，并尽量在 1 到 2 次调用内读取文件。
- 历史记录上限是估算的 16,000 个 token；每个工具输出上限是 16K 字符，约 4K token。
- search 最多返回 30 个匹配项，read_file 会为长文件返回续读提示。
- 作者测试了 qwen、llama、gemma 和 DeepSeek API，结果不一致；还给出了一段样例审查，指出在 llm.Chat 返回错误后，可能存在历史污染 bug。

## Problem

## Approach

## Results

## Link
- [https://zserge.com/posts/socreates/](https://zserge.com/posts/socreates/)
