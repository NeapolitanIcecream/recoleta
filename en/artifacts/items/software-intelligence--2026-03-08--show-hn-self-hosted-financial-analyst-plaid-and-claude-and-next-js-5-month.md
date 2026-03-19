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
language_code: en
---

# Show HN: Self-hosted financial analyst – Plaid and Claude and Next.js, –$5/month

## Summary
This is a self-hosted personal finance analysis system that integrates Plaid brokerage connections, market data enrichment, Claude investment analysis, and a Next.js visualization dashboard into a single repository. It emphasizes low operations overhead and low monthly cost, allowing individual users to automatically consolidate holdings across multiple accounts and receive AI-assisted insights.

## Problem
- Individual investors’ assets are often spread across multiple brokerages and account types, making it difficult to view holdings, net worth, allocation, and risk signals in one place.
- Traditional investment tracking tools often lack a complete pipeline that is self-hostable, extensible, and capable of combining real-time market technical indicators with natural-language analysis.
- Building it yourself usually requires separately handling account integration, data cleaning, indicator calculation, database synchronization, frontend presentation, and scheduled jobs, resulting in high integration costs.

## Approach
- Use **Plaid** to connect supported brokerages such as Robinhood and Fidelity, and uniformly fetch holdings from taxable, retirement, and cash accounts.
- Use the Python `agent/` pipeline to enrich each position with data via `yfinance`, extracting **RSI, MACD, Bollinger Bands, fundamentals, and news**.
- Send the full portfolio to **Claude** to generate structured analysis results, such as a health score, per-stock buy/sell/hold recommendations, and action items.
- Sync pipeline outputs to **Supabase/Postgres**, then use the **Next.js** dashboard to display net worth, asset allocation, RSUs, price refreshes, wealth projections, and AI recommendations.
- Through a single repository, a one-click installer, and scheduled execution via `launchd`/`cron`, enable self-hosted automated operation and emphasize low-friction deployment so that “the whole system runs locally.”

## Results
- Supports connecting **6 explicitly listed brokerages/platforms**: Robinhood, SoFi, Stash, Acorns, Wealthfront, and Fidelity, and claims extensibility to any **Plaid-supported brokerage**.
- The Plaid Development plan is described as **free** and supports up to **100 real account connections**.
- The author provides cost data: based on **15 real pipeline runs** and actual token usage, priced using `claude-sonnet-4-6`, the system’s total cost is about **$5/month**; pricing is listed as **$3.00/1M input tokens** and **$15.00/1M output tokens**.
- Scheduled jobs can automatically run at **Mon/Wed/Fri 7am**, supporting macOS `launchd` or Linux `cron`, emphasizing sustainable automatic refreshes and continued operation after restarts.
- No standard academic benchmarks, A/B comparisons, or quantified investment performance results such as accuracy or returns are provided; the strongest concrete claims are **low deployment complexity, low API cost, real brokerage integration, and end-to-end automated analysis**.

## Link
- [https://github.com/mkash25/Claude-powered-AI-native-financial-dashboard](https://github.com/mkash25/Claude-powered-AI-native-financial-dashboard)
