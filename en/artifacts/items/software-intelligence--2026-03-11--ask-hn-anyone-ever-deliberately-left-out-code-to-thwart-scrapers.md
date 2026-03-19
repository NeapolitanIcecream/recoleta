---
source: hn
url: https://news.ycombinator.com/item?id=47343587
published_at: '2026-03-11T23:00:08'
authors:
- truelinux1
topics:
- code-scraping
- open-source
- anti-scraping
- human-ai-interaction
relevance_score: 0.43
run_id: materialize-outputs
language_code: en
---

# Ask HN: Anyone ever deliberately left out code to thwart scrapers?

## Summary
This is a discussion about whether developers should deliberately leave gaps in public code to hinder scraping bots, rather than a formal research paper. It raises a practical question related to open-source sharing, data scraping, and the disappearance of human-to-human interaction.

## Problem
- The issue under discussion is whether developers should intentionally omit parts of code, dependencies, or key implementations to reduce the risk of automated scraping and unattributed reuse.
- Its importance lies in the fact that code on platforms like GitHub is being continuously scraped at scale for model training or redistribution, while original authors may receive neither interaction, attribution, nor feedback.
- The core tension is whether this practice can effectively express a stance or protect the value of one’s labor, or whether it merely harms reproducibility and normal collaboration without accomplishing anything.

## Approach
- The text does not propose a formal method, but instead gives several simple mechanisms for “deliberately leaving gaps”: declaring but not defining a function, omitting a dependency, or writing in the README, “email me for the missing piece.”
- The simplest interpretation of these practices is that human readers still have a chance to obtain the full content through communication, while automated scraping and direct reuse become more difficult.
- Its implicit mechanism is not technical protection, but rather raising the barrier of manual interaction to force users to shift from “direct scraping” to “contact the author.”
- The text also questions the effectiveness of this mechanism, suggesting that it may be merely a symbolic gesture rather than a truly workable anti-scraping strategy.

## Results
- It provides no quantitative experimental results, datasets, baselines, or metric comparisons.
- It reports no concrete figures on how this “deliberately missing code” strategy affects scraping prevention rates, manual contact rates, project adoption rates, or community feedback.
- The strongest concrete claim is that bots on code-hosting platforms scrape code “24/7,” and that compared with the past, the current environment has “less human-to-human interaction.”
- The text does not demonstrate that the strategy works; it only offers actionable examples and asks the community to judge whether it is “coherent” or “pointless.”

## Link
- [https://news.ycombinator.com/item?id=47343587](https://news.ycombinator.com/item?id=47343587)
