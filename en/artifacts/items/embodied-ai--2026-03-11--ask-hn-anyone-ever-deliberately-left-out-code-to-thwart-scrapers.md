---
source: hn
url: https://news.ycombinator.com/item?id=47343587
published_at: '2026-03-11T23:00:08'
authors:
- truelinux1
topics:
- open-source
- web-scraping
- anti-scraping
- developer-community
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Ask HN: Anyone ever deliberately left out code to thwart scrapers?

## Summary
This is not a research paper, but a Hacker News discussion post raising the question of whether one should deliberately leave gaps in public code to interfere with scraping bots. Its core value lies in reflecting open-source authors' concerns about automated scraping, lack of attribution, and the disappearance of community interaction.

## Problem
- The issue under discussion is whether developers should intentionally omit parts of code, dependencies, or key implementations to prevent automated scraping systems from directly copying the results of their work.
- Its importance, according to the post, is that “bots scrape GitHub 24/7,” and such scraping often lacks acknowledgment, interaction, or the human exchange that used to exist in communities.
- At its core, this is a sociotechnical question about open-source publication strategy, anti-scraping posture, and community norms, rather than a question of algorithmic performance.

## Approach
- The text does not propose a formal research method, but instead gives several possible tactics: calling an undefined function, leaving out a dependency, or noting in the readme, “email me for the missing piece.”
- The shared mechanism of these tactics is simple: deliberately make the repository unable to run completely out of the box, thereby increasing the cost of automated scraping and interaction-free reuse.
- The post further asks whether this is a “coherent stance” or a “pointless gesture,” so it is better understood as an open-ended ethical/strategic discussion rather than a validated method.

## Results
- The text **does not provide any quantitative experimental results**; there are no datasets, metrics, baselines, or comparison methods.
- The only somewhat specific empirical claim is: "bots scrape GitHub 24/7"—that is, the author believes there is continuous high-frequency automated scraping on code hosting platforms, but provides no measured figures or source of evidence.
- It does not report whether deliberately leaving gaps actually reduces scraping, increases attribution, improves interaction, or how much negative impact it has on normal users.
- Therefore, the strongest conclusion that can be drawn from this content is only that some people are considering “incompletely public code” as an anti-scraping posture, but neither its effectiveness nor its reasonableness has been empirically demonstrated.

## Link
- [https://news.ycombinator.com/item?id=47343587](https://news.ycombinator.com/item?id=47343587)
