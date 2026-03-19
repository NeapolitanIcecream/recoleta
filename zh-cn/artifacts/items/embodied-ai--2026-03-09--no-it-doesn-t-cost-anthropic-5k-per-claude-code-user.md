---
source: hn
url: https://martinalderson.com/posts/no-it-doesnt-cost-anthropic-5k-per-claude-code-user/
published_at: '2026-03-09T23:22:06'
authors:
- jnord
topics:
- ai-inference-economics
- api-pricing
- llm-serving-costs
- market-analysis
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# No, it doesn't cost Anthropic $5k per Claude Code user

## Summary
这篇文章反驳“Anthropic 为每个 Claude Code Max 用户承担 5000 美元推理成本”的说法，认为该数字混淆了零售 API 定价与真实推理成本。作者主张，真实成本更可能接近 API 标价的约 10%，因此 Anthropic 在平均用户上大概率并非因推理而严重亏损。

## Problem
- 要解决的问题是：媒体与社交平台把 **API 零售价**误当成 **模型实际推理成本**，从而夸大 Anthropic 在 Claude Code 订阅上的亏损程度。
- 这很重要，因为它会误导公众对前沿 AI 公司商业模式、推理经济学和 API 定价权的理解。
- 文章还区分了两类主体：Anthropic 自己的服务成本，与像 Cursor 这类需要按零售或接近零售价格采购模型 API 的第三方成本。

## Approach
- 作者用一个简单框架比较：**Anthropic 的 Opus 4.6 API 标价** vs **OpenRouter 上相近规模开源/开放权重 MoE 模型的市场价格**，把后者当作真实推理成本的近似代理。
- 选取可比模型包括 **Qwen 3.5 397B-A17B** 和 **Kimi K2.5 1T/32B active**，认为它们在架构规模上接近 Opus 4.6 的可服务区间。
- 核心机制很简单：如果多家提供商能以约 Anthropic API 价格的 **10%** 提供类似规模模型并仍可盈利，那么 Anthropic 的真实单位推理成本不太可能接近其零售 API 标价。
- 然后作者把这个约 **10% 成本率** 代入 Claude Code 重度用户和平均用户的月度 token 消耗，估算 Anthropic 的实际服务成本与订阅收入之间的差距。

## Results
- Anthropic 的 Opus 4.6 API 标价为 **$5/百万输入 token**、**$25/百万输出 token**；按这个零售价计算，重度 Claude Code Max 用户每月确实可能消耗约 **$5,000 API 等价用量**。
- 但 OpenRouter 上可比模型价格显著更低：**Qwen 3.5 397B** 约 **$0.39/百万输入**、**$2.34/百万输出**；**Kimi K2.5** 约 **$0.45/百万输入**、**$2.25/百万输出**，大约是 Anthropic API 价格的 **1/10**。
- 缓存 token 也有类似差距：文中举例 **DeepInfra 对 Kimi K2.5 的 cache read 为 $0.07/MTok**，而 Anthropic 为 **$0.50/MTok**。
- 基于约 **10%** 的真实成本率，若某重度用户产生 **$5,000/月 API 等价用量**，作者估算 Anthropic 的真实推理成本约为 **$500/月**，对应在 **$200/月** 套餐上约亏 **$300/月**，而不是亏 **$4,800/月**。
- 作者引用 Anthropic 数据称：**少于 5%** 的订阅者会触及周上限；平均 Claude Code 开发者约 **$6/天 API 等价消耗**，**90% 低于 $12/天**，即平均约 **$180/月**。若真实成本为其 **10%**，则服务成本约 **$18/月**，对 **$20–$200/月** 订阅价格而言接近盈亏平衡或有利润。
- 对第三方如 Cursor，文章认为 **$5,000/重度用户/月** 这个量级反而可能是对的，因为它们需要按 Anthropic 的零售或接近零售 API 价格采购模型能力。

## Link
- [https://martinalderson.com/posts/no-it-doesnt-cost-anthropic-5k-per-claude-code-user/](https://martinalderson.com/posts/no-it-doesnt-cost-anthropic-5k-per-claude-code-user/)
