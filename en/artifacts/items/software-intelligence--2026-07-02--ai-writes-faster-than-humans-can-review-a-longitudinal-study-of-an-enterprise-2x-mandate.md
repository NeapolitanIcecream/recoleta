---
source: arxiv
url: https://arxiv.org/abs/2607.01904v1
published_at: '2026-07-02T09:03:32'
authors:
- Hao He
- Shyam Agarwal
- Yegor Denisov-Blanch
- Pavel Azaletskiy
- Sanmi Koyejo
- Bogdan Vasilescu
topics:
- ai-coding-tools
- software-engineering-productivity
- code-review
- human-ai-interaction
- enterprise-ai-adoption
- difference-in-differences
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# AI Writes Faster Than Humans Can Review: A Longitudinal Study of an Enterprise 2x Mandate

## Summary
This paper studies an enterprise AI coding mandate using internal telemetry from 802 developers and 196,212 pull requests. It finds that PR throughput doubled by April 2026, with most of the gain linked to AI adoption and accumulated tool use.

## Problem
- Companies are mandating AI coding tools and claiming large productivity gains, but prior credible field results range from a 19% slowdown to about 40% more PRs.
- The paper asks whether a 2x engineering-output target can be reached in a real firm, and what happens to review load and short-horizon quality signals.

## Approach
- The authors study a mid-sized B2B software company whose CTO set a June 2025 goal to double merged PRs per engineer per month through AI use.
- They combine PR and review history with Cursor and Claude Code usage logs, producing a January 2024 to April 2026 developer-month panel of 802 developers and 196,212 non-bot PRs across 364 repositories.
- They estimate within-developer changes with staggered difference-in-differences, aligning each developer on their first AI-tool use instead of the company mandate date.
- They separate an adoption jump from growth tied to prior accumulated AI-written lines, and they test whether model release dates explain the gains.
- They treat adoption intensity as observational, so the estimates support an adoption-and-use channel but do not prove exact causal size.

## Results
- Per-capita PR throughput reached 2.09x the pre-mandate baseline in April 2026.
- In the within-developer decomposition, adoption plus accumulated use was linked to about a 1.5x gain for a given developer, with the trajectory reaching 2x by nine months on tool.
- The estimation panel includes 564 developers; 451 adopted an AI tool and 113 never adopted.
- AI-authored PRs rose from near zero to about 90% of PRs by the end of the study window; 30.2% of all 196,212 non-bot PRs carried the created-by-ai label.
- Per-reviewer load roughly doubled, automated review overtook human review, and merge and revert rates stayed about flat.
- Gains were statistically similar across seniority levels, concentrated in newer repositories, and not separable across Sonnet 4.5, Opus 4.5, and Opus 4.6 model generations.

## Link
- [https://arxiv.org/abs/2607.01904v1](https://arxiv.org/abs/2607.01904v1)
