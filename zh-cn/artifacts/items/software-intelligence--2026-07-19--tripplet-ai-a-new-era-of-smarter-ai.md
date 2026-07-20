---
source: hn
url: https://www.getsonoma.lol/
published_at: '2026-07-19T22:34:20'
authors:
- htmghrceceg
topics:
- code-intelligence
- software-foundation-model
- agentic-tool-use
- human-ai-interaction
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Tripplet AI – a new era of smarter AI

## Summary
## 摘要
Tripplet AI 提供统一工作区，将聊天、代码执行、网络研究、记忆、知识管理和外部工具连接整合到四个专用模型中。摘录介绍了产品功能和开发者接口，但没有提供独立的基准测试或用户研究证据。

## 问题
- 用户原本需要分别使用对话式 AI、实时网络研究、编程、持久化知识管理和工作应用等不同工具。
- 可靠的代码辅助需要实际执行并报告错误，而不只是生成代码输出。
- 该产品面向软件和研究工作流，因为它旨在让用户切换模型、运行代码、检索最新信息并通过已连接的工具执行操作时保留上下文。

## 方法
- Tripplet 在四个具有不同角色的模型之间分配对话，包括推理、研究、通用和轻量交互模型，同时保留对话上下文。
- 它整合了网络搜索、持久化记忆、内置知识库、流式响应，以及 `think`、`deep-research`、`web-search` 和 `study` 等可选模式。
- 它在沙盒中执行 Python，并可提供用于基于 shell 的工作的沙盒 Linux 虚拟机，展示实际输出和错误。
- 它通过范围受限且可撤销的访问权限连接 GitHub、Gmail 和 Notion 等服务，并为开发者构建的代理提供流式 API、MCP 服务器和 OAuth。

## 结果
- 摘录没有提供准确率、延迟、成本、采用情况或基准测试结果等定量数据。
- 产品声称在一次对话中提供四个专用模型，并表示用户可以在这些模型之间切换而不会丢失上下文。
- 展示的 Python 示例计算了 50 以下素数之和，结果为 `328`，体现了执行输出，而非基准比较。
- 该服务声称支持逐 token 的服务器发送事件流式传输、最新网络结果、跨对话持久化记忆、沙盒执行以及与外部应用的集成；本文未对这些声明进行独立评估。

## Problem

## Approach

## Results

## Link
- [https://www.getsonoma.lol/](https://www.getsonoma.lol/)
