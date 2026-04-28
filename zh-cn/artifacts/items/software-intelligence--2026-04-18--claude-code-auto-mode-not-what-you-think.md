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
这篇文章认为，Anthropic 的 Claude Code Auto Mode 证明了面向代理工具使用的运行时安全这一类别有价值，但其公开的 17% 漏报率也说明，只靠一层提供商侧分类器还不够。文章最重要的技术结论是 Anthropic 的“对推理盲”设计：运行时裁决层应该检查请求和工具动作，而不是代理自己的解释或工具输出。

## 问题
- 自主编码代理现在会在没有人工逐步审批的情况下执行一长串文件读取、写入、shell 命令和 API 调用，这让不安全动作漏过检查的机会变多。
- 单一、提供商原生的运行时分类器只能覆盖它自己的产品表面。它看不到混合厂商流水线、跨代理交接、检索输入或第三方工具输出。
- Anthropic 报告 Auto Mode 对真实危险的过度积极动作有 17% 的漏报率。这个漏报率很关键，因为被拦截或漏掉的工具调用发生在真实、未审查的执行过程中，不只是离线基准分数。

## 方法
- Anthropic 的 Auto Mode 在 Claude Code 中用服务器端分类器取代了逐个工具的人类确认，在执行前批准或阻止每一次工具调用。
- 这个分类器在设计上对推理盲：它能看到用户消息和计划中的工具调用，但看不到 Claude 自己的消息或工具输出。
- 这种设计减少了文中提到的两条攻击路径：代理自我辩护，以及通过恶意工具输出操纵代理向裁决器描述动作的方式。
- 文章更广泛的主张是纵深防御：保留提供商原生的动作过滤器，然后在输入边界再加一层与提供商无关的运行时防护，在模型读取文件、RAG chunks、MCP 工具输出和跨代理消息之前先进行扫描。
- 作为第二层的一个例子，作者把 Sunglasses 描述为基于模式的摄取过滤，具备可检查的匹配结果、可审计性，并支持跨代理注入、检索投毒、工具输出投毒和与 MCP 相关的攻击。

## 结果
- Anthropic 公布的数据是，对**真实的过度积极危险动作**有 **17% 的漏报率**。文章把这视为最关键的实证结果，也是增加另一层安全防护的主要理由。
- 文章称 Auto Mode 于 **2026 年 3 月 24 日** 发布，Anthropic 的工程深度解析于 **2026 年 3 月 25 日** 跟进发布。
- 对于与提供商无关的防护层示例，文中一处写的是 **49 个类别中的 328 条模式**，而更早一处写的是 **48 个类别中的 269 条模式**。这个数量在原文内部似乎不一致。
- 文中点名的攻击面包括 **跨代理信任交接**、**检索投毒**、**工具输出“failure-as-license”绕过**，以及提供商原生分类器无法完整观察的 **多厂商或跨框架流水线**。
- 文章对 Sunglasses 给出了一项具体性能说法：每次扫描约 **0.26 ms**。
- 没有正面对比基准测试比较“Auto Mode 加第二层”和“仅 Auto Mode”的差异。摘录中最有力的量化说法仍然是 Anthropic 自己公布的已部署分类器 **17% 漏报率**。

## Problem

## Approach

## Results

## Link
- [https://sunglasses.dev/blog/auto-mode-validates-runtime-security](https://sunglasses.dev/blog/auto-mode-validates-runtime-security)
