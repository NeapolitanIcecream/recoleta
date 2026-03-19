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
language_code: en
---

# No, it doesn't cost Anthropic $5k per Claude Code user

## Summary
This article refutes the claim that “Anthropic bears $5,000 in inference cost for each Claude Code Max user,” arguing that the figure confuses retail API pricing with true inference cost. The author contends that the real cost is more likely around 10% of the listed API price, so Anthropic is probably not losing heavily on inference for the average user.

## Problem
- The problem being addressed is that media and social platforms are mistaking **retail API prices** for **the model’s actual inference cost**, thereby exaggerating the extent of Anthropic’s losses on Claude Code subscriptions.
- This matters because it can mislead the public’s understanding of the business models of frontier AI companies, inference economics, and API pricing power.
- The article also distinguishes between two types of actors: Anthropic’s own service costs, and the costs faced by third parties such as Cursor that must purchase model API access at retail or near-retail prices.

## Approach
- The author uses a simple comparison framework: **Anthropic’s Opus 4.6 API list prices** vs **the market prices of similarly sized open-source/open-weight MoE models on OpenRouter**, treating the latter as a rough proxy for true inference cost.
- Comparable models selected include **Qwen 3.5 397B-A17B** and **Kimi K2.5 1T/32B active**, which the author argues are close to Opus 4.6’s likely serviceable architecture range in scale.
- The core logic is simple: if multiple providers can offer similarly sized models at about **10%** of Anthropic’s API prices and still remain profitable, then Anthropic’s true per-unit inference cost is unlikely to be close to its retail API prices.
- The author then applies this roughly **10% cost ratio** to the monthly token consumption of heavy and average Claude Code users to estimate the gap between Anthropic’s actual serving costs and subscription revenue.

## Results
- Anthropic’s Opus 4.6 API list prices are **$5 per million input tokens** and **$25 per million output tokens**; using those retail prices, a heavy Claude Code Max user could indeed consume about **$5,000/month in API-equivalent usage**.
- But comparable model pricing on OpenRouter is much lower: **Qwen 3.5 397B** is about **$0.39/million input** and **$2.34/million output**; **Kimi K2.5** is about **$0.45/million input** and **$2.25/million output**, roughly **1/10** of Anthropic’s API pricing.
- Cached tokens show a similar gap: the article cites **DeepInfra charging $0.07/MTok for cache reads on Kimi K2.5**, versus **$0.50/MTok** from Anthropic.
- Based on an approximate **10%** true cost ratio, if a heavy user generates **$5,000/month in API-equivalent usage**, the author estimates Anthropic’s real inference cost at about **$500/month**, implying a loss of roughly **$300/month** on a **$200/month** plan, not **$4,800/month**.
- Citing Anthropic data, the author says **fewer than 5%** of subscribers hit weekly limits; the average Claude Code developer uses about **$6/day in API-equivalent consumption**, and **90% are below $12/day**, or about **$180/month** on average. If the true cost is **10%** of that, then serving cost is about **$18/month**, which is near break-even or profitable against subscription prices of **$20–$200/month**.
- For third parties like Cursor, the article argues that **$5,000/heavy user/month** may actually be the right order of magnitude, because they need to buy model capacity at Anthropic’s retail or near-retail API prices.

## Link
- [https://martinalderson.com/posts/no-it-doesnt-cost-anthropic-5k-per-claude-code-user/](https://martinalderson.com/posts/no-it-doesnt-cost-anthropic-5k-per-claude-code-user/)
