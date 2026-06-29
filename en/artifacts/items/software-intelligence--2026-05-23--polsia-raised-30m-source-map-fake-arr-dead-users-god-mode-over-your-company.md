---
source: hn
url: https://zero-arr.vercel.app
published_at: '2026-05-23T22:25:34'
authors:
- not-chatgpt
topics:
- ai-company-builder
- autonomous-agents
- arr-due-diligence
- source-map-exposure
- human-in-the-loop
- privacy-leak
relevance_score: 0.66
run_id: materialize-outputs
language_code: en
---

# Polsia raised $30M; source map: fake ARR, dead users, god-mode over your company

## Summary
The article claims Polsia’s $10M ARR and “fully autonomous” AI company-builder pitch do not match its own public API and shipped source map. It frames the case as technical due diligence on revenue quality, churn, human operations, security, and privacy.

## Problem
- It targets a claimed autonomous AI company-builder that raised $30M while reporting about $10M ARR and 120,000+ companies.
- The issue matters because investors, users, and customer companies may rely on recurring-revenue, automation, and control claims that the article says are contradicted by public data.
- It also reports exposed operational telemetry and owner PII for showcased companies, which creates privacy and trust risk.

## Approach
- The authors query Polsia’s public live dashboard API and compare the marketed ARR number with subscription MRR, churn, cost, company counts, and revenue buckets.
- They reconstruct the public production source map and identify 1,355 source modules, including admin and team-economics UI.
- They inspect source and API fields for human QA labels, admin users, impersonation, SQL access, credits, and kill or override controls.
- They probe generated company pages for checkout or payment paths and query public dashboard endpoints for showcased fund companies.
- They compare their findings with dated third-party snapshots and hands-on user reports.

## Results
- ARR: Polsia’s public dashboard shows a headline $9.70M annualized number, while the article says only about $4.63M is subscription revenue; the rest includes one-off packs ($1.97M), ad-spend pass-through ($1.93M), 1-hour boosts ($0.80M), and user-company payments ($0.36M).
- Churn: paid churn is reported at about 48% per month, implying about 0.04% of the base survives 12 months; the article estimates durable annual recurring revenue rounds to about $0 under that churn.
- Unit economics: daily AI cost is listed as $7,344 against about $12,887 per day of subscription run-rate, so compute consumes about 57% of subscription dollars before human ops and infrastructure.
- Usage: the API reports 118,683 total companies and 7,437 active companies, an active rate of about 6.3%; the article also says all 16 showcased fund companies report $0.00 revenue.
- Autonomy and control: the public source map contains 1,355 modules, with 464 reconstructable into a running app, and the article identifies human QA labeling, operator logins, admin impersonation, production SQL access, and company halt or override controls.
- Privacy/security: for 16 fund companies, an unauthenticated endpoint allegedly returned owner name, Twitter handle, balances, 18-agent rosters, per-agent costs, execution timestamps, and a payload field showing public_dashboard_enabled as false.

## Link
- [https://zero-arr.vercel.app](https://zero-arr.vercel.app)
