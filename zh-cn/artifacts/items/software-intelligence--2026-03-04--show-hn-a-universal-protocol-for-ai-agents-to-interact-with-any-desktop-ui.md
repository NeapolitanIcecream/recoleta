---
source: hn
url: https://github.com/computeruseprotocol/computeruseprotocol
published_at: '2026-03-04T23:15:00'
authors:
- k4cper-g
topics:
- ui-automation
- ai-agents
- accessibility-tree
- cross-platform-protocol
- llm-optimization
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: A universal protocol for AI agents to interact with any desktop UI

## Summary
CUP 提出一种统一协议，让 AI 代理能用同一种方式感知并操作任意桌面与移动/Web UI。其核心价值是把跨平台碎片化的无障碍树表示、动作语义和代理接入方式统一起来，并针对 LLM 上下文做了强压缩。

## Problem
- 各平台 UI 无障碍接口彼此割裂：Windows UIA、macOS AXUIElement、Linux AT-SPI2、Web ARIA、Android、iOS 都有不同角色体系与属性表示。
- 结果是每个 agent 框架都要重复实现一次“平台 UI → 代理可理解表示”的翻译层，难以复用，跨平台 agent 逻辑难以一次编写到处运行。
- 对 LLM 而言，原始 JSON/UI 树过于冗长，复杂界面很容易超出上下文窗口，限制真实桌面自动化与智能交互能力。

## Approach
- 定义一个通用的 JSON envelope/schema，把不同平台捕获到的原生 accessibility tree 归一化为同一结构，包括 app、screen、tree、role、state、action、bounds 等字段。
- 使用 59 个 ARIA 派生角色、16 个状态标记、15 个规范动作动词，作为跨平台统一语义层；SDK 再把这些标准语义映射到各平台原生 API。
- 提供一种面向 LLM 的紧凑文本编码，把同一 UI 树从 JSON 压缩成短文本行表示，目标是在尽量不丢信息的前提下显著减少 token 消耗。
- 保留 `node.platform.*` 原生属性，避免规范化导致的信息损失；同时配套 SDK 与 MCP server，使 Claude、Copilot 等代理能直接接入感知与执行能力。

## Results
- 论文/项目声称紧凑格式相对 JSON 约**缩小 97%**，用于 LLM/CUA 时更适合上下文窗口。
- 声称相对“下一个最接近的格式”可实现约**15x fewer tokens**，但摘录中未给出具体基线名称、实验设置或完整评测表。
- 统一了**6 类平台**映射：Windows、macOS、Linux、Web、Android、iOS。
- 协议语义规模包括**59** 个角色、**16** 个状态、**15** 个规范动作，用于跨平台交互抽象。
- 提供了 SDK 与 MCP server 集成能力，支持代理直接捕获原生 UI 树并执行动作；但摘录中**没有**任务成功率、延迟、代理基准测试或真实桌面 benchmark 的量化结果。

## Link
- [https://github.com/computeruseprotocol/computeruseprotocol](https://github.com/computeruseprotocol/computeruseprotocol)
