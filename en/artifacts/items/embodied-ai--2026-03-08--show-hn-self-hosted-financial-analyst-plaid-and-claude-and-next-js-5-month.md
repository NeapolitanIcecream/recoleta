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
language_code: en
---

# Show HN: Self-hosted financial analyst – Plaid and Claude and Next.js, –$5/month

## Summary
This is a self-hosted personal investment research/finance dashboard system that integrates Plaid brokerage connections, holdings data enrichment, Claude analysis, and Next.js visualization into a single-repo solution that can run locally. It emphasizes low operations overhead and low cost, claiming the full AI analysis costs about **$5 per month**.

## Problem
- Individual investors' assets are often spread across multiple brokerages and accounts, making it difficult to view holdings, allocation, cash, and retirement accounts in one place.
- Raw brokerage data lacks technical indicators, news, and structured investment-research explanations, so users have difficulty quickly getting actionable portfolio-level judgments.
- Existing solutions often rely on cloud SaaS, offering insufficient cost efficiency, privacy, and deployment control; the author wants to provide a self-hosted, low-monthly-cost alternative.

## Approach
- Use **Plaid** to connect multiple real brokerage accounts and uniformly fetch holdings data across taxable, retirement, and cash accounts.
- A Python pipeline enriches each asset with additional data, using sources such as **yfinance** to add **RSI, MACD, Bollinger Bands, fundamentals, and news**.
- Send the complete portfolio to **Claude** to generate structured output such as a health score, per-stock buy/sell/hold recommendations, and action items.
- Sync the results to **Supabase(Postgres)**, then display net worth, asset allocation, RSUs, wealth projections, and AI recommendations in a **Next.js** dashboard.
- Run automatically on **Mon/Wed/Fri 7am** via **launchd/cron**, forming a periodic locally self-hosted analysis workflow.

## Results
- Quantitative results are very limited; the text does **not** provide standard academic benchmarks, A/B tests, returns, prediction accuracy, or user study results.
- The clearest numerical claim is cost: based on token usage statistics from **15 real pipeline runs**, total cost is about **$5/month** when using **claude-sonnet-4-6**.
- The stated model pricing is **$3.00 / 1M input tokens** and **$15.00 / 1M output tokens**, and it notes that cost increases with the number of tickers in the portfolio.
- Plaid Development is described as **free**, supporting up to **100 real account connections**.
- Specific deployment/operations claims include: automatic scheduling **3 times per week** (**Mon/Wed/Fri 7am**), and Plaid Development approval typically takes **1–3 business days**.
- Specific security and engineering implementation claims include: access tokens are “**encrypted at rest**,” using **PBKDF2 + Fernet**, and sensitive keys are restricted to server-side use.

## Link
- [https://github.com/mkash25/Claude-powered-AI-native-financial-dashboard](https://github.com/mkash25/Claude-powered-AI-native-financial-dashboard)
