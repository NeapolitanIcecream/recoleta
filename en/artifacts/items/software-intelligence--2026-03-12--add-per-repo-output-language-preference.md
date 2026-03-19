---
source: hn
url: https://news.ycombinator.com/item?id=47358750
published_at: '2026-03-12T23:32:35'
authors:
- nishiohiroshi
topics:
- code-review
- developer-tools
- localization
- human-ai-interaction
- repo-configuration
relevance_score: 0.67
run_id: materialize-outputs
language_code: en
---

# Add per-repo output language preference

## Summary
This content introduces GitAuto's newly added per-repo output language preference feature, allowing non-English-speaking development teams to read AI-generated code review comments and GitHub comments in their native language. It primarily improves the human-AI collaboration experience for cross-language teams, rather than proposing a new model or algorithm.

## Problem
- When non-English-speaking development teams review AI-generated PRs, if comments default to English, it increases comprehension costs and reduces collaboration efficiency.
- Multi-repo teams may need different language configurations; lacking language preferences at the repository level reduces usability.
- In global software development, if AI tools cannot adapt to local languages, their practical value in code review workflows is limited.

## Approach
- Add **per-repo output language preference** to GitAuto, enabling output language configuration by repository.
- Code comments and GitHub comments can automatically be output in the team's native language according to repository settings.
- Support for **70+ languages** indicates that the core mechanism is localization at the AI review output layer, rather than changing the format of the main PR content.
- PR titles and bodies remain in English, meaning the system adopts a compromise approach of “localized comments, standardized primary collaboration artifacts.”

## Results
- Coverage: repositories can be configured with output preferences for **70+ languages**.
- Direct capability claim: non-English-speaking teams can now read **GitAuto code comments** and **GitHub comments** in their native language.
- Compatibility maintained: **PR titles and bodies stay in English**, helping preserve a consistent format across teams or in open-source collaboration.
- No quantitative experimental results are provided: the excerpt includes no figures for accuracy, review efficiency, user satisfaction, A/B testing, or numerical comparisons with baseline systems. The strongest specific claim is that the per-repo language configuration feature has been launched and covers 70+ languages.

## Link
- [https://news.ycombinator.com/item?id=47358750](https://news.ycombinator.com/item?id=47358750)
