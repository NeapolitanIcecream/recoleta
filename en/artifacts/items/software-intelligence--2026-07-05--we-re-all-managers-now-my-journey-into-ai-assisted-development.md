---
source: hn
url: https://mattmccormick.ca/we-re-all-managers-now-my-journey-into-ai-assisted-development/
published_at: '2026-07-05T23:57:12'
authors:
- mattm
topics:
- ai-assisted-development
- code-generation
- human-ai-interaction
- software-engineering-workflow
- requirements-engineering
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# We're All Managers Now: My Journey into AI-Assisted Development

## Summary
This article argues that AI-assisted development shifts software engineers toward manager-like work: defining requirements, delegating implementation to tools such as Claude Code, reviewing outputs, and coordinating parallel tasks.

## Problem
- AI coding tools can produce large amounts of code faster than a human can review it, which changes where engineering time goes.
- Loose requirements cause faster failure: the author’s large-feature experiment produced several PRs in 20-30 minutes, but the implementation missed the intended design.
- Engineers need new habits for context switching, review, and specification because the author found direct code-following less useful as trust in Claude grew.

## Approach
- The author uses Claude Code as the main coding assistant while building a startup project full time.
- The workflow moved from a repeated prompt-process-response cycle to a delegation pattern: write context and requirements, let Claude implement, then review the generated output.
- Requirements and design documents get more attention before implementation because small gaps lead to fast, visible mismatches in generated code.
- During Claude’s processing time, the author starts other tasks and switches between them, similar to managing multiple workstreams.
- The author treats prior engineering-manager skills, such as context switching and reviewing work through feedback loops, as useful for AI-assisted coding.

## Results
- No benchmarked quantitative results are reported; this is a practitioner essay, not an empirical research paper.
- In one experiment, Claude generated several chained PRs in about 20-30 minutes, but the work missed the target because the requirements were unclear.
- The author reports reaching a practical limit at 3 concurrent Claude-assisted tasks because context recovery became hard.
- Some task reviews could take 20 or 30 minutes each, which made returning to a third task difficult after more than 1 hour away.
- Tool usage increased over time: the author started experimenting over Christmas 2024, paid for a basic Claude Code plan in June 2025, and moved to a Claude 5x Max plan in March 2026.

## Link
- [https://mattmccormick.ca/we-re-all-managers-now-my-journey-into-ai-assisted-development/](https://mattmccormick.ca/we-re-all-managers-now-my-journey-into-ai-assisted-development/)
