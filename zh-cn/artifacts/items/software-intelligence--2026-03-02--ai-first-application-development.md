---
source: hn
url: https://benkaiser.dev/ai-first-software-development/
published_at: '2026-03-02T23:27:35'
authors:
- benkaiser
topics:
- mcp
- ai-first-apps
- llm-tools
- consumer-agents
- software-development
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# AI First Application Development

## Summary
本文提出“AI First Application Development”观点：面向消费者的 MCP（Model Context Protocol）服务器和聊天客户端，可能成为应用的主要交互层，而传统 Web/移动/桌面 UI 退居次要。作者通过 Joey MCP Client 与 Mob CRM 两个实例，说明以 LLM+MCP 为中心的应用开发与使用方式。

## Problem
- 文章要解决的问题是：**普通消费者难以直接使用远程 MCP 服务器**，目前主流平台多将 MCP 能力限制在付费、开发者模式或企业订阅中，阻碍了 AI 原生应用的普及。
- 这很重要，因为 MCP 可以把多个独立服务整合进一次自然语言对话中，让用户直接“说需求”而不是在多个应用和界面之间来回切换。
- 对开发者而言，传统 UI 开发成本高、反馈链路长，而作者认为 AI-first 应用若以 MCP 为主入口，可以降低构建和迭代门槛。

## Approach
- 核心方法很简单：**把应用能力做成可被 LLM 调用的 MCP 服务器，再用一个聊天客户端把模型和这些服务器连接起来**，让用户通过对话完成原本需要多步 UI 操作的任务。
- 作者实现了一个消费者可用的聊天界面 **Joey MCP Client**：通过 OpenRouter 接入多种 LLM，用户手动配置远程 MCP 服务器，并可为每个对话选择具体模型和 MCP 组合。
- Joey 支持多 MCP 同时调用、图片输入/输出、对 MCP 服务器的 OAuth 认证，并强调无遥测、可自行构建源码、按量付费等特性，以降低使用门槛和隐私顾虑。
- 为验证“AI-first application”形态，作者还构建了 **Mob CRM**：一个主要通过 MCP 访问的个人 CRM，用户只需用自然语言描述社交互动，LLM 再通过若干工具调用自动创建联系人、关系与活动记录。
- 作者进一步主张：开发 MCP 服务器类似开发 CLI/REST 工具，因其文本化、易测试、易被 LLM 解释，因此比构建完整 Web/移动 UI 更适合 AI 辅助开发。

## Results
- 文中**没有提供正式实验、基准数据或量化评测结果**，因此没有可报告的准确率、延迟、成本或与现有系统的数值对比。
- 最强的具体效果声明来自 Mob CRM 示例：一次自然语言输入如“我今天见了 John…还认识了 Jane…聊了 slurpees”，可由 LLM 触发**少量工具调用**，自动完成联系人创建、关系建立和活动笔记记录；作者将其对比为省去在传统 CRM 中进行“**30 different clicks**”的手工 UI 操作。
- Joey MCP Client 的实际功能性声明包括：支持**多个 MCP 服务器同时使用**、支持**图片**、支持**OAuth 到 MCP 服务器**、支持用户按会话选择 **OpenRouter LLM + MCP servers**。
- 作者的主要“突破性”主张不是实验结果，而是产品与范式层面的判断：未来消费者将更多通过支持 MCP 的聊天界面使用应用，企业“像今天需要移动应用一样，明天将需要 MCP 服务器”。

## Link
- [https://benkaiser.dev/ai-first-software-development/](https://benkaiser.dev/ai-first-software-development/)
