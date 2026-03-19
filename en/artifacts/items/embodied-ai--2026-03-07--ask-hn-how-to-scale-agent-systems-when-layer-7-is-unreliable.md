---
source: hn
url: https://news.ycombinator.com/item?id=47292281
published_at: '2026-03-07T22:55:20'
authors:
- rjpruitt16
topics:
- agent-systems
- layer-7-reliability
- retry-storms
- workflow-orchestration
- api-failures
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Ask HN: How to scale agent systems when Layer 7 is unreliable?

## Summary
This is not a research paper, but a practical question about how to keep large-scale agent systems running reliably when **Layer 7/API is unreliable**. The core concerns are failure propagation in multi-step workflows, retry storms, and recovery after mid-execution failures.

## Problem
- The problem being addressed is: when an agent workflow depends on **10+ calls** to services such as LLMs, data APIs, and web scraping, failures at the application layer (Layer 7) can cause the entire process to fail.
- This matters because **429 rate limits, partial outages, and synchronized retries** can amplify downstream pressure and create a **retry storm**, further degrading overall system availability.
- It also focuses on workflow orchestration issues, such as whether **LangGraph** can safely recover and continue execution after failing halfway through.

## Approach
- The text does not propose a complete method; instead, it asks whether common reliability mechanisms in production are effective, such as **retry coordination**, **circuit breakers**, failure recovery, and resumption.
- The core idea can be summarized as: do not let every agent retry blindly after failure; instead, use global coordination, rate limiting, and circuit breaking to avoid “overwhelming” downstream services.
- The discussion focuses on how to handle API failures, how to avoid synchronized retries across customers, and how workflow systems can recover state after failing midway.
- The system context mentioned is an agent workflow composed of multiple services, including LLMs, external APIs, and scraping dependencies, so the problem is fundamentally one of **distributed application-layer reliability**.

## Results
- No experiments, benchmarks, or quantitative results are provided.
- The only clearly stated scale information in the text is that agent workflows **typically involve 10+ API calls**.
- The explicitly listed failure types include: **429 rate limits**, **partial outages**, and **LangGraph workflows fail mid-execution**.
- The strongest specific claim is that unreliable Layer 7 can lead to **workflow failure** or **retry storms**, and synchronized retries may further worsen the load on downstream dependencies.

## Link
- [https://news.ycombinator.com/item?id=47292281](https://news.ycombinator.com/item?id=47292281)
