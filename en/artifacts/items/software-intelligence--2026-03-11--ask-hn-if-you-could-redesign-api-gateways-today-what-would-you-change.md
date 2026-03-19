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
- developer-infrastructure
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# Ask HN: If you could redesign API gateways today, what would you change?

## Summary
This is not a research paper, but an open discussion post on Hacker News asking whether the traditional monolithic API gateway should be redesigned into more modular API infrastructure. The core question is whether common capabilities such as authentication, rate limiting, logging, and usage tracking should be decoupled and composed.

## Problem
- The issue under discussion is that modern SaaS architectures are becoming increasingly composable and modular, while API gateways are still often implemented as monolithic systems, raising the question of whether they still fit current needs.
- Its importance lies in the fact that API gateways often carry foundational capabilities such as authentication, rate limiting, logging, and metering, so the design approach affects system flexibility, maintainability, and the cost of evolution.
- The implied pain point in the post is that many teams actually need only a small number of core capabilities, and may not need a complete, traditional “gateway” product.

## Approach
- The text does not propose a formal research method, but instead solicits community opinions through an open question: if designing API infrastructure from scratch today, would people still adopt a traditional gateway.
- The proposed core mechanism is very simple: split capabilities such as authentication, rate limiting, logging, and usage tracking into modules, rather than placing them inside a monolithic gateway.
- The discussion framework compares two approaches: **traditional centralized API gateway** vs **modular infrastructure composed on demand**.
- This content is better understood as problem framing and an architectural hypothesis, rather than a solution validated through experiments.

## Results
- It provides no quantitative results, experiments, datasets, baselines, or performance comparisons.
- The strongest concrete claim is that modern SaaS architectures are “increasingly composable and modular,” while API gateways “still feel fairly monolithic.”
- The text lists only 4 categories of core functions: authentication, rate limiting, logging, usage tracking.
- The post raises 1 key design question: when starting from scratch, should teams retain the traditional API gateway, or move toward a more modular approach.

## Link
- [https://news.ycombinator.com/item?id=47343821](https://news.ycombinator.com/item?id=47343821)
