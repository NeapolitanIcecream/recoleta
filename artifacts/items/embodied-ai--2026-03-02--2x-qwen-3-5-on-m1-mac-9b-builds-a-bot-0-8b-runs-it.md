---
source: hn
url: https://advanced-stack.com/fields-notes/qwen35-opencode-lm-studio-agentic-coding-on-m1.html
published_at: '2026-03-02T23:10:13'
authors:
- advanced-stack
topics:
- agentic-coding
- local-llm
- qwen
- lm-studio
- telegram-bot
relevance_score: 0.06
run_id: materialize-outputs
---

# 2x Qwen 3.5 on M1 Mac: 9B builds a bot, 0.8B runs it

## Summary
这篇文章不是学术论文，而是一份实操记录：作者展示了如何在一台 16GB 内存、约 6 年机龄的 MacBook M1 上，本地运行 OpenCode + LM Studio + Qwen3.5，完成一个可工作的 Telegram 机器人。核心结论是：虽然速度慢，但通过“大模型写代码、小模型跑回复”的分工，本地私有化 agentic coding 已经具备实用性。

## Problem
- 要解决的问题是：**能否在老旧、资源受限的本地硬件上，离线完成 agentic coding，并实际部署一个可用的小型应用**。
- 这很重要，因为很多小团队或个人开发者希望**代码与数据不离开本机/内网**，同时又想保留类似云端 coding agent 的工作流能力。
- 传统认知里，这类任务通常需要更强硬件或云服务；本文试图说明在 **M1 16GB** 这样的低门槛设备上也能“可用”。

## Approach
- 方法非常直接：使用 **OpenCode** 作为 agentic coding 前端，连接 **LM Studio 本地 OpenAI-compatible API**，全部在本机运行。
- 采用**双模型分工**：**Qwen3.5-9B-GGUF (Q4_K_M)** 负责规划、编辑和生成代码；**Qwen3.5-0.8B-GGUF** 负责 Telegram 机器人收到消息后的本地推理回复。
- 系统流程是：用户提示 OpenCode → 9B 模型生成/修改 `bot.py` → Telegram bot 接收消息 → 转发到 `http://localhost:1234/v1/chat/completions` → 0.8B 模型返回响应 → 机器人回复用户。
- 作者在一次短会话中，从“生成一个 `/ip` Telegram bot”进一步迭代到“桥接 Telegram 与本地 LM Studio 服务”，说明该方案支持简单的多轮需求 refinement。
- 为适应本地机器限制，作者将上下文窗口设为 **32k**，实际本次 coding session 使用约 **16k tokens**，并接近吃满 **16GB RAM**。

## Results
- 最核心结果是：在一台**约 6 年机龄的 MacBook M1（16GB RAM）**上，作者成功跑通了完整链路：**Qwen3.5-9B 生成可工作的 Telegram bot，随后将其改造成调用本地 Qwen3.5-0.8B API 的聊天机器人**。
- 配置细节包括：**OpenCode 1.2.10**、**LM Studio 0.4.6**、**Metal llama.cpp 2.5.1**、编码模型 **Qwen3.5-9B-GGUF Q4_K_M**、回复模型 **Qwen3.5-0.8B-GGUF**。
- 作者声称从想法到可工作流程只用了**一次短 session 加少量 follow-ups**，但**没有给出正式 benchmark、耗时、tokens/s、成功率或与其他模型/硬件的定量对比**。
- 给出的最具体资源数字是：配置了 **32k context window**，实际该任务使用约 **16k tokens**，并且基本**占满 16GB 内存**。
- 性能结论是定性的：作者明确表示在 M1 上“**很慢**”，但对**短编码循环、脚本生成、本地自动化、敏感/离线任务**来说“**绝对可用**”。
- 与基线比较方面，仅有弱对比：作者认为该方案**尚不能替代更高端 coding stack**，也**不替代 OpenClaw**；但相较完全依赖云端，它提供了更强的**隐私性与本地可操作性**。

## Link
- [https://advanced-stack.com/fields-notes/qwen35-opencode-lm-studio-agentic-coding-on-m1.html](https://advanced-stack.com/fields-notes/qwen35-opencode-lm-studio-agentic-coding-on-m1.html)
