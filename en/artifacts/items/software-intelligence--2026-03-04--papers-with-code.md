---
source: hn
url: https://papers.app.nz
published_at: '2026-03-04T23:05:00'
authors:
- horsebatterysta
topics:
- scientific-search
- paper-code-linking
- semantic-search
- research-discovery
- benchmark-tracking
relevance_score: 0.46
run_id: materialize-outputs
language_code: en
---

# Papers with Code

## Summary
This is not the main text of a research paper, but rather a site introduction for **Papers with Code**. It presents a research discovery platform that unifies indexing of papers, code, methods, and datasets, and supports semantic search.

## Problem
- Researchers find it difficult to efficiently locate the relationships among **papers, reproducible code, methods, and datasets** across massive volumes of literature.
- Without a unified search entry point, model comparison, benchmark tracking, and experiment reproduction all become inefficient.
- This matters because both research and engineering deployment depend on quickly discovering usable methods and implementations.

## Approach
- Build an aggregation platform that centrally collects papers, code repositories, methods, and datasets.
- Provide **semantic search** capabilities; the text states that it is powered by **gobed** to improve retrieval relevance.
- Use a structured catalog to divide research objects into multiple entity types, such as papers, code repos, methods, and datasets.
- Display recent evals, suggesting that the platform also supports browsing and tracking results/evaluation information.

## Results
- The most specific result given in the text is the platform scale: **577K papers**.
- Includes **600K code repos**.
- Includes **9K methods**.
- Includes **15K datasets**.
- No paper-style experimental metrics are provided; it **does not provide** retrieval precision, recall, speed, or comparative results against relative baselines.

## Link
- [https://papers.app.nz](https://papers.app.nz)
