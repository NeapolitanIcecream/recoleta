---
source: hn
url: https://surfingcomplexity.blog/2026/03/07/grow-fast-and-overload-things/
published_at: '2026-03-07T23:13:16'
authors:
- azhenley
topics:
- llm-reliability
- service-availability
- resilience-engineering
- capacity-planning
- ai-infrastructure
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Grow Fast and Overload Things

## Summary
This article argues that the poor reliability of today’s mainstream AI services is mainly not because they are “developing too fast,” but because user adoption of LLMs is happening too quickly and new use cases keep emerging, causing systems to overload frequently. The author summarizes this phenomenon as “grow fast and overload things,” and explains its causes and directions for improvement from a resilience engineering perspective.

## Problem
- The article discusses the question of why online services from LLM providers such as OpenAI and Anthropic have low reliability, and why this instability matters.
- This matters because LLMs are becoming a broadly relied-upon foundational capability, but insufficient service availability directly affects user workflows, product integrations, and industry trust.
- The author rejects the simple explanation that “high development speed leads to low reliability,” arguing that the more central problem is unpredictable load and system saturation caused by demand growth and innovation in usage patterns.

## Approach
- The core mechanism is simple: once a new capability appears, users rapidly and at scale try new ways of using it, creating what the author, borrowing resilience engineering terminology, calls **florescence**.
- This expansion causes service load to surge in ways that providers find difficult to predict in advance, which then triggers **saturation** (overload), leading to service outages or performance degradation.
- The author uses availability data from the public status pages of OpenAI and Anthropic as a direct signal of the phenomenon of “poor reliability.”
- The improvement direction proposed in the article is not simply to keep expanding capacity, but to improve overload recovery capabilities, such as resource reallocation, load shedding, and graceful degradation.

## Results
- The direct evidence given in the article is status-page availability data: aside from Sora, no service at either company **reaches 99.9% uptime** (three nines).
- **ChatGPT uptime is 98.86%**, which the author points out does **not even reach 99%**.
- The article does not provide controlled experiments, benchmark tests, or paper-style quantitative comparison results, so there are **no rigorous empirical performance improvement numbers**.
- The strongest concrete claim is that the current reliability problem is better described as “**grow fast and overload things**” rather than “move fast and break things”; as experience accumulates, providers may gradually improve in overload recovery, resource scheduling, and graceful degradation.

## Link
- [https://surfingcomplexity.blog/2026/03/07/grow-fast-and-overload-things/](https://surfingcomplexity.blog/2026/03/07/grow-fast-and-overload-things/)
