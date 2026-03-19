---
source: hn
url: https://news.ycombinator.com/item?id=47358750
published_at: '2026-03-12T23:32:35'
authors:
- nishiohiroshi
topics:
- developer-tools
- code-review
- localization
- ai-assistant
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Add per-repo output language preference

## Summary
This is not a research paper, but a product update announcement: GitAuto has added a per-repo output language preference feature, allowing AI-generated code review comments to be displayed in a team's native language. Its main value is improving the usability of reading and reviewing AI-generated PR comments for non-English-speaking development teams, rather than introducing a new algorithmic method.

## Problem
- When non-English-speaking development teams review AI-generated PR comments and code annotations, if the content defaults to English, it increases comprehension costs and collaboration friction.
- Multi-repository teams may need different language strategies; lacking repository-level language configuration reduces workflow flexibility.
- This problem matters because code review is a high-frequency collaboration activity, and language barriers directly affect review efficiency and communication quality.

## Approach
- Provide a **per-repo** output language preference setting, configurable individually in repository Rules Settings.
- GitAuto translates or outputs its generated code comments and GitHub comments in the target native language, supporting **70+ languages**.
- At the same time, it keeps **PR titles and bodies in English**, indicating that the mechanism localizes only certain output channels rather than fully switching the language of all PR metadata.
- The text does not describe the underlying model, translation pipeline, quality control, or any novel research-oriented technical mechanism.

## Results
- The only explicit quantitative information provided is: support for **70+ languages**.
- The post provides no experiments, benchmarks, datasets, A/B tests, or efficiency metrics, so there are **no verifiable quantitative research results**.
- The strongest concrete product claim is: non-English-speaking teams can now read GitAuto's code comments and GitHub comments in their native language.
- Another specific limiting claim is: **PR titles and bodies stay in English**, showing that the current feature scope is limited and only partially localized.

## Link
- [https://news.ycombinator.com/item?id=47358750](https://news.ycombinator.com/item?id=47358750)
