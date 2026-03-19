---
source: hn
url: https://surfingcomplexity.blog/2026/03/07/grow-fast-and-overload-things/
published_at: '2026-03-07T23:13:16'
authors:
- azhenley
topics:
- llm-reliability
- service-uptime
- capacity-overload
- resilience-engineering
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Grow Fast and Overload Things

## Summary
This article is not an academic paper, but an observational commentary on the reliability of LLM services. The author argues that the main reliability problems at OpenAI and Anthropic are not simply due to “developing too fast,” but rather to surging user demand overloading their systems.

## Problem
- The article discusses the question: why the online reliability/availability of mainstream LLM services is still not very high, and why this instability keeps recurring.
- This matters because LLMs have become foundational capability services; once availability is insufficient, it directly affects developers, product integrations, and user trust.
- The author specifically points out that the real challenge may not be “rapid iteration causes failures,” but rather **demand growth and innovative usage patterns exceeding expectations**, thereby triggering capacity saturation.

## Approach
- The core method is not proposing a new algorithm, but providing a **systems reliability interpretation** based on public status-page data and industry phenomena.
- The author cites the availability numbers on OpenAI’s and Anthropic’s status pages to show that current services generally have not reached the 99.9% (three nines) level.
- The author then proposes a simpler mechanistic explanation: as LLMs are adopted rapidly, users invent new use cases that platform providers did not anticipate, causing request load to spike suddenly.
- The author borrows the **florescence** concept from resilience engineering to describe this process of “a capability appearing and then being rapidly and widely absorbed,” and attributes the failures to **saturation/overload** rather than purely software defects.
- Based on this judgment, the article suggests that likely improvement directions will be resource reallocation, peak load smoothing, load shedding, and graceful degradation, rather than relying only on adding constraints to the development process.

## Results
- The most concrete evidence provided in the article is the status-page numbers: aside from Sora, OpenAI’s and Anthropic’s services **did not reach 99.9% availability**.
- The author particularly notes that **ChatGPT uptime is 98.86%**, which does **not even reach 99% (two nines)**.
- The article **does not provide quantitative research results such as experiments, datasets, baseline models, or statistical significance**; it is not an empirical machine learning paper.
- The strongest concrete conclusion is that the current instability of LLM platforms is, in the author’s view, more like “**grow fast and overload things**” — that is, a capacity overload problem triggered by user growth and innovative usage patterns.
- The article also offers a testable operational-level judgment: because GPU capacity is expensive and constrained, providers may not always be able to solve the problem through horizontal scaling, and are therefore more likely to invest in **load management and graceful degradation** capabilities.

## Link
- [https://surfingcomplexity.blog/2026/03/07/grow-fast-and-overload-things/](https://surfingcomplexity.blog/2026/03/07/grow-fast-and-overload-things/)
