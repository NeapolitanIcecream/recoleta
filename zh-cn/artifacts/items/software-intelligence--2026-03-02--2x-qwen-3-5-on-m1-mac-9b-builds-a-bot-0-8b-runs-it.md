---
source: hn
url: https://advanced-stack.com/fields-notes/qwen35-opencode-lm-studio-agentic-coding-on-m1.html
published_at: '2026-03-02T23:10:13'
authors:
- advanced-stack
topics:
- agentic-coding
- local-llm
- qwen3.5
- lm-studio
- telegram-bot
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# 2x Qwen 3.5 on M1 Mac: 9B builds a bot, 0.8B runs it

## Summary
这是一篇实践型技术报告，展示了如何在一台16GB 内存、约6年的 MacBook M1 上，本地运行 OpenCode + LM Studio，用 Qwen3.5-9B 做代理式编码、Qwen3.5-0.8B 做聊天推理。核心结论是：虽然速度慢，但对小型、私有、离线的软件生成任务已经可用。

## Problem
- 解决的问题是：如何在**老旧消费级硬件**上，本地完成代理式编码与应用运行，而不依赖云端模型。
- 这很重要，因为很多小团队或个人开发者需要**数据隐私、离线可用性、低基础设施门槛**，但通常认为这类工作流需要更强硬件或云服务。
- 文中还隐含回答了一个工程问题：是否可以把**较大模型用于代码生成**、把**更小模型用于运行时对话**，从而降低本地部署成本。

## Approach
- 使用分工式双模型架构：OpenCode 调用本地 **Qwen3.5-9B-GGUF (Q4_K_M)** 做代码规划、编辑和迭代；Telegram 机器人再把用户消息转发给本地 API 后的 **Qwen3.5-0.8B-GGUF** 生成回复。
- 推理后端是 **LM Studio 0.4.6 + Metal llama.cpp 2.5.1**，通过 OpenAI 兼容接口 `http://localhost:1234/v1/chat/completions` 暴露服务，形成统一接入层。
- 实际任务链路很简单：用户提示 OpenCode → 9B 模型生成/改写 `bot.py` → Telegram bot 接收消息 → 转发到本地 LM Studio 服务 → 0.8B 模型返回结果 → bot 回传给 Telegram。
- 作者先让模型生成一个简单 `/ip` 机器人，再要求它改写为 Telegram 与本地 LM Studio 之间的桥接器，验证了从“想法”到“可运行程序”的短回路。

## Results
- 在 **MacBook M1（16GB RAM，约6年机龄）** 上成功跑通完整流程：**Qwen3.5-9B** 负责代理式编码，**Qwen3.5-0.8B** 负责本地聊天回复。
- 作者声称在**一次简短会话、少量 follow-up** 中，就从需求描述生成了**可工作的 Telegram bot**，并进一步改造成连接本地 OpenAI 兼容服务的版本。
- 运行配置给出了具体数字：**32k context window**，本次编码会话实际使用约 **16k tokens**，并且“基本吃满” **16GB RAM**。
- 文中没有提供严格基准测试，例如**延迟、吞吐、成功率、HumanEval/SWE-bench 等量化指标**，因此没有标准化性能对比数据。
- 最强的具体结论是工程可行性：即使在老 M1 上，针对**短代码循环、脚本生成、本地自动化、敏感离线任务**，该本地代理式软件生产工作流“虽然慢，但可用”。

## Link
- [https://advanced-stack.com/fields-notes/qwen35-opencode-lm-studio-agentic-coding-on-m1.html](https://advanced-stack.com/fields-notes/qwen35-opencode-lm-studio-agentic-coding-on-m1.html)
