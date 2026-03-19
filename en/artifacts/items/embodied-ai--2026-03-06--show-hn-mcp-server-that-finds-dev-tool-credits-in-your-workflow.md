---
source: hn
url: https://news.ycombinator.com/item?id=47282711
published_at: '2026-03-06T23:54:47'
authors:
- janaksunil
topics:
- mcp-server
- developer-tools
- workflow-assistant
- tool-discovery
- discount-recommendation
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Show HN: MCP server that finds dev tool credits in your workflow

## Summary
This is an MCP server integrated with Claude Code that notifies developers of available credits, discounts, or deals in their workflow when evaluating new tools or initializing a project. It is better understood as a developer tool purchasing-assistance plugin rather than a research paper or a technical work in robotics/foundation models.

## Problem
- When selecting or using tools, developers often do not know about existing credits, discounts, or promotions, which can lead to duplicate spending or missed savings opportunities.
- If the prompting mechanism is too frequent, it turns into ads inside the IDE, disrupting the workflow and reducing usability.
- The author wants to solve the product-experience problem of “providing money-saving information at the right time,” which has practical significance for reducing tool procurement costs.

## Approach
- Build an **MCP server** that can plug into the **Claude Code** workflow.
- The first version triggered whenever the user mentioned any tool, but because it was too “spammy,” it was later changed to trigger only when the user is **actually evaluating a new tool**.
- There are plans to scan **package.json** during initialization to identify tools the project is already using/paying for and surface applicable deals.
- The core mechanism can be understood simply as: **listen to tool context in the development workflow → determine whether the user is in a selection/already-paying scenario → return corresponding discount information**.

## Results
- The text provides **no quantitative experimental results**—no datasets, metrics, baselines, or comparison figures.
- The strongest concrete claim is that the trigger strategy has been improved from “trigger whenever any tool is mentioned” to “trigger only when evaluating a new tool,” in order to reduce intrusive prompts.
- Another concrete plan is to scan `package.json` during init, thereby identifying “tools you are already paying for” and flagging available discounts.
- The current content is more like a product showcase and user research (“Would you use this, or does it feel like ads in your IDE?”) rather than a validated research breakthrough.

## Link
- [https://news.ycombinator.com/item?id=47282711](https://news.ycombinator.com/item?id=47282711)
