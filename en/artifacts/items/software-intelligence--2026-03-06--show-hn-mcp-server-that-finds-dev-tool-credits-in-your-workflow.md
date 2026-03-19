---
source: hn
url: https://news.ycombinator.com/item?id=47282711
published_at: '2026-03-06T23:54:47'
authors:
- janaksunil
topics:
- mcp-server
- developer-tools
- workflow-integration
- cost-optimization
- human-ai-interaction
relevance_score: 0.57
run_id: materialize-outputs
language_code: en
---

# Show HN: MCP server that finds dev tool credits in your workflow

## Summary
This is an MCP server integrated with Claude Code that surfaces available credits, discounts, or deals when developers are evaluating new tools or scanning existing dependencies. It aims to embed “finding dev tool deals” into real development workflows while avoiding turning into ad-like noise inside the IDE.

## Problem
- When adopting or renewing developer tools, developers often do not know whether there are available credits, discounts, or promotions, leading to unnecessary extra costs.
- If deal prompts trigger too frequently or are unrelated to the current task, they can interrupt the programming flow like ads, reducing the tool’s acceptability.
- This matters because developer tool subscriptions are increasingly numerous; if relevant deal information can be provided at the point of decision, it could directly reduce team software costs.

## Approach
- The core method is simple: build an MCP server integrated with Claude Code that detects moments in the user workflow when they are “evaluating a new tool,” then surfaces relevant credits or discounts.
- The first version triggered whenever a tool name was mentioned, but the author found this too spammy, so it was changed to trigger only when “actually evaluating a new tool,” improving contextual relevance.
- The author is also developing the ability to scan `package.json` on initialization to identify tools already used in the project and possibly being paid for, then surface currently available deals.
- In essence, it does not generate code; it is a context-aware recommendation plugin aimed at development procurement/adoption decisions.

## Results
- The text **does not provide quantitative experimental results**: there are no datasets, baselines, accuracy figures, click-through rates, conversion rates, or user study numbers.
- The most concrete reported progress is that the **first version triggered whenever any tool was mentioned**, and the author changed it to **trigger only when evaluating a new tool** to reduce spam.
- It also states plans to scan **`package.json`** during initialization so it can identify “tools already being paid for” and flag available deals, but no effectiveness metrics are given.
- At present, it is more like an early prototype and product exploration, and the author is explicitly seeking feedback on whether users would actually use it or whether it would feel like ads in the IDE.

## Link
- [https://news.ycombinator.com/item?id=47282711](https://news.ycombinator.com/item?id=47282711)
