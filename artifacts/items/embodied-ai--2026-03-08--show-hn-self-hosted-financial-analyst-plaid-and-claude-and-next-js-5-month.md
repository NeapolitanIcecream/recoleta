---
source: hn
url: https://github.com/mkash25/Claude-powered-AI-native-financial-dashboard
published_at: '2026-03-08T23:54:01'
authors:
- prophet94
topics:
- personal-finance
- portfolio-analytics
- llm-agent
- plaid-integration
- self-hosted
- nextjs-dashboard
relevance_score: 0.02
run_id: materialize-outputs
---

# Show HN: Self-hosted financial analyst – Plaid and Claude and Next.js, –$5/month

## Summary
这是一个自托管的个人投研/财务看板系统，把 Plaid 券商连接、持仓数据增强、Claude 分析和 Next.js 可视化整合到一个可本地运行的单仓库方案中。它主打低运维和低成本，声称整套 AI 分析月成本约 **5 美元**。

## Problem
- 个人投资者的资产通常分散在多个券商和账户中，难以统一查看持仓、配置、现金与退休账户情况。
- 原始券商数据缺少技术指标、新闻和结构化投研解释，用户很难快速得到可执行的组合级判断。
- 现有方案常依赖云端 SaaS，成本、隐私和部署控制权不足；作者希望提供可自托管、低月费的替代方案。

## Approach
- 用 **Plaid** 连接多个真实券商账户，统一抓取 taxable、retirement 和 cash 等账户持仓数据。
- Python 管线对每个标的做数据增强：接入 **yfinance** 等来源补充 **RSI、MACD、Bollinger Bands、fundamentals、news**。
- 将完整投资组合发送给 **Claude**，生成结构化输出，如健康评分、逐股票 buy/sell/hold 建议和行动项。
- 把结果同步到 **Supabase(Postgres)**，再由 **Next.js** 仪表盘展示净值、资产配置、RSU、财富预测和 AI 建议。
- 通过 **launchd/cron** 定时在 Mon/Wed/Fri 7am 自动运行，形成本地自托管的周期性分析流程。

## Results
- 定量结果很有限；文中**没有**提供标准学术基准、A/B 测试、收益率、预测准确率或用户研究结果。
- 最明确的数字主张是成本：基于 **15 次真实 pipeline 运行** 的 token 使用统计，使用 **claude-sonnet-4-6** 时总成本约 **$5/月**。
- 给出的模型单价为 **$3.00 / 1M input tokens**、**$15.00 / 1M output tokens**，并说明成本会随投资组合中 ticker 数量增加而上升。
- Plaid Development 被描述为**免费**，并支持最多 **100 个真实账户连接**。
- 部署/运行层面的具体主张包括：自动调度为 **每周 3 次**（Mon/Wed/Fri 7am），Plaid Development 审批通常 **1–3 个工作日**。
- 安全与工程层面的具体实现声明包括：访问令牌“**encrypted at rest**”，采用 **PBKDF2 + Fernet**，并且将敏感密钥限制在服务端使用。

## Link
- [https://github.com/mkash25/Claude-powered-AI-native-financial-dashboard](https://github.com/mkash25/Claude-powered-AI-native-financial-dashboard)
