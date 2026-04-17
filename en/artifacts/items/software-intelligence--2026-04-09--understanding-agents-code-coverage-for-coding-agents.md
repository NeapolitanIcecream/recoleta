---
source: hn
url: https://blog.asymmetric.re/understanding-agents-code-coverage-for-coding-agents/
published_at: '2026-04-09T23:17:35'
authors:
- matt_d
topics:
- coding-agents
- code-coverage
- security-auditing
- agent-observability
- developer-tools
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Understanding Agents: Code Coverage for Coding Agents

## Summary
This post introduces an open-source tool that reconstructs and visualizes which code a coding agent read during an audit run. It helps humans compare agent behavior across prompts, models, and reasoning levels, and inspect what the agent looked at and missed.

## Problem
- Coding agents can report bugs after long audit runs, but current tools give weak visibility into which files and lines the agent actually inspected.
- That gap makes it hard to judge whether the agent searched the relevant attack surface, compare runs fairly, or guide follow-up audits.
- For security auditing, this matters because an agent cannot find bugs in code it never read, and humans need a way to spot blind spots.

## Approach
- The tool parses local `.jsonl` session logs from Claude Code and `codex-cli`, which contain prompts, reasoning summaries, and executed tool commands.
- It converts the agent's file-reading actions into covered line ranges and links those ranges to the sub-task or intent associated with the read.
- It shows the result in a web UI with highlighted covered lines, a project treemap, per-line coverage counts, and the sub-tasks that touched each region.
- The tool is meant for post-hoc inspection: humans can compare prompts, models, reasoning effort, and repeated runs, then direct later audits toward uncovered areas.

## Results
- On an OpenSSH pre-auth RCE audit task, GPT-5.4 runs stayed focused on a narrower part of the obvious pre-auth surface across five runs per setting.
- Median uniquely covered lines for GPT-5.4 increased with reasoning budget: about 8.3k for `gpt5.4-medium`, 13.5k for `gpt5.4-high`, and 17.7k for `gpt5.4-xhigh`.
- Files touched per GPT-5.4 run also increased with reasoning effort: roughly 24, 35, and 40 files for medium, high, and xhigh.
- Opus 4.6 covered much more code: median uniquely covered lines were about 31.8k for `opus4.6-high` and 30.3k for `opus4.6-medium`, with one medium run reaching roughly 50k lines.
- Across five runs, Opus configurations touched 298 distinct files for high and 395 for medium, while GPT-5.4 settings stayed in the 40 to 62 range.
- The authors state that coverage is not a direct bug-finding metric, but repeated runs still matter because agent behavior is probabilistic and can surface different bugs over time.

## Link
- [https://blog.asymmetric.re/understanding-agents-code-coverage-for-coding-agents/](https://blog.asymmetric.re/understanding-agents-code-coverage-for-coding-agents/)
