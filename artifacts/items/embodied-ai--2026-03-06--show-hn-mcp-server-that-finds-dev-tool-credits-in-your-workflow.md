---
source: hn
url: https://news.ycombinator.com/item?id=47282711
published_at: '2026-03-06T23:54:47'
authors:
- janaksunil
topics:
- mcp-server
- developer-tools
- workflow-assistant
- tool-discovery
- discount-recommendation
relevance_score: 0.01
run_id: materialize-outputs
---

# Show HN: MCP server that finds dev tool credits in your workflow

## Summary
这是一个接入 Claude Code 的 MCP server，用来在开发者评估新工具或初始化项目时，提示其工作流中可用的 credits、折扣或优惠。它更像是一个开发工具购买辅助插件，而不是一篇研究论文或机器人/基础模型方向的技术工作。

## Problem
- 开发者在选型或使用工具时，常常不知道已有的 credits、折扣或促销，可能导致重复付费或错过优惠。
- 如果提示机制过于频繁，会变成 IDE 内广告，打断工作流并降低可用性。
- 作者想解决“在合适时机提供省钱信息”这个产品体验问题，这对降低工具采购成本有现实意义。

## Approach
- 构建一个 **MCP server**，可插入 **Claude Code** 工作流中。
- 初版会在用户提到任意工具时触发，但因为过于“spammy”，后续改为仅在用户**实际评估新工具**时才触发。
- 计划在初始化时扫描 **package.json**，识别项目已在使用/付费的工具，并提示可能适用的 deals。
- 核心机制可以简单理解为：**监听开发工作流中的工具上下文 → 判断是否处于选型/已付费场景 → 返回对应优惠信息**。

## Results
- 文本中**没有提供任何定量实验结果**，没有数据集、指标、基线或对比数字。
- 最强的具体声明是：触发策略已从“提到任何工具都触发”改进为“仅在评估新工具时触发”，以减少骚扰式提示。
- 另一个具体计划是：在 init 阶段扫描 `package.json`，从而识别“你已经在付费的工具”并标记可用优惠。
- 当前内容更像是产品展示与用户调研（“你会用吗，还是像 IDE 里的广告？”），而非经过验证的研究突破。

## Link
- [https://news.ycombinator.com/item?id=47282711](https://news.ycombinator.com/item?id=47282711)
