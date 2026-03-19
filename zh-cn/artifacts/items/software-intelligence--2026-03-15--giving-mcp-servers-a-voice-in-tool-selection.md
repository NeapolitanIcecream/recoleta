---
source: hn
url: https://divanv.com/post/server-side-tool-gating/
published_at: '2026-03-15T22:36:22'
authors:
- divanvisagie
topics:
- mcp
- tool-selection
- tool-gating
- agent-infrastructure
- context-optimization
relevance_score: 0.85
run_id: materialize-outputs
language_code: zh-CN
---

# Giving MCP servers a voice in tool selection

## Summary
这篇文章提出一种针对 MCP（Model Context Protocol）工具选择的轻量改进：让服务器通过一个约定俗成的 `_tool_gating` 工具参与每轮工具筛选。其目标是减少无关工具进入提示词、降低误选概率，并在确定性命令场景下直接跳过模型调用。

## Problem
- MCP 服务器目前只能注册工具并提供 schema，但**无法影响模型如何选工具**；结果是无关工具也会被一并加载进上下文，浪费 token 并增加误选风险。
- 当工具数量增多时，LLM 的工具选择准确率会明显下降；文中引用研究称：**超过约 20 个工具后性能显著变差**，而“全部工具都加载”的朴素基线**准确率可低至约 14%**。
- 这很重要，因为多服务器 MCP 生态下工具数量会快速膨胀；作者举例一个 weather MCP 就会带来 **20,000 tokens** 的额外上下文，既贵又拖慢响应。

## Approach
- 核心机制非常简单：服务器暴露一个约定名称的工具 **`_tool_gating`**；客户端若在 `tools/list` 中发现它，就在**每次请求、构建给模型的工具列表之前**先调用它。
- `_tool_gating` 返回两类裁决：**`exclude`**（本轮把某些工具从模型上下文中移除）和 **`claim`**（服务器声明该请求应由某个工具直接处理，客户端可**跳过模型**直接调用该工具）。默认未提及的工具即 `include`。
- 该方案**不需要修改 MCP 规范**、**不需要 capability flag**，仅依赖已有的 tool 机制和少量客户端逻辑改造。
- 作者原型实现中，服务器侧采用**基于关键词/模式的简单规则**而非 ML：例如精确匹配 `/projects`、`/list` 直接 claim；识别只读意图时排除 `notes_write`、`notes_edit`、`project_new`；无 archive 意图时排除 `project_archive`。
- 客户端流程为：连接时探测 `_tool_gating`；每轮先向所有支持 gating 的服务器请求裁决；若有 `claim` 则直接调用工具并返回；否则对工具列表做 `exclude` 过滤后再发送给模型。若 claim 失败，还可回退到正常 LLM 路径。

## Results
- 作者在自己的 Python MCP 服务器 **pman-mcp** 和 Rust 客户端 **chell** 上做了原型验证；在**只读请求**场景下，能够从每轮候选中**移除 4 个工具**。
- 上述过滤带来约 **318 tokens/turn** 的节省，这是文中给出的直接实测数字。
- 对于 slash commands（如 `/projects`、`/new ...`），系统可通过 **claim** 机制**完全不调用模型**，从而以更确定、更低延迟的方式完成命令；文中未给出具体时延数字。
- 作者认为这是“小而稳”的优化，但若被更多工具和客户端采用，潜在收益可扩展到**数千甚至数百万 tokens 的节省**；这一点是前瞻性主张，**未提供系统性大规模实验数据**。
- 与 OpenAI Agents SDK `tool_filter`、Google ADK、Portkey embedding-based filter、STRAP megatool 等方案相比，本文最强的具体主张是：**过滤判断应尽量由最了解工具能力的服务器端来做，而不是完全放在客户端或外部框架中**。

## Link
- [https://divanv.com/post/server-side-tool-gating/](https://divanv.com/post/server-side-tool-gating/)
