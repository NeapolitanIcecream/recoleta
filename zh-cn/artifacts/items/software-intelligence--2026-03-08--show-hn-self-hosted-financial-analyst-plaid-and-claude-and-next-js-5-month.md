---
source: hn
url: https://github.com/mkash25/Claude-powered-AI-native-financial-dashboard
published_at: '2026-03-08T23:54:01'
authors:
- prophet94
topics:
- personal-finance
- self-hosted-ai
- investment-analytics
- nextjs-dashboard
- llm-agent
relevance_score: 0.39
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Self-hosted financial analyst – Plaid and Claude and Next.js, –$5/month

## Summary
这是一个自托管的个人金融分析系统，把 Plaid 券商连接、市场数据增强、Claude 投资分析和 Next.js 可视化面板整合到单一仓库中。它强调低运维与低月成本，让个人用户自动汇总多账户持仓并获得 AI 辅助洞察。

## Problem
- 个人投资者的资产通常分散在多个券商与账户类型中，难以统一查看持仓、净值、配置和风险信号。
- 传统投资跟踪工具往往缺少可自托管、可扩展、能结合实时市场技术指标与自然语言分析的完整流水线。
- 如果要自己搭建，通常需要分别处理账户接入、数据清洗、指标计算、数据库同步、前端展示和定时任务，集成成本高。

## Approach
- 用 **Plaid** 连接 Robinhood、Fidelity 等支持的券商，统一抓取 taxable、retirement 和 cash 账户持仓。
- 用 Python `agent/` 流水线对每个仓位做数据增强：接入 `yfinance` 提取 **RSI、MACD、布林带、基本面和新闻**。
- 将完整投资组合发送给 **Claude**，生成结构化分析结果，如健康评分、逐股票 buy/sell/hold 建议和行动项。
- 把流水线输出同步到 **Supabase/Postgres**，再由 **Next.js** 仪表盘展示净值、资产配置、RSU、价格刷新、财富预测与 AI 建议。
- 通过单仓库、一键安装器和 `launchd`/`cron` 定时调度，实现自托管自动运行，强调“整套系统本地跑起来”的低门槛部署。

## Results
- 支持连接 **6 个明确列出的券商/平台**：Robinhood、SoFi、Stash、Acorns、Wealthfront、Fidelity，并声称可扩展到任意 **Plaid-supported brokerage**。
- Plaid Development 方案被描述为 **免费**，并支持最多 **100 个真实账户连接**。
- 作者给出成本数据：基于 **15 次真实流水线运行** 的实际 token 使用，按 `claude-sonnet-4-6` 定价，系统总成本约 **$5/月**；定价列为 **$3.00/1M 输入 token**、**$15.00/1M 输出 token**。
- 定时任务可自动在 **Mon/Wed/Fri 7am** 运行，支持 macOS `launchd` 或 Linux `cron`，强调可持续自动刷新且重启后继续运行。
- 未提供标准学术基准、A/B 对比或准确率/收益率等量化投资表现结果；最强的具体主张是 **低部署复杂度、低 API 成本、真实券商接入与端到端自动化分析**。

## Link
- [https://github.com/mkash25/Claude-powered-AI-native-financial-dashboard](https://github.com/mkash25/Claude-powered-AI-native-financial-dashboard)
