---
source: hn
url: https://sunglasses.dev/blog/auto-mode-validates-runtime-security
published_at: '2026-04-18T23:03:33'
authors:
- azrollin
topics:
- runtime-security
- agentic-coding
- tool-call-approval
- defense-in-depth
- prompt-injection
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Claude Code "AUTO MODE" – Not what you think

## Summary
## 摘要
这篇文章认为，Anthropic 的 Claude Code Auto Mode 证明了运行时安全在代理工具使用场景中的价值，但它公布的 17% 假阴性率也说明，单靠一个提供方侧分类器还不够。最重要的技术结论是 Anthropic 的“推理盲”设计：运行时审查器应该检查请求和工具动作，而不是代理自己的解释或工具输出。

## 问题
- 自主编码代理现在会在没有逐步人工确认的情况下执行很长的文件读取、写入、shell 命令和 API 调用链，这让未被拦截的不安全动作有更多机会通过。
- 单个提供方原生运行时分类器只能覆盖自己的产品表面。它看不到混合供应商管道、跨代理交接、检索输入或第三方工具输出。
- Anthropic 报告，Auto Mode 在真实危险的激进行为上有 17% 的假阴性率。这个漏检率很重要，因为被阻止或漏掉的工具调用影响的是正在运行、未经审查的执行，而不只是离线基准分数。

## 方法
- Anthropic 的 Auto Mode 用服务器端分类器取代了 Claude Code 中逐工具的人类确认，在执行前批准或阻止每次工具调用。
- 这个分类器按设计是推理盲的：它能看到用户消息和计划中的工具调用，但看不到 Claude 自己的消息或工具输出。
- 这个设计减少了文章里提到的两条攻击路径：代理自我辩护，以及通过恶意工具输出操纵它对动作的描述，从而影响审查结果。
- 文章更大的主张是分层防御：保留提供方原生的动作过滤器，再在输入边界加第二层与提供方无关的运行时过滤，在模型读取之前扫描文件、RAG 分块、MCP 工具输出和跨代理消息。
- 作为第二层的例子，作者把 Sunglasses 描述为基于模式的摄取过滤，带可检查的匹配、可审计性，以及对跨代理注入、检索污染、工具输出污染和 MCP 相关攻击的支持。

## 结果
- Anthropic 公布的数字是，**17% 的假阴性率**，对象是**真实的激进行为中的危险动作**。文章把这视为关键实证结果，也是加入另一层安全机制的主要理由。
- 文章说 Auto Mode 在 **2026 年 3 月 24 日**上线，Anthropic 的工程深度解析在 **2026 年 3 月 25 日**发布。
- 作为提供方无关层的例子，文本在一个部分写的是 **328 个模式，49 个类别**；而前一部分写的是 **269 个模式，48 个类别**。这个计数在源文本里不一致。
- 文中点名的攻击面包括 **跨代理信任交接**、**检索污染**、**工具输出中的“故障即授权”绕过**，以及 **多供应商或跨框架管道**，这些都不是提供方原生分类器能完整看到的。
- 文章给出 Sunglasses 的一个具体性能说法：每次扫描约 **0.26 ms**。
- 文中没有把 Auto Mode 加第二层与只用 Auto Mode 做直接对比的基准测试。这个摘录里最强的量化结论是 Anthropic 对已部署分类器给出的 **17% 漏检率**。

## Problem

## Approach

## Results

## Link
- [https://sunglasses.dev/blog/auto-mode-validates-runtime-security](https://sunglasses.dev/blog/auto-mode-validates-runtime-security)
