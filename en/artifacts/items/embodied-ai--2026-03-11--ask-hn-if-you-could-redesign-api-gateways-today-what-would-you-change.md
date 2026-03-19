---
source: hn
url: https://news.ycombinator.com/item?id=47343821
published_at: '2026-03-11T23:18:27'
authors:
- shubham7004
topics:
- api-gateway
- modular-architecture
- saas
- infra-discussion
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Ask HN: If you could redesign API gateways today, what would you change?

## Summary
This is an open discussion post on Hacker News, not a research paper. It raises a question about redesigning API gateways: in modern modular SaaS architectures, should traditional monolithic API gateways be replaced by more modular infrastructure?

## Problem
- The core issue under discussion is that traditional API gateways are often fairly monolithic, while modern SaaS systems increasingly emphasize composable, modular architectures.
- The post points out that many teams actually only need a small number of core capabilities, such as authentication, rate limiting, logging, and usage tracking, so a full traditional gateway may be overly heavy.
- This matters because the shape of API infrastructure directly affects system complexity, maintainability, and how teams build systems.

## Approach
- This content **does not propose a formal paper methodology**; instead, it solicits community opinions in the form of a question: if designing API infrastructure from scratch today, would people still adopt a traditional API gateway.
- The implicit mechanism envisioned in the text is to split capabilities such as authentication, rate limiting, logging, and usage tracking into more independent, composable modules rather than relying on a single gateway product.
- It is essentially comparing two design philosophies: **traditional monolithic gateway** vs **modular API infrastructure**.

## Results
- **No quantitative experimental results** are provided, nor datasets, baselines, or performance metrics, because this is not a research paper but a community discussion post.
- The strongest specific claim is that modern SaaS architectures are "increasingly composable and modular," while API gateways "still feel fairly monolithic."
- The typical required capabilities listed in the text include **4** items: authentication, rate limiting, logging, usage tracking.
- The post metadata shows it had only **2 points** at the time and was posted **3 days ago**, but these do not constitute research results.

## Link
- [https://news.ycombinator.com/item?id=47343821](https://news.ycombinator.com/item?id=47343821)
