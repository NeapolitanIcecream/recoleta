---
source: hn
url: https://github.com/computeruseprotocol/computeruseprotocol
published_at: '2026-03-04T23:15:00'
authors:
- k4cper-g
topics:
- desktop-ui-agents
- accessibility-tree
- cross-platform-protocol
- llm-optimization
- computer-use
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: A universal protocol for AI agents to interact with any desktop UI

## Summary
这项工作提出了 Computer Use Protocol（CUP），一个让 AI 智能体以统一方式感知和操作任意桌面/移动/Web UI 的跨平台协议。其核心价值是把分裂的辅助功能树表示、动作语义和平台差异统一起来，并用极紧凑的文本格式显著降低 LLM 上下文开销。

## Problem
- 现有 Windows、macOS、Linux、Web、Android、iOS 的 UI 辅助功能接口各不相同，导致每个 agent 框架都要重复实现一套平台适配与翻译层。
- 对 AI agent 来说，UI 结构通常以 JSON 等冗长格式提供，容易占满上下文窗口，限制复杂界面的感知与推理。
- 缺少统一动作语义会让跨平台执行变得脆弱；如果不能“一次编写，到处运行”，桌面智能体生态很难扩展。

## Approach
- 提出一个统一的 UI 表示协议：用基于 ARIA 的角色体系，把不同平台的原生 accessibility tree 规范化为同一种 JSON envelope。
- 设计面向 LLM 的紧凑文本编码，把同一棵 UI 树压缩成更短的可读文本，方便模型在有限上下文中处理复杂界面。
- 定义跨平台共享的语义层，包括 59 个标准角色、16 个状态标记、15 个规范动作动词，由各平台 SDK 映射到原生 API 执行。
- 为避免信息损失，在统一表示之外保留原生平台属性到 `node.platform.*`，兼顾标准化与可追溯性。
- 通过 SDK 与 MCP server，把“抓取 UI 树 + 执行动作”的能力直接暴露给 Claude、Copilot 等 AI agent 使用。

## Results
- 声称实现 **一个格式覆盖 6 类平台**：Windows、macOS、Linux、Web、Android、iOS，使 agent 逻辑可跨平台复用。
- 声称紧凑格式相对 JSON 可实现约 **97% 体积/Token 缩减**，并称对 CUA/LLM 优化后可比“次优接近格式”少约 **15x tokens**。
- 协议层面给出明确规范：**59 个角色**、**16 个状态**、**15 个规范动作**，并提供跨平台 role mapping 与 schema。
- 文本未提供标准学术基准、数据集或对比实验，因此**没有可验证的任务成功率、延迟、准确率等定量评测结果**。
- 最强的具体主张是：通过统一表示层一次性解决跨平台 UI 翻译问题，并在不丢失原生属性的前提下显著降低 LLM 处理 UI 的上下文成本。

## Link
- [https://github.com/computeruseprotocol/computeruseprotocol](https://github.com/computeruseprotocol/computeruseprotocol)
