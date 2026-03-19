---
source: hn
url: https://news.ycombinator.com/item?id=47282726
published_at: '2026-03-06T23:56:36'
authors:
- ramoz
topics:
- github-ui
- web-bug
- repository-metadata
- frontend-behavior
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# GitHub appears to be hiding repo stars for signed-out users

## Summary
This is not a research paper, but rather a Hacker News discussion about GitHub possibly hiding repository star counts from signed-out users. The content is very short, and the core is a report of an apparent frontend display anomaly, along with a preliminary counterexample check using `curl` to fetch the page.

## Problem
- The issue under discussion is whether GitHub is hiding the display of repository star counts from users who are not logged in.
- This matters because star counts are a commonly used signal of open-source project popularity and social proof; if hidden, they would affect discovery, evaluation, and sharing.
- However, the given text is more like a bug/phenomenon report than a systematic study, and it does not include a formal experimental setup.

## Approach
- An observation is made: the post title claims that GitHub has hidden repo stars from signed-out users.
- The commenter uses the simplest possible check: running `curl -sL ... | grep -iE 'Star |stars'` on `https://github.com/openai/gpt-2`.
- Because that command still retrieves star-related text, the commenter proposes the simplest explanation: this is more likely a bug than GitHub intentionally hiding the data.
- Overall, the mechanism is not a research method, but a quick verification via manual webpage fetching and string matching.

## Results
- The text contains no formal quantitative experimental results, dataset, metrics, or baseline comparisons.
- The only visible numerical information is Hacker News post metadata: `3 points`, `1 comment`, which is not directly related to the technical conclusion.
- The strongest specific claim is: after running `curl` on the `openai/gpt-2` page, it still “shows star data,” therefore it is “probably a bug.”
- No numerical evidence is provided about the scope of the hiding, reproduction rate, browser conditions, regional differences, or time span.

## Link
- [https://news.ycombinator.com/item?id=47282726](https://news.ycombinator.com/item?id=47282726)
