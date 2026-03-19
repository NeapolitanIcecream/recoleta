---
source: hn
url: https://backnotprop.com/blog/do-not-ab-test-my-workflow/
published_at: '2026-03-13T23:55:19'
authors:
- ramoz
topics:
- ab-testing
- ai-product
- workflow-regression
- transparency
- human-in-the-loop
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Anthropic, Do Not A/B Test My Workflow

## Summary
This is not an academic paper, but a user complaint and engineer response about product experimentation in Claude Code. The core point is: conducting opaque A/B tests on critical AI features that affect professional workflows harms transparency, controllability, and user trust.

## Problem
- The issue discussed in the article is that an AI coding tool is A/B testing core workflow functionality without clearly informing users or providing an opt-out mechanism, leading to declines in user experience and productivity.
- This matters because the tool is used as a professional productivity tool, and changes in behavior directly affect engineers’ work quality, stability, and trust.
- The author specifically points out that when users cannot distinguish between a “product regression” and an “experimental split,” it weakens their perception of transparency and configurability in the AI system.

## Approach
- The piece does not propose a new research method; instead, it argues the point through personal usage experience, observations from conversations with the model, and public community discussion.
- The author claims that plan mode output was experimentally changed to a shorter format with less context, for example being capped at **40 lines**, prohibiting contextual paragraphs, and emphasizing the removal of prose.
- The article cites a response from a Claude Code engineer explaining that the experimental hypothesis was that shortening plan text might reduce **rate-limit hits** while keeping results as similar as possible.
- The engineer stated that the test included multiple variants, that the author was assigned to the “most aggressive” version, and that the affected population was “a few thousand others.”

## Results
- There is no formal academic evaluation, dataset, or statistical significance analysis, so there are **no reproducible quantitative research results**.
- The most specific numerical information in the article is that the author pays **$200/month** for Claude Code, and cites community comments suggesting that fully enabled resource usage might cost close to **$400/month**, but this is speculation, not an experimental result.
- The experimental setup disclosed by the engineer includes limiting plan mode to **40 lines** and testing the most aggressive version on “few thousand” users.
- The only result-oriented conclusion given by the engineer is: **Early results aren’t showing much impact on rate limits so I’ve ended the experiment**—that is, early results did not show a significant effect on rate-limit hit rates, so the experiment has ended.
- The strongest concrete claim is not a performance improvement, but a product-level conclusion: covertly changing plan mode can make some users feel that their workflow has degraded, and can trigger doubts about the transparency and configurability of AI tools.

## Link
- [https://backnotprop.com/blog/do-not-ab-test-my-workflow/](https://backnotprop.com/blog/do-not-ab-test-my-workflow/)
