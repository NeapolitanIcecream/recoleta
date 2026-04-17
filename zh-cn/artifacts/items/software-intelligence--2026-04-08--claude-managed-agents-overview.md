---
source: hn
url: https://platform.claude.com/docs/en/managed-agents/overview
published_at: '2026-04-08T23:48:50'
authors:
- NicoJuicy
topics:
- managed-agents
- agent-runtime
- code-execution
- developer-platform
- multi-agent
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Claude Managed Agents Overview

## Summary
## 摘要
Claude Managed Agents 是一个托管运行时，用于将 Claude 作为具备工具调用、代码执行、网页访问和持久化会话状态的自主代理来运行。它面向不想自己构建执行循环、容器运行时和事件处理管线的团队。

## 问题
- 构建一个自主的编程或研究代理，通常需要为代理循环、工具调用、运行时隔离、会话状态和流式输出做大量定制开发。
- 这些基础设施工作很重要，因为它会影响安全性、延迟、可靠性，以及开发者能否方便地在长时间运行的任务中引导或中断代理。
- 摘要内容将 Managed Agents 说明为一种绕过这类搭建工作、直接使用托管环境的方式。

## 方法
- 该产品将代理执行拆分为四个主要对象：代理定义、环境、会话和事件流。
- 代理定义保存模型、系统提示词、工具、MCP 服务器和技能，并通过 ID 在不同会话间复用这套配置。
- 环境是一个云容器，包含已安装的语言和软件包、网络访问规则以及挂载文件。
- 会话将代理和环境绑定起来，然后接收用户事件；与此同时，Claude 会调用工具、执行代码、浏览网页，并通过服务器发送事件（SSE）流式返回结果。
- 该系统还支持服务端事件历史记录、运行中引导或中断，以及内置的提示词缓存和压缩，以提高效率。

## 结果
- 摘要内容没有给出基准测试结果、评测分数、延迟数据或成本对比。
- 它称 Claude 可以在一个完全托管的环境中运行，并支持读取文件、执行命令、浏览网页和安全地执行代码。
- 它称内置了提示词缓存和压缩等性能特性来提高输出质量和效率，但没有给出具体的增益数据。
- 它提到 outcomes、multiagent 和 memory 处于研究预览阶段，这说明产品计划支持更高级的代理工作流，但摘要内容没有提供技术细节或验证结果。
- 该产品目前处于 beta 阶段，并要求使用 `managed-agents-2026-04-01` beta header。

## Problem

## Approach

## Results

## Link
- [https://platform.claude.com/docs/en/managed-agents/overview](https://platform.claude.com/docs/en/managed-agents/overview)
