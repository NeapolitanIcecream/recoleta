---
source: hn
url: https://lr0.org/blog/p/crocker/
published_at: '2026-03-13T23:14:37'
authors:
- ghd_
topics:
- technical-communication
- crockers-rules
- engineering-culture
- code-review
- incident-reporting
relevance_score: 0.33
run_id: materialize-outputs
language_code: en
---

# I beg you to follow Crocker's Rules, even if you will be rude to me

## Summary
This article argues for adopting a direct communication style similar to Crocker’s Rules in technical collaboration: reduce polite preambles, preemptive apologies, and self-justification, and get to the actual information as quickly as possible. The core view is that clarity and high signal density are more professional than social cushioning, and are more helpful for debugging, review, and incident response.

## Problem
- The article discusses the problem that a large amount of “polite noise,” small talk, preventive apologies, and lengthy explanations in technical communication can bury the truly important information very deeply.
- This matters because in code review, technical help requests, performance analysis, and incident retrospectives, delays in information and diluted signal waste team time and reduce the efficiency of problem diagnosis and decision-making.
- The author also believes that excessive social packaging trains recipients to skim and weakens the speaker’s technical credibility and the team’s ability to face real problems directly.

## Approach
- The core mechanism is simple: by default, set the goal of communication as “efficient exchange of true information,” allowing the other party to point out problems directly without requiring emotional cushioning first.
- A concrete practice is to remove openings and modifiers that add no information, such as “hope you had a great weekend,” “sorry for the long message,” or “maybe I’m wrong but...”.
- In technical writing, state the facts, impact, and evidence directly, such as “the cache layer added **400ms** to cold requests; trace attached,” rather than first asking for permission to speak.
- In incident explanations, keep only actionable information: what broke, why it broke, and what needs to change; record background factors only when they can lead to structural fixes.
- The author emphasizes that this is not encouragement of rudeness or insult, but an agreement by both sides to decouple emotion management from information transfer and prioritize high-signal content.

## Results
- This is not a paper or experimental report; the article **does not provide a formal dataset, controlled experiments, or statistical metrics**.
- The clearest quantitative example is that the author gives the example that “the cache layer added **400ms** overhead to cold requests,” to illustrate that stating the problem directly is more useful than a long preamble.
- The author’s central concluding claim is that directly saying “this approach is wrong, here's why” saves more time, improves readability, and better respects the recipient than multiple paragraphs of polite buffering.
- In incident report scenarios, the author argues that one should directly write “configuration value X was set to Y, but should have been Z,” rather than adding self-justifying content about stress, blame, or emotional state.
- The article also advances a strong claim: teams that cannot tolerate direct statements of reality will struggle to debug systems more complex than a “typo.”

## Link
- [https://lr0.org/blog/p/crocker/](https://lr0.org/blog/p/crocker/)
