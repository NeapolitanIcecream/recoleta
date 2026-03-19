---
source: hn
url: https://news.ycombinator.com/item?id=47282726
published_at: '2026-03-06T23:56:36'
authors:
- ramoz
topics:
- github
- repo-metadata
- web-ui-bug
- open-source-signals
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# GitHub appears to be hiding repo stars for signed-out users

## Summary
This is not a research paper, but a Hacker News discussion post claiming that GitHub may be hiding repository star counts from signed-out users. The content is very limited; the core information is that a user could still see star data after fetching the page with `curl`, so this appears more likely to be a frontend display issue or bug rather than a verified product policy change.

## Problem
- The issue under discussion is whether GitHub is hiding repository star counts from signed-out users.
- This matters because star counts are often used as a quick signal of an open-source project's popularity, credibility, and adoption.
- However, the provided text contains only one brief comment, so the evidence is insufficient to determine whether this is a systematic change or a localized bug.

## Approach
- An observer raised the suspicion based on what they saw in the web interface: the repository star count did not seem to be visible while signed out.
- A commenter used the simplest validation method: fetching and searching the page content via `curl -sL https://github.com/openai/gpt-2 | grep -iE 'Star |stars'`.
- This check found that the returned content still included star-related data, leading to the explanation that “this is probably a bug.”
- In essence, this is a very lightweight manual visibility check, not a system experiment, measurement study, or formal method.

## Results
- No formal quantitative results, dataset, experimental setup, or statistical comparison are provided.
- The only specific “result” is that after running `curl` on `https://github.com/openai/gpt-2`, the page source still contains retrievable `Star`/`stars` text.
- The discussion thread currently has only **3 points** and **1 comment**, indicating that both the sample and the scale of discussion are extremely small.
- The strongest specific conclusion is not that “GitHub is definitely hiding star counts,” but rather that “at least in the page source of the specific repository provided, star data is still present, so this looks more like a display-layer bug.”

## Link
- [https://news.ycombinator.com/item?id=47282726](https://news.ycombinator.com/item?id=47282726)
