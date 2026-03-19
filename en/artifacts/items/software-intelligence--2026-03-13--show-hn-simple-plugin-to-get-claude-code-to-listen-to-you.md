---
source: hn
url: https://www.gopeek.ai
published_at: '2026-03-13T23:15:22'
authors:
- itsankur
topics:
- code-assistant
- developer-tools
- preference-learning
- prompt-injection
- human-ai-interaction
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# Show HN: Simple plugin to get Claude Code to listen to you

## Summary
This is a simple plugin for Claude Code that claims to automatically learn user preferences and inject prompts at the right moments, thereby guiding the coding assistant's behavior better than static markdown rule files. The provided content reads more like a product introduction than a paper, so technical details and empirical evidence are very limited.

## Problem
- Coding assistants often struggle to consistently "understand" and follow users' personal preferences, working styles, and implicit rules.
- Relying only on markdown files to constrain assistant behavior may not be flexible enough and may fail to take effect in the right context and at the right time.
- This matters because development efficiency and output quality depend heavily on whether the assistant can reliably follow user intent.

## Approach
- The core mechanism is: **automatically learning user preferences**, rather than requiring users to manually maintain extensive rule descriptions.
- It then **injects these preferences into Claude Code** at the "right moments" to more precisely influence its responses and behavior.
- Put simply: it acts like an intermediary layer that remembers your habits and reminds Claude Code in time to work the way you prefer while you code.
- The product also emphasizes that you can "get started in 5 lines," suggesting lightweight integration, but it provides no implementation details.

## Results
- The text **does not provide quantitative results**—there is no dataset, evaluation metric, baseline method, or ablation study.
- The strongest explicit claim is that Peek "guides Claude Code better than markdown files."
- It also claims that this capability comes from two things: **automatically learning preferences** and **injecting preferences at the right time**.
- It gives no concrete numbers, such as improvements in success rate, code quality, latency overhead, or user study results.

## Link
- [https://www.gopeek.ai](https://www.gopeek.ai)
