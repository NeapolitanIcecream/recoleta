---
source: hn
url: https://news.ycombinator.com/item?id=47282711
published_at: '2026-03-06T23:54:47'
authors:
- janaksunil
topics:
- mcp-server
- developer-tools
- workflow-integration
- cost-optimization
- human-ai-interaction
relevance_score: 0.57
run_id: materialize-outputs
---

# Show HN: MCP server that finds dev tool credits in your workflow

## Summary
这是一个接入 Claude Code 的 MCP 服务器，用来在开发者评估新工具或扫描现有依赖时，提示可用的 credits、折扣或优惠。它试图把“找开发工具优惠”嵌入真实开发工作流中，同时避免变成 IDE 里的广告噪音。

## Problem
- 开发者在采用或续费开发工具时，常常不知道是否存在可用的 credits、折扣或促销，导致额外成本支出。
- 如果优惠提示触发过于频繁或与当前任务无关，就会像广告一样打断编程流程，降低工具可接受性。
- 这件事之所以重要，是因为开发工具订阅越来越多，若能在决策时点提供相关优惠信息，可能直接降低团队软件成本。

## Approach
- 核心方法很简单：做一个 MCP server，接入 Claude Code，在用户工作流里识别“正在评估新工具”的时刻，再提示相关 credits 或折扣。
- 第一版是基于提到工具名就触发，但作者发现这过于 spammy，因此改成只在“实际评估新工具”时触发，提升上下文相关性。
- 作者还在开发初始化扫描 `package.json` 的能力，以识别项目中已经使用、可能正在付费的工具，并提示现有可用优惠。
- 本质上，它不是生成代码，而是一个面向开发采购/采用决策的上下文感知推荐插件。

## Results
- 文本中**没有提供定量实验结果**，没有数据集、基线、准确率、点击率、转化率或用户研究数字。
- 最具体的已报告进展是：**第一版会在提到任意工具时都触发**，作者将其改为**仅在评估新工具时触发**，以减少 spam。
- 还声称计划在初始化时扫描 **`package.json`**，以便识别“已经在付费的工具”并标记可用 deals，但未给出效果数字。
- 当前更像是早期原型与产品探索，作者明确在征求反馈：用户是否会使用，还是会觉得这是 IDE 里的广告。

## Link
- [https://news.ycombinator.com/item?id=47282711](https://news.ycombinator.com/item?id=47282711)
