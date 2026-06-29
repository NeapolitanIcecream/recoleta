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
Claude Managed Agents 是一个托管运行时，用于让 Claude 作为自主代理运行，带有工具、代码执行、网页访问和持久会话状态。它面向那些想要代理行为，但不想自己搭建执行循环、容器运行时和事件传递的团队。

## 问题
- 构建一个自主编程或研究代理，通常需要为代理循环、工具调用、运行时隔离、会话状态和流式输出做定制工作。
- 这些基础设施工作很重要，因为它会影响安全性、延迟、可靠性，以及开发者在长任务中多容易引导或中断代理。
- 这段摘要把 Managed Agents 描述为一种避开这套搭建方式、直接使用托管环境的办法。

## 方法
- 这个产品把代理执行拆成四个主要对象：代理定义、环境、会话和事件流。
- 代理定义保存模型、系统提示、工具、MCP 服务器和技能，然后通过 ID 在不同会话之间复用这组配置。
- 环境是一个云容器，包含已安装的语言和包、网络访问规则以及挂载文件。
- 会话把代理和环境绑定起来，然后接收用户事件；Claude 在此期间运行工具、执行代码、浏览网页，并通过服务器发送事件流返回结果。
- 系统还支持服务器端事件历史、中途引导或中断，以及内置的提示缓存和压缩来提高效率。

## 结果
- 这段摘要没有提供基准结果、评测分数、延迟数字或成本对比。
- 它声称 Claude 可以在一个完全托管的环境中运行，支持读文件、执行命令、浏览网页和安全执行代码。
- 它声称有提示缓存和压缩等内置性能功能，用来提高输出质量和效率，但没有给出实测提升。
- 它说明 outcomes、multiagent 和 memory 处于研究预览阶段，这说明产品计划支持更高级的代理工作流，但这段摘要没有技术细节或验证结果。
- 这个产品目前处于 beta 阶段，需要 `managed-agents-2026-04-01` beta header。

## Problem

## Approach

## Results

## Link
- [https://platform.claude.com/docs/en/managed-agents/overview](https://platform.claude.com/docs/en/managed-agents/overview)
