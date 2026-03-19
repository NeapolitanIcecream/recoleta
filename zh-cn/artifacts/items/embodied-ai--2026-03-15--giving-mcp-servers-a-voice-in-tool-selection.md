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
- agent-inference
- token-efficiency
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Giving MCP servers a voice in tool selection

## Summary
这篇文章提出一种面向 MCP 的“服务器端工具门控”机制，让服务器在每次请求时先参与筛选或直接认领工具调用，从而减少上下文噪声、节省 token，并降低模型误选工具的概率。

## Problem
- MCP 服务器虽然最了解自身工具能力，但传统流程中工具选择完全由模型根据工具描述“猜测”，服务器本身无法参与路由决策。
- 当工具数量增多时，所有工具都被加载进提示词会显著增加 token 开销，并让工具选择准确率下降；文中引用研究称，超过约 20 个工具后，朴素“全部加载”基线准确率可低至约 **14%**。
- 某些服务器工具集极大，例如一个天气 MCP 会增加约 **20,000 tokens**，造成明显成本与误路由问题。

## Approach
- 提出一个无需修改 MCP 规范的方案：服务器暴露一个约定俗成的工具 **`_tool_gating`**，客户端若检测到它，就在每次请求、构建给模型的工具列表前先调用它。
- 服务器返回少量“例外裁决”：**exclude** 表示从本轮模型上下文移除某些工具；**claim** 表示服务器断言应直接处理该请求，客户端可跳过模型直接调用目标工具。
- 该机制把筛选智能放回“最懂工具的人”——服务器端，而不是仅依赖客户端 SDK、外部 embedding 过滤器或 megatool 合并策略。
- 作者的实现使用非常简单的规则逻辑而非机器学习：关键词/前缀匹配决定哪些命令可直接 claim，哪些写入类工具在只读意图下应被 exclude；不确定时默认保留工具。
- 客户端侧改动很小：连接时检测 `_tool_gating` 并对 LLM 隐藏它；每轮先向所有支持门控的服务器查询，再执行直接调用或对工具列表做按轮过滤；若 claim 失败则回退到正常 LLM 路径。

## Results
- 在作者测试环境中，通过新增一个门控工具并修改客户端预调用逻辑，针对只读相关请求可从上下文中移除 **4 个工具**。
- 该改动在测试中带来约 **318 tokens/turn** 的节省。
- 对于斜杠命令（如确定性的命令式请求），方案可**完全跳过模型调用**，以直接工具调用替代 LLM 回合。
- 文中未提供标准数据集、系统性 benchmark、A/B 实验或显著性检验结果，因此**没有严格的通用定量评测**。
- 最强的具体主张是：该方案**无需修改 MCP 规范**、只需“一个约定工具 + 少量客户端逻辑”，即可减少提示词负担、降低误选风险，并在更广泛采用时潜在节省“**数千到数百万 tokens**”。

## Link
- [https://divanv.com/post/server-side-tool-gating/](https://divanv.com/post/server-side-tool-gating/)
